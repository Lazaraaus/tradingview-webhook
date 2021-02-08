import cbpro
import config
import time
import datetime as dt

auth_client = cbpro.AuthenticatedClient(config.CB_API_KEY, config.CB_API_SECRET, config.CB_PASSPHRASE)

initInvestment = 20.00

funding = initInvestment

currency = 'XLM-USD'

# def getSpecificAccount(cur):
#     x = auth_client.get_accounts()
#     for account in x:
#         if account['currency'] == cur:
#             return account['id']

# specificID = getSpecificAccount(currency[:3])

# period = 300

# iteration = 1

# buy = True

newData = auth_client.get_product_ticker(product_id = currency)
print(newData)
currentPrice = newData['price']
print(currentPrice)

# possiblePurchase = (float(funding)) / float(currentPrice)
# auth_client.place_market_order(product_id=currency, side='buy', funds=str(funding))

# message = "buyin"
