from contexts.financials.models import FinancialReport 


def convert_to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None



def parse_xbrl_data_to_domain(xbrl_data,xbrl_link):
    source = "xbrl_file"
    symbol = xbrl_data.get("Symbol")
    isin = xbrl_data.get("ISIN")
    company_name = xbrl_data.get("NameOfTheCompany")
    sebi_intimation_date = xbrl_data.get("DateOnWhichPriorIntimationOfTheMeetingForConsideringFinancialResultsWasInformedToTheExchange")
    results_approval_date = xbrl_data.get("DateOfBoardMeetingWhenFinancialResultsWereApproved")

    quarter = xbrl_data.get("ReportingQuarter")
    if quarter:
        if "first" in quarter.lower():
            quarter = "Q1"
        elif "second" in quarter.lower():
            quarter = "Q2"
        elif "third" in quarter.lower():
            quarter = "Q3"
        elif "fourth" in quarter.lower():
            quarter = "Q4"
    else:
        pass 

    financial_end_date = xbrl_data.get("DateOfEndOfFinancialYear")
    financial_year = int(financial_end_date.split("-")[0]) if financial_end_date else None


    nature_of_report = xbrl_data.get("NatureOfReportStandaloneConsolidated")

    finance_costs = xbrl_data.get("FinanceCosts")
    finance_costs = convert_to_float(finance_costs)

    employee_benefits_expense = xbrl_data.get("EmployeeBenefitExpense")
    employee_benefits_expense = convert_to_float(employee_benefits_expense)

    depreciation_amortization = xbrl_data.get("DepreciationDepletionAndAmortisationExpense")
    depreciation_amortization = convert_to_float(depreciation_amortization)

    # Expense Items
    other_production_expenses = xbrl_data.get("Other production expenses")
    other_production_expenses = convert_to_float(other_production_expenses)

    other_expenses = xbrl_data.get("Other expenses")
    other_expenses = convert_to_float(other_expenses)

    cost_of_materials_consumed = xbrl_data.get("CostOfMaterialsConsumed")
    cost_of_materials_consumed = convert_to_float(cost_of_materials_consumed)

    professional_charges = xbrl_data.get("Professional charges")
    professional_charges = convert_to_float(professional_charges)


    type_of_report_period = xbrl_data.get("TypeOfReportingPeriod")
    type_of_report_period = type_of_report_period.lower()

    report_period_end_date = xbrl_data.get("DateOfEndOfReportingPeriod")

    fin = FinancialReport(
        isin = isin,
        source = source,
        source_link = xbrl_link,
        type_of_report_period = type_of_report_period,
        report_period_end_date = report_period_end_date,
        symbol = symbol,
        company_name = company_name,
        sebi_intimation_date = sebi_intimation_date,
        results_approval_date = results_approval_date,
        quarter = quarter,
        fin_year = financial_year,
        nature_of_report = nature_of_report,
        finance_costs = finance_costs,
        employee_benefits_expense = employee_benefits_expense,
        depreciation_amortization = depreciation_amortization,
        professional_charges = professional_charges,
        cost_of_materials_consumed = cost_of_materials_consumed,
        other_production_expenses = other_production_expenses,
        other_expenses = other_expenses,
    )


    return fin


















