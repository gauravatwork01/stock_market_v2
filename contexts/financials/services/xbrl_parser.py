from collections import defaultdict
from lxml import etree
from datetime import datetime


def classify_period(start, end):
    if not start or not end:
        return None
    
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    
    days = (end_date - start_date).days
    
    if days <= 100:      # roughly 1 quarter (~90 days)
        return "quarterly"
    elif days >= 350:    # roughly full year (~365 days)
        return "year_to_date"
    else:
        return "other"   # e.g. half-year, 9-months etc.


def flatten_facts(sorted_facts):
    flat_facts = {}
 
    for key, value in sorted_facts.items():
        if key == "general":
            flat_facts.update(value)
            continue
 
        axis = key
        for label, collapsed_value in value.items():
            if isinstance(collapsed_value, dict):
                for concept, v in collapsed_value.items():
                    flat_facts[f"{axis}__{label}__{concept}"] = v
            else:
                flat_facts[f"{axis}__{label}"] = collapsed_value
 
    flat_facts = dict(sorted(flat_facts.items()))
    return flat_facts



def parse_xbrl(link_content):
    root = etree.fromstring(link_content)
    ns = root.nsmap

    # --------------------------------------------------
    # 1. Parse contexts
    # --------------------------------------------------

    contexts = {}

    for context in root.xpath("./xbrli:context", namespaces=ns):

        context_id = context.get("id")

        identifier = context.xpath(
            "./xbrli:entity/xbrli:identifier/text()",
            namespaces=ns
        )

        instant = context.xpath(
            "./xbrli:period/xbrli:instant/text()",
            namespaces=ns
        )

        start = context.xpath(
            "./xbrli:period/xbrli:startDate/text()",
            namespaces=ns
        )

        end = context.xpath(
            "./xbrli:period/xbrli:endDate/text()",
            namespaces=ns
        )

        # Explicit dimensions: axis (attribute) -> member (text)
        dimensions = {}
        for member in context.xpath(".//xbrldi:explicitMember", namespaces=ns):
            axis = member.get("dimension")
            dimensions[axis] = member.text

        # Typed dimensions: axis (attribute) -> filer-defined value (text)
        typed_dimensions = {}
        for member in context.xpath(".//xbrldi:typedMember", namespaces=ns):
            axis = member.get("dimension")
            value = "".join(member.itertext()).strip()
            typed_dimensions[axis] = value

        contexts[context_id] = {
            "entity": identifier[0] if identifier else None,

            "period_type": (
                "instant"
                if instant
                else "duration"
                if start and end
                else None
            ),

            "instant": instant[0] if instant else None,
            "start": start[0] if start else None,
            "end": end[0] if end else None,

            "dimensions": dimensions,
            "typed_dimensions": typed_dimensions,
        }

    # --------------------------------------------------
    # 2. Parse units (unchanged)
    # --------------------------------------------------

    units = {}
    for unit in root.xpath("./xbrli:unit", namespaces=ns):
        unit_id = unit.get("id")
        measures = unit.xpath("./xbrli:measure/text()", namespaces=ns)
        units[unit_id] = measures

    # --------------------------------------------------
    # 3. Discover every axis present in the file
    # --------------------------------------------------

    axes = set()
    for ctx in contexts.values():
        axes.update(ctx["dimensions"].keys())
        axes.update(ctx["typed_dimensions"].keys())

    # --------------------------------------------------
    # 4. Collect quarterly facts, grouped by context_id
    #    (never keyed by concept alone -> no overwrite bugs)
    # --------------------------------------------------

    facts_by_context = defaultdict(dict)

    for element in root:
        context_id = element.get("contextRef")
        if not context_id:
            continue

        context = contexts.get(context_id)
        if context is None:
            continue

        period_classification = classify_period(context["start"], context["end"])
        if period_classification != "quarterly":
            continue

        concept = etree.QName(element).localname
        value = element.text.strip() if element.text else None

        facts_by_context[context_id][concept] = value

    # --------------------------------------------------
    # 5. Split into:
    #      - flat scalar facts (non-dimensional contexts) under "general"
    #      - dimensional facts, grouped: axis -> label -> value (or
    #        axis -> label -> {concept: value} when a row has more than
    #        one reported fact besides its Description)
    # --------------------------------------------------

    facts = {"general": {}}
    dimensional = {axis.split(":", 1)[-1] if axis else axis: {} for axis in axes}

    for context_id, concept_values in facts_by_context.items():
        context = contexts[context_id]
        all_dims = {**context["dimensions"], **context["typed_dimensions"]}

        if not all_dims:
            # Non-dimensional context -> merge straight into flat facts
            facts["general"].update(concept_values)
            continue

        # Dimensional context -> resolve a human-readable label.
        # Prefer a sibling "Description*" fact sharing this same context;
        # otherwise fall back to the raw member/typed-member value.
        label = next(
            (v for c, v in concept_values.items() if c.startswith("Description")),
            next(iter(all_dims.values()))
        )

        # Everything except the Description fact itself is the row's data
        row = {
            c: v for c, v in concept_values.items()
            if not c.startswith("Description")
        }

        # If this row boils down to exactly one fact (the common
        # "description + amount" pattern, e.g. OtherExpenses), flatten it
        # to axis -> label -> value directly. Otherwise (e.g. the auditor
        # context with 3 facts), keep the inner concept:value breakdown.
        if len(row) == 1:
            (only_value,) = row.values()
            collapsed = only_value
        else:
            collapsed = row

        for axis in all_dims:
            clean_axis = axis.split(":", 1)[-1] if axis else axis
            dimensional.setdefault(clean_axis, {})[label] = collapsed

    facts.update(dimensional)

    sorted_facts = dict(sorted(facts.items()))
    flattened_facts = flatten_facts(sorted_facts)
    return sorted_facts, flattened_facts



