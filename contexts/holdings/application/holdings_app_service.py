from shared.infrastructure import get_kc_api_client
from contexts.broker_auth.application.services import get_access_token



class HoldingsAppService:


    @staticmethod
    def get_holdings():
        kc_client = get_kc_api_client()

        access_token = get_access_token()

        kc_client.set_access_token(access_token)

        pass 
        # bq_holdings_repo = BigQueryHoldingsRepository(
        #     bigquery_client = BigQueryClient()
        # )
        # kite_holdings_provider = KiteHoldingsProvider(
        #     kite_client = kc_api_client()
        # )
        # holdings = GetHoldingsUseCase(
        #     holdings_repo = bq_holdings_repo,
        #     kite_provider = kite_holdings_provider
        # ).get_holdings()

        # return holdings
        return True 





