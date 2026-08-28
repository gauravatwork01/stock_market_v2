from pathlib import Path
from datetime import datetime
from ..infra.big_query.financials_repo import FinancialsRepo, FinancialReport


def save_financials(source,filename, file_data):
    # Service implementation placeholder; endpoint now forwards uploaded file.

    if source == "nse_file":
        upload_financials_from_nsefile(filename,file_data)


    return None




def upload_financials_from_nsefile(filename,file_data: list[dict]):

    json_value = {}

    for each_row in file_data:
        key = each_row.get("Element Name")
        value = each_row.get("Fact Value")
        json_value[key] = value


    quarter = json_value.get("ReportingQuarter")
    if "first" in quarter.lower():
        quarter = "Q1"
    elif "second" in quarter.lower():
        quarter = "Q2"
    elif "third" in quarter.lower():
        quarter = "Q3"
    elif "fourth" in quarter.lower():
        quarter = "Q4"

    fin_year = json_value.get("DateOfEndOfFinancialYear")
    year = datetime.strptime(fin_year, "%Y-%m-%d").year

    data_row = FinancialsRow(
        symbol = json_value.get("Symbol"),
        quarter = quarter,
        year = year,
        data = json_value,
        source = "nse_file" 
    )
    
    FinancialsRepo().upload_financials(data_row)
    pass 
