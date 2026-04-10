from repositories.bigquery_client import BigQueryManager




class TokenRepository:


    @staticmethod
    def get_latest_token():
        query = f"""
        SELECT *
        FROM `{BigQueryManager.get_table_path("request_tokens")}`
        ORDER BY timestamp DESC
        LIMIT 1
        """

        result = BigQueryManager.client.query(query).result()

        latest_row = next(result, None)

        print(latest_row) 







