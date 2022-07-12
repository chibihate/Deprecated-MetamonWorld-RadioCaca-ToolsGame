import requests
from prettytable import PrettyTable
import time
import json
import math

exceptNumber = [-1, 0, 1, 5, 12, 13, 14, 1018, 1019, 1020]
typeItems = {
    -1: "All",
    0: "Metamon",
    1: "Metamon Fragments",
    2: "Potion",
    3: "Yellow Diamond",
    4: "Purple Diamond",
    5: "u-RACA",
    6: "Metamon Egg",
    7: "Space Ticket",
    8: "Valhalla",
    9: "N Battle Flag",
    10: "Purple Potion",
    11: "Anti-Fatigue Potion",
    12: "N Stimulant",
    13: "R Stimulant",
    14: "SR Stimulant",
    1004: "Donuts",
    1007: "Spaceship",
    1008: "Rocket",
    1015: "Villa Fragments",
    1016: "Mansion Fragments",
    1017: "Castle Fragments",
    1018: "Villa",
    1019: "Mansion",
    1020: "Castle",
}
dropItems = {
    111: "Purple Potion",
    106: "Anti-Fatigue Potion",
    108: "N Stimulant",
    109: "R Stimulant",
    110: "SR Stimulant",
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

# URLs to make api calls
BASE_URL = "https://metamon-api.radiocaca.com/usm-api"


def tableSelect(types, exceptNumber=[]):
    table = PrettyTable()
    table.field_names = ["Number", "Item"]
    table.align["Number"] = "r"
    table.align["Item"] = "l"
    for numberID in types:
        if numberID in exceptNumber:
            continue
        table.add_row([numberID, types[numberID]])
    print(str(table) + "\nPlease choose number is beyond:")
    while 1 != 0:
        number = int(input())
        if number not in types.keys():
            print("Number is out of range")
            print(str(table) + "\nPlease choose number is beyond again:")
            continue
        elif number in exceptNumber:
            print(f"{types[number]} is not available")
            print(str(table) + "\nPlease choose number is beyond again:")
            continue
        else:
            return number


class MetamonPlayer:
    def __init__(self, address, accessToken):
        self.accessToken = accessToken
        self.headers = {
            "accessToken": self.accessToken,
        }
        self.address = address
        self.payload_address = {"address": self.address}
        self.orderId = -1
        self.orderAmount = ""

    def post_data(self, url, payload):
        return json.loads(
            requests.Session().post(url, data=payload, headers=self.headers).text
        )

    def get_data(self, url, payload):
        return json.loads(
            requests.Session().get(url, data=payload, headers=self.headers).text
        )

    def getMetamonsAtIsland(self):
        """! Get list of metamon at island
        @return List of metamon at island
        """
        ## Payload of API
        payload = {"address": self.address, "orderType": "-1"}
        ## Url of API
        url = f"{BASE_URL}/getWalletPropertyList"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("getWalletPropertyList: " + response["message"])
            return
        return response["data"]["metamonList"]

    def getMetamonsAtLostWorld(self):
        """! Get list of metamon at lost world
        @return List of metamon at lost world
        """
        ## Payload of API
        payload = {"address": self.address, "orderType": "2", "position": 2}
        ## Url of API
        url = f"{BASE_URL}/kingdom/monsterList"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("monsterList: " + response["message"])
            return
        return response["data"]

    def checkBag(self):
        itemsInGame = {}
        urlCheckBag = f"{BASE_URL}/checkBag"
        responseCheckBag = self.post_data(urlCheckBag, self.payload_address)
        if responseCheckBag["code"] != "SUCCESS":
            print("checkBag: " + responseCheckBag["message"])
        itemsInCheckBag = responseCheckBag["data"]["item"]
        for item in itemsInCheckBag:
            if item["bpType"] > 0 and int(item["bpNum"]) > 0:
                itemsInGame[typeItems[int(item["bpType"])]] = item["bpNum"]

        urlSellBag = f"{BASE_URL}//shop-order/sellBag"
        responseSellBag = self.post_data(urlSellBag, self.payload_address)
        if responseSellBag["code"] != "SUCCESS":
            print("sellBag: " + responseSellBag["message"])
        itemsInSellBag = responseSellBag["data"]
        for item in itemsInSellBag:
            itemsInGame[typeItems[int(item["type"])]] = item["bpNum"]

        urlGetBpOther = f"{BASE_URL}/getBpOther"
        payload = {
            "address": self.address,
            "pageSize": 50,
            "bpId": "-1",
            "bpRecordId": "-1",
        }
        responseGetBpOther = self.post_data(urlGetBpOther, payload)
        if responseGetBpOther["code"] != "SUCCESS":
            print("getBpOther: " + responseGetBpOther["message"])
        itemsInGetBpOther = responseGetBpOther["data"]["list"]
        for item in itemsInGetBpOther:
            itemsInGame[item["symbol"]] = item["bpNum"]

        table = PrettyTable()
        table.title = "All items in bag"
        table.field_names = ["Item", "Amount"]
        table.align["Amount"] = "r"
        table.align["Item"] = "l"
        for item, amount in itemsInGame.items():
            table.add_row([item, amount])
        print(table)

    def getShopOrderList(
        self, _typeItem, _orderType, _orderId=-1, _orderAmount="", _pageSize=1
    ):
        payload = {
            "address": self.address,
            "type": _typeItem,
            "orderType": _orderType,
            "orderId": _orderId,
            "pageSize": _pageSize,
            "orderAmount": _orderAmount,
        }
        url = f"{BASE_URL}/shop-order/sellList"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("sellList: " + response["message"])
        return response["data"]["shopOrderList"]

    def getPriceInMarket(
        self, _typeItem, _orderType, _orderId=-1, _orderAmount="", _pageSize=1
    ):
        shopOrderList = self.getShopOrderList(
            _typeItem, _orderType, _orderId, _orderAmount, _pageSize
        )
        indexNumber = 0
        table = PrettyTable()
        table.field_names = ["Index", "Unit", "Num", "Total"]
        table.align["Index"] = "r"
        table.align["Unit"] = "r"
        table.align["Num"] = "r"
        table.align["Total"] = "r"
        orderId = {}
        orderAmount = {}
        for shopOrder in shopOrderList:
            indexNumber += 1
            orderId[indexNumber] = shopOrder["id"]
            orderAmount[indexNumber] = str(shopOrder["amount"])
            table.add_row(
                [
                    indexNumber,
                    shopOrder["amount"],
                    shopOrder["quantity"],
                    shopOrder["totalAmount"],
                ]
            )
        print(table)
        return orderId, orderAmount

    def buyItem(self, orderId):
        payload = {"address": self.address, "orderId": orderId}
        url = f"{BASE_URL}/shop-order/buy"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("buy: " + response["message"])
        else:
            print("Buy items successfully")

    def tranAvgPrice(self, typeItem):
        payload = {"address": self.address, "type": typeItem}
        url = f"{BASE_URL}/shop-order/tranAvgPrice"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("tranAvgPrice: " + response["message"])
            return 0
        else:
            return response["data"]["tranSellPrice"]

    def screenOrder(self, typeItem, quantity, minAmount, maxAmount):
        payload = {
            "address": self.address,
            "type": typeItem,
            "quantity": quantity,
            "minAmount": minAmount,
            "maxAmount": maxAmount,
        }
        url = f"{BASE_URL}/shop-order-quick/screen"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("screen: " + response["message"])
            return 0
        else:
            return response["data"]["id"]

    def buyQuickly(self, typeItem, quantity, minAmount, maxAmount):
        orderId = self.screenOrder(typeItem, quantity, minAmount, maxAmount)
        if orderId == 0 or orderId == None:
            print("There are no eligible orders, please place a new order")
            return
        payload = {"address": self.address, "orderId": orderId}
        url = f"{BASE_URL}/shop-order-quick/buy"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("buy: " + response["message"])
        else:
            print("Buy items successfully")

    def buyOrder(self):
        typeItem = tableSelect(typeItems, exceptNumber)
        self.getPriceInMarket(typeItem, 2, -1, "", 15)
        minPrice = int(self.tranAvgPrice(typeItem))
        if minPrice == 0:
            return
        print(f"Max price >= {minPrice}")
        while 1 != 0:
            maxAmount = int(input("Please fill max price:\n"))
            if maxAmount < minPrice:
                print("Please fill again !!!")
                continue
            else:
                break
        print(f"Min price <= {maxAmount}")
        while 1 != 0:
            minAmount = int(input("Please fill min price:\n"))
            if minAmount > maxAmount:
                print("Please fill again !!!")
                continue
            else:
                break
        while 1 != 0:
            quantity = int(input("Please fill quantity:\n"))
            if quantity <= 0:
                print("Please fill again !!!")
                continue
            else:
                break
        self.buyQuickly(typeItem, quantity, minAmount, maxAmount)

    def shellItem(self, typeItem, quantity, price):
        payload = {
            "address": self.address,
            "type": typeItem,
            "quantity": quantity,
            "amount": price,
            "tokenId": "-1",
        }
        url = f"{BASE_URL}/shop-order/sell"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("sell: " + response["message"])
        else:
            print("Shell items successfully")
        return response["code"]

    def shopping(self):
        typeItem = tableSelect(typeItems, exceptNumber)
        orderType = tableSelect(orderTypes)
        self.orderId = -1
        self.orderAmount = ""
        pageSize = 15
        while 1 != 0:
            orderId, orderAmount = self.getPriceInMarket(
                typeItem, orderType, self.orderId, self.orderAmount, pageSize
            )
            caseNumber = int(
                input(
                    f"1-{pageSize} to buy, 0 to get latest, {(pageSize +1)} to load more\n"
                )
            )
            if caseNumber == 0:
                self.orderId = -1
                self.orderAmount = ""
                continue
            elif caseNumber == (pageSize + 1):
                self.orderId = orderId[pageSize]
                self.orderAmount = orderAmount[pageSize]
                continue
            elif caseNumber in range((pageSize + 1)):
                self.orderId = -1
                self.orderAmount = ""
                self.buyItem(orderId[caseNumber])
                continue
            else:
                return

    def shoppingWithSetPrice(self):
        typeItem = tableSelect(typeItems, exceptNumber)
        orderType = tableSelect(orderTypes)
        self.getPriceInMarket(typeItem, orderType, -1, "", 15)
        item = self.getShopOrderList(typeItem, orderType)
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
            item = self.getShopOrderList(typeItem, orderType)
            price = int(item[0]["amount"])
            orderId = item[0]["id"]
            if caseNumber == 1:
                if price <= lowestPrice:
                    self.buyItem(orderId)
            if caseNumber == 2:
                if price <= priceExpect:
                    self.buyItem(orderId)
            time.sleep(5)

    def shelling(self, type):
        typeItem = tableSelect(typeItems, exceptNumber)
        if type == 1:
            orderType = 3
            quantity = 1
        else:
            orderType = 2
            quantity = int(input("Please enter your quantity: "))
        while 1 != 0:
            self.getPriceInMarket(typeItem, orderType, -1, "", 15)
            shopOrderList = self.getShopOrderList(typeItem, orderType)
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
        payload = {
            "address": self.address,
            "orderId": "-1",
            "pageSize": 20,
        }
        url = f"{BASE_URL}/shop-order/onSaleList"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("onSaleList: " + response["message"])
        return response["data"]["shopOrderList"]

    def getItemsOnSale(self):
        itemOnSale = self.getOnSaleList()
        indexNumber = 0
        table = PrettyTable()
        table.field_names = ["Index", "Item", "Unit", "Num", "Total"]
        table.align["Index"] = "r"
        table.align["Item"] = "l"
        table.align["Unit"] = "r"
        table.align["Num"] = "r"
        table.align["Total"] = "r"
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
        payload = {"address": self.address, "orderId": orderId}
        url = f"{BASE_URL}/shop-order/cancel"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("cancel: " + response["message"])
        else:
            print("Cancel items successfully")

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

    def buyItemInDrops(self, orderId, num):
        payload = {"address": self.address, "orderId": orderId, "num": num}
        url = f"{BASE_URL}/official-sale/buy"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("buy: " + response["message"])
        else:
            print("Buy items successfully")
        return response["code"]

    def listDrops(self):
        payload = {"address": self.address, "pageSize": 50, "orderId": -1}
        url = f"{BASE_URL}/official-sale/list?address={self.address}&pageSize=50&orderId=-1"
        response = self.get_data(url, payload)
        if response["code"] != "SUCCESS":
            print("list: " + response["message"])
            return []
        else:
            return response["data"]["list"]

    def buyDrops(self):
        orderId = tableSelect(dropItems)
        listDrops = self.listDrops()
        if listDrops == []:
            return
        for item in listDrops:
            if int(item["id"]) == int(orderId):
                if item["buyerNum"] == None:
                    buyerNum = 0
                else:
                    buyerNum = int(item["buyerNum"])
                if item["buyerNum"] == item["maxNum"] and item["maxNum"] != None:
                    print("Reach to maximum buy today")
                    return
                if item["maxNum"] != None:
                    if int(item["maxNum"]) <= int(item["limitNum"]):
                        maxQuantity = int(item["maxNum"]) - buyerNum
                    else:
                        maxQuantity = int(item["limitNum"]) - buyerNum
                else:
                    maxQuantity = int(item["limitNum"]) - buyerNum
                print(f"Maximum quantity: {maxQuantity}")
                while 1 != 0:
                    quantity = int(input("Please fill quantity:\n"))
                    if quantity <= 0 or quantity > maxQuantity:
                        print("Please fill again !!!")
                        continue
                    else:
                        self.buyItemInDrops(orderId, quantity)
                        break

    def getNftRecord(self, typeItem, dealType, bpNftId=-1, bpOtherId=-1, bpRacaId=-1):
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
        url = f"{BASE_URL}/getNftRecord"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("getNftRecord: " + response["message"])
        nftRecords = response["data"]["nftRecords"]
        bpNftId = response["data"]["bpNftId"]
        bpOtherId = response["data"]["bpOtherId"]
        bpRacaId = response["data"]["bpRacaId"]
        table = PrettyTable()
        table.field_names = ["Type", "Deal", "Num", "Detail", "Time"]
        table.align["Type"] = "l"
        table.align["Deal"] = "l"
        table.align["Num"] = "r"
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
        1. Get the latest
        2. You want to see more
        0. Exit
        Please select you want to choose
        """
        while 1 != 0:
            caseNumber = int(input(helloContent))
            if caseNumber == 1:
                bpNftId, bpOtherId, bpRacaId = self.getNftRecord(typeItem, dealType)
                continue
            if caseNumber == 2:
                bpNftId, bpOtherId, bpRacaId = self.getNftRecord(
                    typeItem, dealType, bpNftId, bpOtherId, bpRacaId
                )
                continue
            if caseNumber == 0:
                return

    def withdrawFee(self):
        url = f"{BASE_URL}/withdrawFee"
        response = self.post_data(url, self.payload_address)
        if response["code"] != "SUCCESS":
            print("withdrawFee: " + response["message"])
            return
        else:
            return response["data"]

    def setupPassword(self):
        password = int(input("Please input your 6-digits PIN\n"))
        payload = {
            "address": self.address,
            "password": password,
        }
        url = f"{BASE_URL}/owner-setting/verifyPassWord/setup"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("Setup passWord: " + response["message"])
            return
        else:
            return response["code"]

    def changePassword(self):
        oldPassword = int(input("Please input your oldPassword 6-digits PIN:\n"))
        newPassword = int(input("Please input your newPassword 6-digits PIN:\n"))
        payload = {
            "address": self.address,
            "oldPassword": oldPassword,
            "newPassword": newPassword,
        }
        url = f"{BASE_URL}/owner-setting/verifyPassWord/edit"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("Change passWord: " + response["message"])
            return
        else:
            return response["code"]

    def verifyPassWord(self, password):
        payload = {
            "address": self.address,
            "password": password,
        }
        url = f"{BASE_URL}/owner-setting/verifyPassWord"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("verifyPassWord: " + response["message"] + "\n")
            return response["code"]
        else:
            return response["code"]

    def transferOutBySymbol(self, num, fee):
        receiveRACA = num - fee
        payload = {
            "address": self.address,
            "type": 5,
            "tokenIds": "",
            "num": num,
            "rartity": 0,
        }
        url = f"{BASE_URL}/transferOutBySymbol"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("withdraw: " + response["message"])
        else:
            print(f"{receiveRACA} RACA will be received, please check your wallet")

    def withdrawRACA(self):
        withdrawFee = self.withdrawFee()
        fee = int(withdrawFee["fee"])
        limit = int(withdrawFee["limit"])
        minVal = int(withdrawFee["minVal"])
        print(f"withdraw fee is {fee} u-RACA")
        print(f"{minVal} u-RACA <= | You can withdraw | <= {limit} u-RACA")
        password = int(input("Please fill your 6-digits PIN:\n"))
        isVerifyPassword = self.verifyPassWord(password)
        while 1 != 0:
            if isVerifyPassword != "SUCCESS":
                password = int(input("Please fill your 6-digits PIN again:\n"))
                isVerifyPassword = self.verifyPassWord(password)
                continue
            else:
                break

        if isVerifyPassword == "SUCCESS":
            numberRaca = int(
                input("Please fill your number RACA you want to withdraw:\n")
            )
            while 1 != 0:
                if numberRaca < minVal or numberRaca > limit:
                    numberRaca = int(
                        input("Your number is exceed, please fill again:\n")
                    )
                    continue
                else:
                    self.transferOutBySymbol(numberRaca, fee)
                    return

    def calculatingUpScore(self):
        potionNeedToUpgrade = 0
        metamonTotal = 0
        metamonOnIsland = 0
        metamonOnLostWorld = 0
        listMetamonOnLostWorld = self.getMetamonsAtLostWorld()
        listMetamonOnIsland = self.getMetamonsAtIsland()
        if listMetamonOnIsland != []:
            for mtm in listMetamonOnIsland:
                if int(mtm["level"]) == 60:
                    metamonOnIsland += 1
                if int(mtm["sca"]) < 380:
                    potionNeedToUpgrade += 1
        print(f"Amount metamons lv 60 on island: {metamonOnIsland}")
        if listMetamonOnLostWorld != []:
            metamonOnLostWorld = int(len(listMetamonOnLostWorld))
            for mtm in listMetamonOnLostWorld:
                if int(mtm["sca"]) < 380:
                    potionNeedToUpgrade += 1
        print(f"Amount metamons on Lost world: {metamonOnLostWorld}")
        print(f"Potion need to upgrade: {potionNeedToUpgrade}")

        metamonTotal = metamonOnLostWorld + metamonOnIsland
        print(f"Total amount metamons lv 60: {metamonTotal}")
        potionPrice = int(self.getShopOrderList(2, 3)[0]["amount"])
        print(f"Potion price: {potionPrice}")
        pPotionPrice = int(self.getShopOrderList(10, 2)[0]["amount"])
        purplePotionPrice = round(pPotionPrice * 98 / 100)
        print(f"Purple potion after sale: {purplePotionPrice}")
        feeOnLostWorld = metamonOnLostWorld * 200
        print(f"Fee on Lost world: {feeOnLostWorld}")

        potionInBag = 0
        urlCheckBag = f"{BASE_URL}/checkBag"
        responseCheckBag = self.post_data(urlCheckBag, self.payload_address)
        if responseCheckBag["code"] != "SUCCESS":
            print("checkBag: " + responseCheckBag["message"])
        itemsInCheckBag = responseCheckBag["data"]["item"]
        for item in itemsInCheckBag:
            if item["bpType"] == 2:
                potionInBag = int(item["bpNum"])
        print(f"Potions in bag: {potionInBag}")
        potionNeedToBuy = potionNeedToUpgrade - potionInBag
        print(f"Potions need to buy: {potionNeedToBuy}")
        feePotion = potionNeedToBuy * potionPrice
        print(f"Fee for potion: {feePotion}")
        totalSellPurplePotionPrice = metamonTotal * purplePotionPrice
        print(
            f"u-RACA received after selling purple potion: {totalSellPurplePotionPrice}"
        )
        purplePotionNeedToSell = metamonTotal - math.floor(
            (totalSellPurplePotionPrice - feePotion - feeOnLostWorld)
            / purplePotionPrice
        )
        print(f"Total purple potions need to sell: {purplePotionNeedToSell}")

        caseNumber = int(input("1. Todo\n2. Exit\n"))
        if caseNumber != 1:
            return

        print(f"Buy {metamonTotal} purple potions")
        codeBuyPurplePotion = self.buyItemInDrops(111, metamonTotal)
        if codeBuyPurplePotion != "SUCCESS":
            return

        print(f"Shell {purplePotionNeedToSell} purple potions")
        codeShellPurplePotion = self.shellItem(
            10, purplePotionNeedToSell, pPotionPrice - 1
        )
        if codeShellPurplePotion != "SUCCESS":
            return

        print(f"Buy {potionNeedToBuy} purple potions")
        self.buyQuickly(2, potionNeedToBuy, 1, potionPrice * 2)
