import moralis, os
from moralis import evm_api
from dotenv import load_dotenv
import pygsheets

load_dotenv()
api_key = os.getenv("API_KEY")

def getWalletData(params):
    tokenData = evm_api.token.get_wallet_token_balances(api_key=api_key, params=params)
    array_length = len(tokenData)
    walletTokens = []
    walletBalance = []
    tokenAddresses = []
    finalBalance = []
    for i in range(array_length):
        walletTokens.append(tokenData[i]["name"])
        walletBalance.append(float(tokenData[i]["balance"])*10**-abs(tokenData[i]["decimals"]))
        tokenAddresses.append(tokenData[i]['token_address'])
        continue
    for i in range(array_length):
        tokenAdd = tokenAddresses[i]
        try:
            tokenValue = evm_api.token.get_token_price(api_key=api_key, params={"address": tokenAdd,"chain": "eth"})
            if tokenValue["usdPrice"] > 1:
                finalBalance.append([walletTokens[i],walletBalance[i],tokenValue["usdPrice"]])
            else:
                continue
        except:
            continue
    return finalBalance

print(getWalletData({"chain": "eth", "address": "0x9297c0545e262fB6D6F096a9c6ff5365190FfDcd"}))

