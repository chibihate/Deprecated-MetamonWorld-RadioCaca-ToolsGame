import requests
import os
from prettytable import PrettyTable
from dotenv import load_dotenv

load_dotenv()

ADDRESS_WALLET = os.getenv("ADDRESS_WALLET")
SIGN_WALLET = os.getenv("SIGN_WALLET")
MSG_WALLET = os.getenv("MSG_WALLET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

typeItems = {
    1: "Metamon Fragments",
    2: "Potion",
    3: "Yellow diamond",
    4: "Purple diamond",
    5: "u-RACA",
    6: "Egg",
    7: "Space ticket",
    8: "Valhalla",
    10: "Purple potion",
    11: "Anti-fatigue potion",
    12: "N stimulant",
    13: "R stimulant",
    14: "SR stimulant",
    1004: "Donuts",
    1015: "Villa fragments",
    1016: "Mansion fragments",
    1017: "Castle fragments",
}

orderTypes = {
    2: "LowestPrice",
    -2: "HighestPrice",
    3: "LowestTotalPrice",
    -3: "HighestTotalPrice",
}


def getTypeItem():
    table = PrettyTable()
    table.field_names = ["Number", "Item"]
    table.align["Number"] = "r"
    table.align["Item"] = "l"
    for item in typeItems:
        table.add_row([item, typeItems[item]])
    print(str(table) + "\nPlease choose number:")
    while 1 != 0:
        number = int(input())
        if number not in typeItems.keys():
            print("Number is out of range")
            print("Please choose number again:")
            continue
        elif number == 1 or number == 5:
            print(f"{typeItems[number]} is not available in market")
            print("Please choose number again:")
            continue
        else:
            return number


def getOrderType():
    table = PrettyTable()
    table.field_names = ["Number", "Item"]
    table.align["Number"] = "r"
    table.align["Item"] = "l"
    for type in orderTypes:
        table.add_row([type, orderTypes[type]])
    print(str(table) + "\nPlease choose number:")
    while 1 != 0:
        number = int(input())
        if number not in orderTypes.keys():
            print("Number is out of range")
            print("Please choose number again:")
            continue
        else:
            return number


class AccessGame:
    def __init__(self, address, sign, msg):
        self.accessToken = None
        self.address = address
        self.sign = sign
        self.msg = msg
        self.initAccessToken()

    def getAccessToken(self):
        """Obtain token for game session to perform battles and other actions"""
        payload = {
            "address": self.address,
            "sign": self.sign,
            "msg": self.msg,
            "network": "1",
            "clientType": "MetaMask",
        }
        url = "https://metamon-api.radiocaca.com/usm-api/login"
        response = requests.request("POST", url, data=payload)
        json = response.json()
        self.accessToken = json.get("data").get("accessToken")
        print("Access token: " + self.accessToken)

    def getLoginCode(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address}
        url = "https://metamon-api.radiocaca.com/usm-api/owner-setting/email/sendLoginCode"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        if json.get("code") == "SUCCESS":
            print("Code is sending to your email. Kindly check")

    def verifyLoginCode(self, loginCode):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "code": loginCode}
        url = "https://metamon-api.radiocaca.com/usm-api/owner-setting/email/verifyLoginCode"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        if json.get("code") == "SUCCESS":
            print("Email is verified")

    def initAccessToken(self):
        self.getAccessToken()
        self.getLoginCode()
        print("Please fill your code:")
        self.verifyLoginCode(loginCode=input())


