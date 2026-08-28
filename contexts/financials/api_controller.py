import csv
from io import StringIO
import pandas as pd
from io import BytesIO
from .services.upload_services import save_financials
from .services import content_reader
from .services import mapping_services, data_analyzer
from contexts.financials.infra.big_query.financials_repo import FinancialsRepo
from contexts.financials.models import FinancialReport


class FlaskFile:

    def read_uploaded_file_to_bytes(self,file_attachment):
        if file_attachment is None:
            return b""

        file_attachment.stream.seek(0)
        content = file_attachment.read()
        file_attachment.stream.seek(0)
        return content


    def convert_bytes_to_string(self,content_bytes):
        if content_bytes is None:
            return ""
        encoding = "utf-8"
        return content_bytes.decode(encoding)


    def read_string_to_csvrows(self,content_string):
        return list(csv.DictReader(StringIO(content_string)))

    def to_csvrows(self,file_attachment):
        content_bytes = self.read_uploaded_file_to_bytes(file_attachment)
        content_string = self.convert_bytes_to_string(content_bytes)
        csv_rows = self.read_string_to_csvrows(content_string)
        return csv_rows

    def to_rows(self, file_attachment)->list[dict]:
        if file_attachment is None:
            return []

        filename = (file_attachment.filename or "").lower()
        content = self.read_uploaded_file_to_bytes(file_attachment)

        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content), dtype=str)
            df.columns = df.columns.str.strip()
            return df.to_dict(orient="records")
            # text = content.decode("utf-8-sig", errors="replace")
            # return list(csv.DictReader(StringIO(text)))

        if filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content), dtype=str)
            df = df.fillna("")
            return df.to_dict(orient="records")




def upload_financials(request):
    file_attachment = request.files.get("file")
    source = request.form.get("source")

    flask_file = FlaskFile()
    file_rows = flask_file.to_rows(file_attachment)

    save_financials(source, file_attachment.filename, file_rows)
    


def ingest_xbrl_filings(request):
    file_attachment = request.files.get("file")
    flask_file = FlaskFile()
    file_rows = flask_file.to_rows(file_attachment)

    for each_row in file_rows:
        xbrl_link = each_row.get("XBRL")
        if xbrl_link:
            xbrl_content = content_reader.fetch_link_contents(xbrl_link)
            xbrl_data = content_reader.parse_xbrl(xbrl_content)
            fin_report : FinancialReport = mapping_services.parse_xbrl_data_to_domain(xbrl_data,xbrl_link)
            financials_repo = FinancialsRepo()
            financials_repo.upload_financials(fin_report)
        pass 
    pass 




def get_financials(isin):
    financials_repo = FinancialsRepo()
    data = financials_repo.get_financials(isin)
    data = data_analyzer.analyze(data)
    return data
