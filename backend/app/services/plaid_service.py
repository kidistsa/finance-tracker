# import plaid
# from plaid.api import plaid_api
# from plaid.model.link_token_create_request import LinkTokenCreateRequest
# from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
# from plaid.model.transactions_sync_request import TransactionsSyncRequest
# from app.core.config import settings

# class PlaidService:
#     def __init__(self):
#         configuration = plaid.Configuration(
#             host=plaid.Environment.Sandbox,  # Use Development for production
#             api_key={
#                 'clientId': settings.PLAID_CLIENT_ID,
#                 'secret': settings.PLAID_SECRET,
#             }
#         )
#         api_client = plaid.ApiClient(configuration)
#         self.client = plaid_api.PlaidApi(api_client)
    
#     def create_link_token(self, user_id: str):
#         """Create a link token for Plaid Link initialization"""
#         request = LinkTokenCreateRequest(
#             user={"client_user_id": user_id},
#             client_name="Birr Finance Tracker",
#             products=["transactions"],
#             country_codes=["US", "GB"],  # Add ET when available
#             language="en",
#             webhook="https://your-domain.com/api/plaid/webhook"
#         )
#         response = self.client.link_token_create(request)
#         return response['link_token']
    
#     def exchange_public_token(self, public_token: str):
#         """Exchange public token for access token"""
#         request = ItemPublicTokenExchangeRequest(public_token=public_token)
#         response = self.client.item_public_token_exchange(request)
#         return response['access_token'], response['item_id']
    
#     def sync_transactions(self, access_token: str, cursor: str = None):
#         """Sync transactions from Plaid"""
#         request = TransactionsSyncRequest(
#             access_token=access_token,
#             cursor=cursor
#         )
#         response = self.client.transactions_sync(request)
#         return response['transactions'], response['next_cursor']