class MetamonPlayer:
    def __init__(self, address, accessToken):
        self.accessToken = accessToken
        self.address = address
        self.fragmentNum = 0
        self.battleWin = 0
        self.battleLose = 0

    def checkBag(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address}

        url = "https://metamon-api.radiocaca.com/usm-api/checkBag"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        itemsInBag = json.get("data").get("item")
        table = PrettyTable()
        table.title = "All items in bag"
        table.field_names = ["Item", "Amount"]
        table.align["Amount"] = "r"
        table.align["Item"] = "l"
        for item in itemsInBag:
            if item["bpType"] > 0 and int(item["bpNum"]) > 0:
                table.add_row([typeItems[int(item["bpType"])], item["bpNum"]])
        print(table)

    def getShopOrderList(self, typeItem, orderType, pageSize):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "type": typeItem,
            "orderType": orderType,
            "orderId": "-1",
            "pageSize": pageSize,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/shop-order/sellList"
        print(f"Price of {typeItems[typeItem]} with {orderTypes[orderType]}")
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("data").get("shopOrderList")

    def getPriceInMarket(self, typeItem, orderType):
        shopOrderList = self.getShopOrderList(typeItem, orderType, 15)
        indexNumber = 0
        table = PrettyTable()
        table.field_names = ["Index", "Unit price", "Quantity", "Total price"]
        table.align["Index"] = "r"
        table.align["Unit price"] = "r"
        table.align["Quantity"] = "r"
        table.align["Total price"] = "r"
        result = {}
        for shopOrder in shopOrderList:
            indexNumber += 1
            result[indexNumber] = shopOrder["id"]
            table.add_row(
                [
                    indexNumber,
                    shopOrder["amount"],
                    shopOrder["quantity"],
                    shopOrder["totalAmount"],
                ]
            )
        print(table)
        return result

    def buyItem(self, orderId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "orderId": orderId}

        url = "https://metamon-api.radiocaca.com/usm-api/shop-order/buy"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        print(json)

    def shellItem(self, typeItem, quantity, price):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "type": typeItem,
            "quantity": quantity,
            "amount": price,
        }

        url = "https://metamon-api.radiocaca.com/usm-api/shop-order/sell"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        print(json)

    def shopping(self):
        typeItem = getTypeItem()
        orderType = getOrderType()
        while 1 != 0:
            priceInMarket = self.getPriceInMarket(typeItem, orderType)
            caseNumber = int(input("Select 1-15 to buy - 0 to refresh\n"))
            if caseNumber == 0:
                continue
            elif caseNumber in range(16):
                self.buyItem(priceInMarket[caseNumber])
                continue
            else:
                return

    def shellingUnitItem(self):
        typeItem = getTypeItem()
        while 1 != 0:
            self.getPriceInMarket(typeItem, 3)
            shopOrderList = self.getShopOrderList(typeItem, 3, 1)
            lowestPrice = int(shopOrderList[0]["amount"])
            print(f"The lowest price is {lowestPrice}")
            caseNumber = int(input("1. Shell lowest\n2. Set the price\n"))
            if caseNumber == 1:
                lowestPrice -= 1
                print(f"The lowest price will shell {lowestPrice}")
                self.shellItem(typeItem, 1, lowestPrice)
                continue
            elif caseNumber == 2:
                price = int(input("Insert your price\n"))
                self.shellItem(typeItem, 1, price)
                continue
            else:
                return

    def getOnSaleList(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "orderId": "-1",
            "pageSize": 20,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/shop-order/onSaleList"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("data").get("shopOrderList")

    def getItemsOnSale(self):
        itemOnSale = self.getOnSaleList()
        indexNumber = 0
        table = PrettyTable()
        table.field_names = ["Index", "Item", "Unit price", "Quantity", "Total price"]
        table.align["Index"] = "r"
        table.align["Item"] = "l"
        table.align["Unit price"] = "r"
        table.align["Quantity"] = "r"
        table.align["Total price"] = "r"
        result = {}
        for item in itemOnSale:
            indexNumber += 1
            result[indexNumber] = item["id"]
            table.add_row(
                [
                    indexNumber,
                    typeItems[item["type"]],
                    item["amount"],
                    item["quantity"],
                    item["totalAmount"],
                ]
            )
        print(table)
        return result

    def cancelItem(self, orderId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "orderId": orderId}

        url = "https://metamon-api.radiocaca.com/usm-api/shop-order/cancel"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        print(json)

    def canceling(self):
        while 1 != 0:
            ItemsOnSale = self.getItemsOnSale()
            caseNumber = int(
                input(
                    f"Select number in range {len(ItemsOnSale)} to cancel - 0 to refresh\n"
                )
            )
            if caseNumber == 0:
                continue
            elif caseNumber in range(len(ItemsOnSale) + 1):
                self.cancelItem(ItemsOnSale[caseNumber])
                continue
            else:
                return


if __name__ == "__main__":
    accessTokenGame = ""

    helloContent = """
    1. Get access token game
    2. Get metamon player
    3. Check bag
    4. Check price in the market
    5. Shopping
    6. Shelling unit item
    7. Canceling
    0. Exit
    Please select you want to choose
    """
    while 1 != 0:
        caseNumber = int(input(helloContent))
        if caseNumber == 1:
            getAccessTokenGame = AccessGame(
                address=ADDRESS_WALLET, sign=SIGN_WALLET, msg=MSG_WALLET
            )
            accessTokenGame = getAccessTokenGame.accessToken
        if caseNumber == 2:
            if accessTokenGame == "":
                mtm = MetamonPlayer(address=ADDRESS_WALLET, accessToken=ACCESS_TOKEN)
            else:
                mtm = MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessTokenGame)
        if caseNumber == 3:
            mtm.checkBag()
        if caseNumber == 4:
            typeItem = getTypeItem()
            orderType = getOrderType()
            while 1 != 0:
                mtm.getPriceInMarket(typeItem, orderType)
        if caseNumber == 5:
            mtm.shopping()
        if caseNumber == 6:
            mtm.shellingUnitItem()
        if caseNumber == 7:
            mtm.canceling()
        if caseNumber == 0:
            exit()
