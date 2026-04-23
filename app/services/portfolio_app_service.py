from infrastructure.api_clients.kite_connect_client import KiteConnectAPIClient
from domains.portfolio.portfolio_domain_services import PortfolioDomainService

class PortfolioApplicationService:


    def get_holdings():

        kc_api_client = KiteConnectAPIClient()
        holdings : list[dict] = kc_api_client.portfolio.get_portfolio_holdings()

        holdings : list[dict] = PortfolioDomainService.compute_portfolio_metrics(holdings)
        return holdings 


