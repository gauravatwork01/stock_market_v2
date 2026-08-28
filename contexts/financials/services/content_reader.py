

import requests
from lxml import etree
import xml.etree.ElementTree as ET
import certifi
from arelle import Cntlr, ModelManager



def fetch_link_contents(xbrl_link):
    resp = requests.get(
        xbrl_link,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        verify="/opt/homebrew/etc/openssl@3/cert.pem",
        timeout=(10, 60),
    )
    resp.raise_for_status()
    return resp.content



def read_xbrl_to_json(xbrl_link):
    link_content = fetch_link_contents(xbrl_link)
    parse_xbrl(link_content)


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

        # Explicit dimensions
        dimensions = {}

        for member in context.xpath(
            ".//xbrldi:explicitMember",
            namespaces=ns
        ):
            dimensions[member.get("dimension")] = member.text

        # Typed dimensions
        typed_dimensions = {}

        for member in context.xpath(
            ".//xbrldi:typedMember",
            namespaces=ns
        ):
            dimension = member.get("dimension")

            value = "".join(member.itertext()).strip()

            typed_dimensions[dimension] = value

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
    # 2. Parse units
    # --------------------------------------------------

    units = {}

    for unit in root.xpath("./xbrli:unit", namespaces=ns):

        unit_id = unit.get("id")

        measures = unit.xpath(
            "./xbrli:measure/text()",
            namespaces=ns
        )

        units[unit_id] = measures

    # --------------------------------------------------
    # 3. Parse facts
    # --------------------------------------------------

    facts = {}

    for element in root:

        context_id = element.get("contextRef")

        # Not a financial/data fact
        if not context_id:
            continue

        context = contexts.get(context_id)

        if context is None:
            continue

        concept = etree.QName(element).localname

        value = (
            element.text.strip()
            if element.text
            else None
        )

        # fact = {
            # "concept": concept,
            # "value": value,
            # concept: value,

            # "unit": element.get("unitRef"),
            # "decimals": element.get("decimals"),
            # "context_id": context_id,

            # "entity": context["entity"],
            # "period_type": context["period_type"],
            # "period_start": context["start"],
            # "period_end": context["end"],
            # "instant": context["instant"],
            # "dimensions": context["dimensions"],
            # "typed_dimensions": context["typed_dimensions"],

        # }
        # print(fact)
        period_classification = classify_period(context["start"], context["end"])
        if period_classification == "quarterly":
            facts[concept] = value
        else:
            continue 
        # facts[concept] = value

    sorted_facts = dict(sorted(facts.items()))
    return sorted_facts



