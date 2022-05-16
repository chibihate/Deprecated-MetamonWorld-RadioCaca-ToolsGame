import requests
from prettytable import PrettyTable
import time

typeItems = {
    -1: "All",
    0: "Metamon",
    1: "Metamon Fragments",
    2: "Potion",
    3: "Yellow diamond",
    4: "Purple diamond",
    5: "u-RACA",
    6: "Egg",
    7: "Space ticket",
    8: "Valhalla",
    9: "N Battle Flag",
    10: "Purple potion",
    11: "Anti-fatigue potion",
    12: "N stimulant",
    13: "R stimulant",
    14: "SR stimulant",
    1004: "Donuts",
    1007: "Spaceship",
    1008: "Rocket",
    1015: "Villa fragments",
    1016: "Mansion fragments",
    1017: "Castle fragments",
    1018: "Villa",
    1019: "Mansion",
    1020: "Castle",
}

orderTypes = {
    2: "LowestPrice",
    -2: "HighestPrice",
    3: "LowestTotalPrice",
    -3: "HighestTotalPrice",
}

dealTypes = {
    -1: "All",
    2: "Level up",
    3: "Deposit",
    4: "Withdraw",
    6: "Mint",
    7: "Open",
    8: "Buy",
    9: "Sell",
    10: "Lock",
    11: "Stake",
    13: "+Exp",
    14: "Enhance",
    15: "+Space ticket",
    16: "Travel",
    17: "+Health",
    19: "World Rewards",
    20: "Reset",
}


def tableSelect(types, exceptNumber=[]):
    table = PrettyTable()
    table.field_names = ["Number", "Item"]
    table.align["Number"] = "r"
    table.align["Item"] = "l"
    for numberID in types:
        table.add_row([numberID, types[numberID]])
    print(str(table) + "\nPlease choose number:")
    while 1 != 0:
        number = int(input())
        if number not in types.keys():
            print("Number is out of range")
            print("Please choose number again:")
            continue
        elif number in exceptNumber:
            print(f"{types[number]} is not available in market")
            print("Please choose number again:")
            continue
        else:
            return number


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
        exceptNumber = [-1, 0, 1, 5, 9, 1018, 1019, 1020]
        typeItem = tableSelect(typeItems, exceptNumber)
        orderType = tableSelect(orderTypes)
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

    def shoppingWithSetPrice(self):
        exceptNumber = [-1, 0, 1, 5, 9, 1018, 1019, 1020]
        typeItem = tableSelect(typeItems, exceptNumber)
        orderType = tableSelect(orderTypes)
        self.getPriceInMarket(typeItem, orderType)
        item = self.getShopOrderList(typeItem, orderType, 1)
        lowestPrice = int(item[0]["amount"])
        print(f"The lowest price of item is {lowestPrice}")
        shoppingContent = """
        1. The lowest price
        2. Set price
        0. Exit
        Please select you want to choose
        """
        caseNumber = int(input(shoppingContent))
        if caseNumber == 2:
            priceExpect = int(input("Please enter price you want:\n"))
        if caseNumber == 0:
            return
        while 1 != 0:
            item = self.getShopOrderList(typeItem, orderType, 1)
            price = int(item[0]["amount"])
            orderId = item[0]["id"]
            if caseNumber == 1:
                if price <= lowestPrice:
                    self.buyItem(orderId)
                    print("Buy successfully")
            if caseNumber == 2:
                if price <= priceExpect:
                    self.buyItem(orderId)
                    print("Buy successfully")
            time.sleep(1)

    def shelling(self, type):
        exceptNumber = [-1, 0, 1, 5, 9, 1018, 1019, 1020]
        typeItem = tableSelect(typeItems, exceptNumber)
        if type == 1:
            orderType = 3
            quantity = 1
        else:
            orderType = 2
            quantity = int(input("Please enter your quantity: "))
        while 1 != 0:
            self.getPriceInMarket(typeItem, orderType)
            shopOrderList = self.getShopOrderList(typeItem, orderType, 1)
            lowestPrice = int(shopOrderList[0]["amount"])
            print(f"The lowest price is {lowestPrice}")
            caseNumber = int(input("1. Shell lowest\n2. Set the price\n"))
            if caseNumber == 1:
                lowestPrice -= 1
                print(f"The lowest price will shell {lowestPrice}")
                self.shellItem(typeItem, quantity, lowestPrice)
                continue
            elif caseNumber == 2:
                price = int(input("Insert your price\n"))
                self.shellItem(typeItem, quantity, price)
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

    def buyItemInDrops(self, orderId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address}

        url = f"https://metamon-api.radiocaca.com/usm-api/official-sale/buy?orderId={orderId}"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        print(json)

    def buyDrops(self):
        helloContent = """
        Official sale 
        1. Purple Potion         - 111
        2. Anti-Fatigue Potion   - 106
        0. Exit
        Please select you want to buy it
        """
        caseNumber = int(input(helloContent))
        numberToBuy = int(input("How much do you want to buy?\n"))
        if caseNumber == 1:
            for i in range(numberToBuy):
                self.buyItemInDrops(111)
            return
        if caseNumber == 2:
            for i in range(numberToBuy):
                self.buyItemInDrops(106)
            return
        if caseNumber == 0:
            return

    def getNftRecord(self, typeItem, dealType, bpNftId=-1, bpOtherId=-1, bpRacaId=-1):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "bpType": typeItem,
            "bpNftId": bpNftId,
            "orderId": -1,
            "bpRacaId": bpRacaId,
            "pageSize": 15,
            "dealType": dealType,
            "bpOtherId": bpOtherId,
            "farmOrderId": -1,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/getNftRecord"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        nftRecords = json.get("data").get("nftRecords")
        bpNftId = json.get("data").get("bpNftId")
        bpOtherId = json.get("data").get("bpOtherId")
        bpRacaId = json.get("data").get("bpRacaId")
        table = PrettyTable()
        table.field_names = ["Type", "Deal", "Deal Num", "Detail", "Time"]
        table.align["Type"] = "l"
        table.align["Deal"] = "l"
        table.align["Deal Num"] = "r"
        for nftRecord in nftRecords:
            table.add_row(
                [
                    typeItems[int(nftRecord["bpType"])],
                    dealTypes[int(nftRecord["dealType"])],
                    nftRecord["dealNum"],
                    nftRecord["detail"],
                    nftRecord["createTime"],
                ]
            )
        print(table)
        return bpNftId, bpOtherId, bpRacaId

    def transactionHistory(self):
        exceptNumber = [1]
        typeItem = tableSelect(typeItems, exceptNumber)
        dealType = tableSelect(dealTypes)
        bpNftId, bpOtherId, bpRacaId = self.getNftRecord(typeItem, dealType)
        helloContent = """
        1. You want to see more
        0. Exit
        Please select you want to choose
        """
        while 1 != 0:
            caseNumber = int(input(helloContent))
            if caseNumber == 1:
                bpNftId, bpOtherId, bpRacaId = self.getNftRecord(
                    typeItem, dealType, bpNftId, bpOtherId, bpRacaId
                )
                continue
            if caseNumber == 0:
                return
