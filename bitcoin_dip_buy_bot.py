# Common python libraries

import requests
import time

# Coinbase library

import coinbase_apikey

# Import commands from Rhett Reisman's library

from coinbase_advanced_trader.config import set_api_credentials
from coinbase_advanced_trader.strategies.limit_order_strategies import fiat_limit_buy

# Api key and secret used to access coinbase account

API_KEY = "XXXXXXXXXXXXXXXX"
API_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
set_api_credentials(API_KEY, API_SECRET)

# Headers contain the api key to access coinbase data

headers= {
    'X-CMC_PRO_API_KEY': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    'Accepts': 'application/json'
}

# Params contain what cryptocurrencies to examine. We limit it to the top currency, bitcoin

params = {
    'start': '1',
    'limit': '1',
    'convert': 'USD'
}

# Input the size of the dip

dip = -100

# Input the time interval (seconds) between each price check

interval = 300

# Input the amount of bitcoin to purchase

usd_size = 1

# Input current bitcoin price

current_price = 42624.55

# A list that is limited to the previous bitcoin price check and current bitcoin price

price = [current_price]

# A while loop runs its block of code once every specified time interval

while True:

    # Get the latest bitcoin price and time of day. Store it in a variable called "response"

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    response = requests.get(url, params=params, headers=headers).json()

    # Extract the time of day data. Convert it from zulu to central time

    timestamp = response['status']['timestamp']
    day = timestamp.split("T")[0]
    timestamp = timestamp.split("T")[1].split(".")[0].split(":")
    hour = str(int(timestamp[0]) - 6)

    # Store the time of day in a variable called central_time

    central_time = str(hour) + ":" + timestamp[1] + ":" + timestamp[2]

    # Extract bitcoin price data and store in a variable called bitcoin_price

    bitcoin_price = response['data'][0]['quote']['USD']['price']

    # Print the time of day and the bitcoin price

    print(day + " " + central_time + " " + " Price: " + str(bitcoin_price))

    # Add the price to the price list

    price.append(bitcoin_price)

    # Limit the price list to the most recent 2 entries

    price = price[-2:]

    # Check the difference in price. Store it in a variable called change

    change = price[1] - price[0]

    # Print the change in price

    print("Change: " + str(change)[:5])

    # If change is less than the desired dip...

    if change < dip:

        # ...purchase desired amount of bitcoin using coinbase cash account

        # limit_buy_order = fiat_limit_buy("BTC-USD", usd_size)

        # Print a message that a purchase was made

        print("Time to buy.")

    # Pause before running the while loop again

    time.sleep(interval)


