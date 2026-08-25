from pathlib import Path




def save_financials(source,filename, file_data):
    # Service implementation placeholder; endpoint now forwards uploaded file.

    if source == "nse_file":
        upload_financials_from_nsefile(filename,file_data)


    return None


from ..infra.big_query.financials_repo import FinancialsRepo

def upload_financials_from_nsefile(filename,file_data: list[dict]):

    file_stem = Path(filename).stem
    symbol, financial_year, quarter = file_stem.split("_")

    data_row = {
        
    }
    pass 
