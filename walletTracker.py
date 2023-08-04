import moralis, os
from moralis import evm_api
from dotenv import load_dotenv
import pygsheets

load_dotenv()
api_key = os.getenv("API_KEY")

service_file = 'credentials.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = "Wallet Tracker"
sh = gc.open(sheetname)

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

def getAddresses():
    wks = sh.worksheet_by_title("Ethereum Wallets")
    addresses = wks.get_values("A2", "A1000", returnas="matrix", include_tailing_empty="false")
    return addresses

def createNewSheet():
    for i in range(len(getAddresses())+1):
        try:
            str(sh.worksheet(property="index", value=i))
            if str(sh.worksheet(property="index", value= i)) != "<Worksheet 'Ethereum Wallets' index:0>":
                sh.del_worksheet(sh.worksheet(property="index", value=i))
            else:
                continue
        except:
            pass
    for i in range(len(getAddresses())):
        title = getAddresses()
        sh.add_worksheet(str(title[i]), rows=5, cols=3, src_tuple=None, src_worksheet=None, index=None)
        continue
    return
def generateSheetValues():
    addresses = getAddresses()
    for i in range(len(addresses)):
        data = getWalletData({"chain": "eth", "address":str(addresses[i])})
        wks = sh.worksheet_by_title(str(addresses[i]))
        wks.update_value("A1", "Token")
        wks.update_value("B1", "Quantity")
        wks.update_value("C1", "USD Value")
        wks.update_value("A"+str(i+2), data[i][0])
        continue
    return

generateSheetValues()