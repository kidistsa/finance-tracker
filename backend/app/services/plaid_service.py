import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import datetime, timedelta
from app.core.config import settings

class PlaidService:
    def __init__(self):
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': settings.PLAID_CLIENT_ID,
                'secret': settings.PLAID_SECRET,
            }
        )
        self.client = plaid.ApiClient(configuration)
        self.api_client = plaid_api.PlaidApi(self.client)
    
    def create_link_token(self, user_id: str):
        request = LinkTokenCreateRequest(
            user={"client_user_id": user_id},
            client_name="Personal Finance Tracker",
            products=["transactions"],
            country_codes=["US"],
            language="en"
        )
        response = self.api_client.link_token_create(request)
        return response['link_token']
    
    def exchange_public_token(self, public_token: str):
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.api_client.item_public_token_exchange(request)
        return response['access_token']
    
    def get_transactions(self, access_token: str):
        now = datetime.now()
        start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = now.strftime('%Y-%m-%d')
        
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = self.api_client.transactions_get(request)
        return response['transactions']