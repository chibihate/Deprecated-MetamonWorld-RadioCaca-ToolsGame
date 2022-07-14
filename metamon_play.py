import json
import requests
from prettytable import PrettyTable
import time
import math
import os  # disable when you don't use .env
from dotenv import load_dotenv  # disable when you don't use .env

load_dotenv()  # disable when you don't use .env
# clear os.getenv if you don't use .env
ADDRESS_WALLET = os.getenv("ADDRESS_WALLET") or "your_ADDRESS_WALLET"
SIGN_WALLET = os.getenv("SIGN_WALLET") or "your_SIGN_WALLET"
MSG_WALLET = os.getenv("MSG_WALLET") or "your_MSG_WALLET"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or ""
HAVE_DOTENV = 1  # 0 if you don't use
HAVE_2FA = 1  # 0 if you don't use

# URLs to make api calls
BASE_URL = "https://metamon-api.radiocaca.com/usm-api"

# Global constants
## The attributes of metamon
attrType = {
    "1": "luck",
    "2": "courage",
    "3": "wisdom",
    "4": "size",
    "5": "stealth",
}

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
    def __init__(self, address, sign, msg):
        self.accessToken = ACCESS_TOKEN
        self.address = address
        self.sign = sign
        self.msg = msg
        self.headers = {
            "accessToken": self.accessToken,
        }
        self.payload_address = {"address": self.address}
        self.payload_login = {
            "address": self.address,
            "sign": self.sign,
            "msg": self.msg,
            "network": "1",
            "clientType": "MetaMask",
        }
        self.initAccessToken()
        ## Initialization fragment numbers, numbers of battle win and lose
        # when we start battle in Island
        self.fragmentNum = 0
        self.battleWin = 0
        self.battleLose = 0
        self.status = True
        self.id = 0
        self.level = 0
        self.exp = 0
        self.expMax = 0
        self.hi = 0
        self.rarity = "N"
        self.orderId = -1
        self.orderAmount = ""

    def post_data(self, url, payload, isData=True):
        if isData != True:
            return json.loads(
                requests.Session().post(url, json=payload, headers=self.headers).text
            )
        else:
            return json.loads(
                requests.Session().post(url, data=payload, headers=self.headers).text
            )

    def get_data(self, url, payload):
        return json.loads(
            requests.Session().get(url, data=payload, headers=self.headers).text
        )

    def changeAccessTokenInSetting(self):
        envFile = open(".env")
        contentInEnvFile = envFile.readlines()
        envFile.close()

        contentInEnvFile[3] = "ACCESS_TOKEN = " + str(self.accessToken) + "\n"
        envFile = open(".env", "w")
        newContentInEnvFile = "".join(contentInEnvFile)
        envFile.write(newContentInEnvFile)
        envFile.close()

    def getInfo(self):
        url = f"{BASE_URL}/owner-setting/info"
        response = self.post_data(url, self.payload_address)
        return response["code"]

    def getAccessToken(self):
        """Obtain token for game session to perform battles and other actions"""
        url = f"{BASE_URL}/login"
        response = self.post_data(url, self.payload_login)
        if response["code"] != "SUCCESS":
            print("login: " + response["message"])
            exit()
        else:
            self.accessToken = response["data"]["accessToken"]
            self.headers = {
                "accessToken": self.accessToken,
            }

    def getLoginCode(self):
        url = f"{BASE_URL}/owner-setting/email/sendLoginCode"
        response = self.post_data(url, self.payload_address)
        if response["code"] != "SUCCESS":
            print("sendLoginCode: " + response["message"])
            exit()
        else:
            print("Code is sending to your email. Kindly check")

    def verifyLoginCode(self, loginCode):
        payload = {"address": self.address, "code": loginCode}
        url = f"{BASE_URL}/owner-setting/email/verifyLoginCode"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("verifyLoginCode: " + response["message"])
            return
        return response["code"]

    def initAccessToken(self):
        if HAVE_DOTENV == 1:
            if self.getInfo() != "SUCCESS":
                if HAVE_2FA == 0:
                    self.getAccessToken()
                    self.changeAccessTokenInSetting()
                else:
                    self.getAccessToken()
                    self.changeAccessTokenInSetting()
                    self.getLoginCode()
                    while 1 != 0:
                        print("Please fill your code:")
                        code = self.verifyLoginCode(loginCode=input())
                        if code != "SUCCESS":
                            continue
                        else:
                            print("Email is verified")
                            return
            else:
                return
        else:
            if HAVE_2FA == 0:
                self.getAccessToken()
            else:
                self.getAccessToken()
                self.getLoginCode()
                while 1 != 0:
                    print("Please fill your code:")
                    code = self.verifyLoginCode(loginCode=input())
                    if code != "SUCCESS":
                        continue
                    else:
                        print("Email is verified")
                        return

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

    def showAllMetamons(self):
        """! Show off all metamons"""
        metamonList = []
        ## Init metamons of Island via getMetamonsAtIsland()
        metamonsAtIsland = self.getMetamonsAtIsland()
        ## Init metamons of Lost world via getMetamonsAtLostWorld()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        ## Init all metamons
        metamonList = metamonList + metamonsAtLostWorld
        metamonList = metamonList + metamonsAtIsland
        ## Creata a table with these field names
        table = PrettyTable()
        table.field_names = [
            "ID",
            "Rare",
            "Lv",
            "Scare",
            "Luck",
            "Cour",
            "Wis",
            "Size",
            "Steal",
        ]
        ## Align of these field names
        table.align["Rare"] = "r"
        table.align["Lv"] = "r"
        table.align["Luck"] = "r"
        table.align["Cour"] = "r"
        table.align["Wis"] = "r"
        table.align["Size"] = "r"
        table.align["Steal"] = "r"
        ## Loop in each metamon of list, add them to these field names
        for metamon in metamonList:
            table.add_row(
                [
                    metamon["tokenId"],
                    metamon["rarity"],
                    metamon["level"],
                    metamon["sca"],
                    metamon["luk"],
                    metamon["crg"],
                    metamon["inte"],
                    metamon["con"],
                    metamon["inv"],
                ]
            )
        ## Show off the table
        print(table)

    def addAttrNeedAsset(self, metamonId, type):
        """! Check the upgrade ability of metamon
        @detail Potion available and attribue index is not full
        @param metamonId The id of metamon inside Metamon Game
        @param type The type of attribute you want to upgrade
        @return The status of the request
        """
        ## Payload of API
        payload = {
            "address": self.address,
            "nftId": metamonId,
            "attrType": type,
        }
        ## URL of API
        url = f"{BASE_URL}/addAttrNeedAsset"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print(attrType[type] + ": " + response["message"])
            return
        return response["code"]

    def addAttr(self, metamonId, type):
        """! Upgrade the attribute metamon
        @param metamonId The id of metamon inside Metamon Game
        @param type The type of attribute you want to upgrade
        """
        ## Payload of API
        payload = {
            "address": self.address,
            "nftId": metamonId,
            "attrType": type,
        }
        ## URL of API
        url = f"{BASE_URL}/addAttr"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("addAttr: " + response["message"])
            return
        else:
            upperNum = response["data"]["upperNum"]
            title = response["data"]["title"]
            upperMsg = response["data"]["upperMsg"]
            sca = int(response["data"]["sca"])
            upperSca = int(response["data"]["upperSca"])
            print(f"{title}: {upperMsg}")
            if sca != upperSca:
                print(f"{sca} + {upperNum} --> {upperSca}")

    def resetMonster(self, metamonId):
        """! Reset exp of the metamon lv 60 when she travel to island
        @param metamonId The id of metamon inside Metamon Game
        """
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = f"{BASE_URL}/resetMonster"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        ## Show off the notice when status when the status is "SUCCESS" or not
        if response["code"] != "SUCCESS":
            print("resetMonster: " + response["message"])
            return
        else:
            print("Reseted monster successfully")

    def updateMonster(self, metamonId):
        """! Up level of the metamon
        @param metamonId The id of metamon inside Metamon Game
        """
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = f"{BASE_URL}/updateMonster"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        ## Show off the notice when status when the status is "SUCCESS" or not
        if response["code"] != "SUCCESS":
            print("updateMonster: " + response["message"])
            return
        else:
            print("Updated monster successfully")

    def addHealthy(self, metamonId):
        """! Add a health index of the metamon
        @param metamonId The id of metamon inside Metamon Game
        """
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = f"{BASE_URL}/addHealthy"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        ## Show off the notice when status when the status is "SUCCESS" or not
        if response["code"] != "SUCCESS":
            print("addHealthy: " + response["message"])
            return
        else:
            print("Add healthy monster successfully")

    def addFatigueNeedAsset(self, metamonId):
        """! Check ability recover healthy index
        @detail Check anti-fatigue potion is available and a healthy index
        of the metamon below 100 or not
        @param metamonId The id of metamon inside Metamon Game
        @return The status of function
        """
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = f"{BASE_URL}/addFatigueNeedAsset"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("addFatigueNeedAsset: " + response["message"])
            return
        return response["code"]

    def autoAddAttrMetamon(self, metamon):
        print("\n" + metamon["tokenId"])
        if metamon["luk"] != metamon["lukMax"]:
            print("Luck")
            if self.addAttrNeedAsset(metamon["id"], "1") != "SUCCESS":
                return
            else:
                self.addAttr(metamon["id"], "1")
                return
        if metamon["crg"] != metamon["crgMax"]:
            print("Courage")
            if self.addAttrNeedAsset(metamon["id"], "2") != "SUCCESS":
                return
            else:
                self.addAttr(metamon["id"], "2")
                return
        if metamon["inv"] != metamon["invMax"]:
            print("Stealth")
            if self.addAttrNeedAsset(metamon["id"], "5") != "SUCCESS":
                return
            else:
                self.addAttr(metamon["id"], "5")
                return
        if metamon["inte"] != metamon["inteMax"]:
            print("Wisdom")
            if self.addAttrNeedAsset(metamon["id"], "3") != "SUCCESS":
                return
            else:
                self.addAttr(metamon["id"], "3")
                return
        if metamon["con"] != metamon["conMax"]:
            print("Size")
            if self.addAttrNeedAsset(metamon["id"], "4") != "SUCCESS":
                return
            else:
                self.addAttr(metamon["id"], "4")
                return

    def autoAddAttrAllMetamon(self):
        metamonList = []
        metamonsAtIsland = self.getMetamonsAtIsland()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        metamonList = metamonList + metamonsAtIsland
        metamonList = metamonList + metamonsAtLostWorld
        print("\nAdd attr follow Luck > Courage > Stealth > Wisdom > Size")
        for metamon in metamonList:
            if int(metamon["sca"]) >= 380:
                continue
            time.sleep(5)
            self.autoAddAttrMetamon(metamon)

    def autoAddAttrMetamonAbove380(self):
        purplePotion = self.checkOnlyBag(10)
        loopCount = 0
        if purplePotion == 0:
            print("Out of purple potions")
            return
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        metamonList = {}
        self.showAllMetamons()
        for metamon in metamonsAtLostWorld:
            metamonList[int(metamon["tokenId"])] = metamon
        # print(metamonList)
        while 1 != 0:
            number = int(input("Please fill number ID metamon to add:\n"))
            if number not in metamonList.keys():
                print("Number ID metamon is not correct in your team.")
                continue
            else:
                break
        if purplePotion >= 5:
            loopCount = 5
        else:
            loopCount = purplePotion
        for i in range(loopCount):
            self.autoAddAttrMetamon(metamonList[number])

    def addAttrAllMetamon(self):
        """! Add attribute for all metamons"""
        helloContent = """
        1. Luck
        2. Courage
        3. Wisdom
        4. Size
        5. Stealth
        Please choose attr to add all metamons
        """
        ## Get all metamons from Island and Lost world via
        ## method getMetamonsAtIsland and getMetamonsAtLostWorld
        metamonList = []
        metamonsAtIsland = self.getMetamonsAtIsland()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        metamonList = metamonList + metamonsAtIsland
        metamonList = metamonList + metamonsAtLostWorld
        caseNumber = input(helloContent)
        ## Loop through all metamons, first check ability to add attribute
        ## of the memontamon, if it is "SUCCESS", do add attribute to the metamon
        metamonNumbers = 0
        for metamon in metamonList:
            print("\n" + metamon["tokenId"])
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)
                metamonNumbers += 1
            time.sleep(5)
        print(f"Total metamons are add attr: {metamonNumbers}")

    def getBattelObjects(self, metamonId, level):
        """! Get battle objects in the battle fields
        @param metamonId The id of metamon inside Metamon Game
        @param level The level of the battle fields
        @return The list of battle objects in the battle field
        """
        ## Payload of API
        payload = {
            "address": self.address,
            "metamonId": metamonId,
            "front": level,
        }
        ## URL of API
        url = f"{BASE_URL}/getBattelObjects"
        ## Get data from API via POST method
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("getBattelObjects: " + response["message"])
            return
        return response["data"]["objects"]

    def getMinScareBattleObject(self, metamonId, level):
        """! Get the mininum score battle object in the battle fields
        @param metamonId The id of metamon inside Metamon Game
        @param level The level of the battle fields
        @return The list of mininum score battle object in the battle field
        """
        ## Init the maximum score
        scareScore = 650
        ## Get battle objects via method getBattelObjects
        battelObjects = self.getBattelObjects(metamonId, level)
        ## Loop through battle objects, find the metamon with minimum "sca"
        for battleObject in battelObjects:
            if int(battleObject["sca"]) < int(scareScore):
                scareScore = int(battleObject["sca"])
                minScareBattleObject = battleObject
        return minScareBattleObject

    def getMinScareBattleObjectAllLevel(self, metamonId, metamonLevel):
        minScareBattleObjects = []
        scareScore = 650
        level = 0
        levelBattleObject = 0
        numberBattleField = 0
        if 21 <= int(metamonLevel) <= 40:
            numberBattleField = 2
        elif 41 <= int(metamonLevel) <= 60:
            numberBattleField = 3
        else:
            numberBattleField = 1
        for i in range(int(numberBattleField)):
            minScareBattleObjects.append(self.getMinScareBattleObject(metamonId, i + 1))
        for battleObject in minScareBattleObjects:
            level += 1
            if int(battleObject["sca"]) < int(scareScore):
                scareScore = int(battleObject["sca"])
                minScareBattleObjectAllLevel = battleObject["id"]
                levelBattleObject = level
        print(f"Battle object has scare score {scareScore}")
        return minScareBattleObjectAllLevel, levelBattleObject

    def startBattle(self, myMonId, battleMonId, battleLevel):
        payload = {
            "address": self.address,
            "monsterA": myMonId,
            "monsterB": battleMonId,
            "battleLevel": battleLevel,
        }
        url = f"{BASE_URL}/startBattle"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("startBattle: " + response["message"])
            return
        self.fragmentNum += response["data"]["bpFragmentNum"]
        if response["data"]["challengeExp"] == 5:
            self.battleWin += 1
            return True
        else:
            self.battleLose += 1
            return False

    def checkAbility(self):
        if self.level == 60 and self.exp >= 395:
            potion = self.checkOnlyBag(2)
            if potion == 0:
                self.buyQuickly(2, 1, 1, 1000)
            self.resetMonster(self.id)
            self.exp = 0
        if self.level == 59 and self.exp == 600:
            if self.rarity == "N":
                itemNeedToBuy = self.checkOnlyBag(2)
                if itemNeedToBuy == 0:
                    self.buyQuickly(2, 1, 1, 1000)
            if self.rarity == "R":
                itemNeedToBuy = self.checkOnlyBag(3)
                if itemNeedToBuy == 0:
                    self.buyQuickly(3, 1, 1, 100000)
            if self.rarity == "SR" or self.rarity == "SSR":
                itemNeedToBuy = self.checkOnlyBag(4)
                if itemNeedToBuy == 0:
                    self.buyQuickly(4, 1, 1, 1000000)
            self.updateMonster(self.id)
            self.level = 60
            self.exp = 0
            self.status = False
        if self.level != 59 and self.exp >= self.expMax:
            if self.rarity == "N":
                itemNeedToBuy = self.checkOnlyBag(2)
                if itemNeedToBuy == 0:
                    self.buyQuickly(2, 1, 1, 1000)
            if self.rarity == "R":
                itemNeedToBuy = self.checkOnlyBag(3)
                if itemNeedToBuy == 0:
                    self.buyQuickly(3, 1, 1, 100000)
            if self.rarity == "SR" or self.rarity == "SSR":
                itemNeedToBuy = self.checkOnlyBag(4)
                if itemNeedToBuy == 0:
                    self.buyQuickly(4, 1, 1, 1000000)
            self.updateMonster(self.id)
            self.exp = 0
            self.level += 1
        if self.hi <= 90 and self.addFatigueNeedAsset(self.id) == "SUCCESS":
            hiPotion = self.checkOnlyBag(11)
            if hiPotion == 0:
                code = self.buyItemInDrops(106, 1)
                if code == "SUCCESS":
                    return
                self.buyQuickly(11, 1, 1, 10000)
            self.addHealthy(self.id)
            self.hi += 10

    def battleIsland(self, mode):
        metamonAtIslandList = self.getMetamonsAtIsland()
        for metamon in metamonAtIslandList:
            tear = int(metamon["tear"])
            if tear == 0:
                continue
            self.status = True
            tokenId = metamon["tokenId"]
            self.id = metamon["id"]
            self.level = int(metamon["level"])
            self.exp = int(metamon["exp"])
            self.expMax = int(metamon["expMax"])
            self.hi = int(metamon["healthy"])
            self.rarity = metamon["rarity"]
            print(
                f"Start {tokenId} with level:{self.level}, exp:{self.exp}, HI:{self.hi} and {tear} turns"
            )
            # Check ability of metamon before start battle
            self.checkAbility()
            # Get the mininum score scare object battle
            if mode == 1:
                (
                    minScareBattleObjectAllLevel,
                    levelBattleObject,
                ) = self.getMinScareBattleObjectAllLevel(self.id, self.level)
            elif mode == 2:
                levelBattleObject = "1"
                minScareBattleObjectAllLevel = "883061"
            elif mode == 3:
                levelBattleObject = "1"
                minScareBattleObjectAllLevel = "442383"
            else:
                levelBattleObject = "1"
                minScareBattleObjectAllLevel = "214650"

            for i in range(tear):
                # Update ability of metamon
                self.checkAbility()
                if self.status == False:  # This case for metamon lv 59 -> 60
                    break
                statusBattle = self.startBattle(
                    self.id, minScareBattleObjectAllLevel, levelBattleObject
                )
                if statusBattle == True:
                    self.exp += 5
                else:
                    self.exp += 3
            print(f"End {tokenId}")
            if self.status == False:  # This case for metamon lv 59 -> 60
                continue
        time.sleep(5)

    def startBattleIsland(self, mode):
        for i in range(3):
            self.battleIsland(mode)
        print(f"Total egg fragments: {self.fragmentNum}")
        print(f"Total win battle: {self.battleWin}")
        print(f"Total lose battel: {self.battleLose}")
        rateWin = 0
        if self.fragmentNum != 0:
            rateWin = self.battleWin / (self.battleLose + self.battleWin) * 100
        print(f"Rate: {round(rateWin)}%")
        return 0

    def mintEgg(self):
        url = f"{BASE_URL}/composeMonsterEgg"
        response = self.post_data(url, self.payload_address)
        if response["code"] != "SUCCESS":
            print("composeMonsterEgg: " + response["message"])
            return
        print(f"Minted eggs are success")

    def getScoreGroupInKingdom(self, thresholdSca, isDev=True):
        payload = {
            "address": self.address,
            "page": 1,
            "pageSize": 100,
            "orderField": "monsterNum",
        }
        url = f"{BASE_URL}/kingdom/teamList"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("teamList: " + response["message"])
            return
        squadList = response["data"]["list"]
        table = PrettyTable()
        table.field_names = ["Index", "Group", "Score", "Mons", "Lock", "Rank"]
        table.align["Index"] = "r"
        table.align["Group"] = "l"
        table.align["Score"] = "r"
        table.align["Mons"] = "r"
        table.align["Lock"] = "l"
        table.align["Rank"] = "l"
        indexSquad = 0
        idSquadList = {}
        monSquadList = {}
        scaSquadList = {}
        lockSquadList = {}
        for squad in squadList:
            if isDev == True:
                if squad["symbol"] != "":
                    continue
            if (
                int(squad["monsterNum"]) >= 100
                and int(squad["monsterScaThreshold"]) <= thresholdSca
            ):
                indexSquad += 1
                idSquadList[indexSquad] = int(squad["id"])
                monSquadList[indexSquad] = int(squad["monsterNum"])
                scaSquadList[indexSquad] = int(squad["averageSca"])
                lockSquadList[indexSquad] = squad["lockTeam"]
                table.add_row(
                    [
                        indexSquad,
                        squad["name"],
                        squad["averageSca"],
                        squad["monsterNum"],
                        squad["lockTeam"],
                        squad["ranking"],
                    ]
                )
        print(table)
        return idSquadList, monSquadList, scaSquadList, lockSquadList

    def getMetamonIsReadyInKingdom(self):
        metamons = self.getMetamonsAtLostWorld()
        metamonsList = []
        sca = 650
        for metamon in metamons:
            if str(metamon["kingdomLock"]).lower() == "false":
                metamonsList.append({"nftId": metamon["id"]})
                if int(metamon["sca"]) < sca:
                    sca = int(metamon["sca"])
        return metamonsList, sca

    def checkPwd(self, teamId, invitationCode):
        payload = {
            "address": self.address,
            "teamId": teamId,
            "joinPassword": invitationCode,
        }
        url = f"{BASE_URL}/kingdom/checkPwd"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("checkPwd: " + response["message"])
        return response["code"]

    def joinLostWorldManual(self, metamons, sca, isDev=True):
        print(f"We have {len(metamons)} metamons are available")
        while 1 != 0:
            (
                idSquadList,
                monSquadList,
                scaSquadList,
                lockSquadList,
            ) = self.getScoreGroupInKingdom(sca, isDev)
            caseNumber = int(
                input(
                    f"Select number in range {len(idSquadList)} to join - 0 to refresh\n"
                )
            )
            if caseNumber == 0:
                continue
            elif caseNumber in range(len(idSquadList) + 1):
                if lockSquadList[caseNumber] == False:
                    self.teamJoin(idSquadList[caseNumber], metamons)
                    continue
                else:
                    passToJoin = input("Please fill invitationCode:\n")
                    code = self.checkPwd(idSquadList[caseNumber], passToJoin)
                    if code != "SUCCESS":
                        continue
                    self.teamJoin(idSquadList[caseNumber], metamons, passToJoin)
                    continue
            else:
                return

    def joinLostWorldAutomatic(
        self, _scoreAverage=650, _monsterNum=900, metamons=[], sca=650
    ):
        print(f"We have {len(metamons)} metamons are available")
        while 1 != 0:
            (
                idSquadList,
                monSquadList,
                scaSquadList,
                lockSquadList,
            ) = self.getScoreGroupInKingdom(sca)

            for i in range(len(idSquadList)):
                if (monSquadList[i + 1] >= _monsterNum) and (
                    scaSquadList[i + 1] >= _scoreAverage
                ):
                    print(
                        f"Found the squad as your demand with score average is {_scoreAverage} and monster number is {_monsterNum}"
                    )
                    self.teamJoin(idSquadList[i + 1], metamons)
                    return
            time.sleep(10)

    def teamJoin(self, teamId, metamons, invitationCode=""):
        if invitationCode == "":
            payload = {
                "address": self.address,
                "teamId": teamId,
                "metamons": metamons,
            }
        else:
            payload = {
                "address": self.address,
                "teamId": teamId,
                "metamons": metamons,
                "joinPassword": invitationCode,
            }
        url = f"{BASE_URL}/kingdom/teamJoin?address={self.address}"
        response = self.post_data(url, payload, False)
        if response["code"] != "SUCCESS":
            print("teamJoin: " + response["message"])

    def joinTheBestSquad(self):
        joinSquadContent = """
        1. Manual - Dev Legion
        2. Manual - Not Dev Legion
        3. Automatic
        Please select you want to choose
        """
        metamons, sca = self.getMetamonIsReadyInKingdom()
        if metamons == []:
            print("No metamons are available")
            return
        caseNumber = int(input(joinSquadContent))
        if caseNumber == 2:
            scoreAverage = int(input("Please enter your score average:\n"))
            monsterNum = int(input("Please enter your monster number:\n"))
        while 1 != 0:
            metamons, sca = self.getMetamonIsReadyInKingdom()
            if metamons == []:
                print("No metamons are available")
                return
            if caseNumber == 1:
                self.joinLostWorldManual(metamons, sca)
                continue
            if caseNumber == 2:
                self.joinLostWorldManual(metamons, sca, False)
                continue
            if caseNumber == 3:
                self.joinLostWorldAutomatic(scoreAverage, monsterNum, metamons, sca)
                continue

    def battleRecord(self):
        payload = {"address": self.address, "pageSize": 10, "battleId": -1}
        url = f"{BASE_URL}/kingdom/battleRecord"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("battleRecord: " + response["message"])
            return
        battleRecordDetails = response["data"]["battleRecordDetails"]
        table = PrettyTable()
        table.field_names = ["Date", "Monsters", "Valhalla", "Status"]
        table.align["Monsters"] = "r"
        table.align["Valhalla"] = "r"
        table.align["Status"] = "l"
        for battle in battleRecordDetails:
            statusRecord = ""
            if int(battle["winStatus"]) == 1:
                statusRecord = "Win"
            else:
                statusRecord = "Lose"
            table.add_row(
                [
                    battle["startTime"],
                    battle["monsterNum"],
                    battle["myMerit"],
                    statusRecord,
                ]
            )
        print(table)

    def getMyTeams(self):
        url = f"{BASE_URL}/kingdom/myTeams"
        response = self.post_data(url, self.payload_address)
        if response["code"] != "SUCCESS":
            print("myTeams: " + response["message"])
            return
        battles = response["data"]
        table = PrettyTable()
        table.field_names = [
            "Mons",
            "Sca",
            "Team",
            "R",
            "Unlock date",
        ]
        table.align["Mons"] = "r"
        table.align["Sca"] = "r"
        table.align["R"] = "r"
        table.align["Team"] = "r"
        for battle in battles:
            myAverage = round(int(battle["mytotalSca"]) / int(battle["myMonsterNum"]))
            table.add_row(
                [
                    battle["myMonsterNum"],
                    myAverage,
                    battle["averageSca"],
                    battle["monsterNumRarity"],
                    battle["unlockDate"],
                ]
            )
        print(table)

    def checkOnlyBag(self, itemBeChecked):
        amountItemBeChecked = 0
        urlCheckBag = f"{BASE_URL}/checkBag"
        responseCheckBag = self.post_data(urlCheckBag, self.payload_address)
        if responseCheckBag["code"] != "SUCCESS":
            print("checkBag: " + responseCheckBag["message"])
        itemsInCheckBag = responseCheckBag["data"]["item"]
        for item in itemsInCheckBag:
            if item["bpType"] == itemBeChecked:
                amountItemBeChecked = int(item["bpNum"])
        return amountItemBeChecked

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

    def listDrops(self):
        payload = {"address": self.address, "pageSize": 50, "orderId": -1}
        url = f"{BASE_URL}/official-sale/list?address={self.address}&pageSize=50&orderId=-1"
        response = self.get_data(url, payload)
        if response["code"] != "SUCCESS":
            print("list: " + response["message"])
            return []
        else:
            return response["data"]["list"]

    def buyItemInDrops(self, orderId, num):
        payload = {"address": self.address, "orderId": orderId, "num": num}
        url = f"{BASE_URL}/official-sale/buy"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("buy: " + response["message"])
        else:
            print("Buy items successfully")
        return response["code"]

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

        print(f"Buy {potionNeedToBuy} potions")
        self.buyQuickly(2, potionNeedToBuy, 1, potionPrice * 2)

    def playGame(self):
        helloContent = """
        1. Battle in Island
        2. Mint eggs
        3. Show all metamons
        4. Up attribute monsters   
        5. Join the best squad in Lost world
        6. Battle record in Lost world
        7. Get status my teams in Lost world
        0. Exit
        Please select you want to choose
        """
        addAttrContent = """
        1. Manual - All metamons
        2. Automatic - All metamons
        3. Automatic - Specific metamon above 380
        0. Exit
        Please select you want to choose
        """
        battleContent = """
        1. Auto select the lowest scare
        2. Quick battle object - 883061
        3. Quick battle object - 442383
        4. Quick battle object - 214650
        0. Exit
        Please select you want to choose
        """
        while 1 != 0:
            caseNumber = int(input(helloContent))
            if caseNumber == 1:
                caseNumber = int(input(battleContent))
                if caseNumber == 1:
                    self.startBattleIsland(1)
                    continue
                if caseNumber == 2:
                    self.startBattleIsland(2)
                    continue
                if caseNumber == 3:
                    self.startBattleIsland(3)
                    continue
                if caseNumber == 4:
                    self.startBattleIsland(4)
                    continue
                if caseNumber == 0:
                    continue
            if caseNumber == 2:
                self.mintEgg()
            if caseNumber == 3:
                self.showAllMetamons()
            if caseNumber == 4:
                caseNumber = int(input(addAttrContent))
                if caseNumber == 1:
                    self.addAttrAllMetamon()
                    continue
                if caseNumber == 2:
                    self.autoAddAttrAllMetamon()
                    continue
                if caseNumber == 3:
                    self.autoAddAttrMetamonAbove380()
                    continue
                if caseNumber == 0:
                    continue
            if caseNumber == 5:
                self.joinTheBestSquad()
            if caseNumber == 6:
                self.battleRecord()
            if caseNumber == 7:
                self.getMyTeams()
            if caseNumber == 0:
                return

    def marketGame(self):
        helloContent = """
        1. Check bag
        2. Shopping
        3. Shelling
        4. Canceling
        5. Buy item in drops
        6. Transaction history
        7. Withdraw
        8. Calculating up score
        0. Exit
        Please select you want to choose
        """
        shoppingContent = """
        1. Manual
        2. Automatic
        3. Order
        0. Exit
        Please select you want to choose
        """
        shellingContent = """
        1. Unit
        2. Bulks
        0. Exit
        Please select you want to choose
        """
        while 1 != 0:
            caseNumber = int(input(helloContent))
            if caseNumber == 1:
                self.checkBag()
            if caseNumber == 2:
                caseNumber = int(input(shoppingContent))
                if caseNumber == 1:
                    self.shopping()
                    continue
                if caseNumber == 2:
                    self.shoppingWithSetPrice()
                    continue
                if caseNumber == 3:
                    self.buyOrder()
                    continue
                if caseNumber == 0:
                    continue
            if caseNumber == 3:
                caseNumber = int(input(shellingContent))
                if caseNumber == 1:
                    self.shelling(caseNumber)
                    continue
                if caseNumber == 2:
                    self.shelling(caseNumber)
                    continue
                if caseNumber == 0:
                    continue
            if caseNumber == 4:
                self.canceling()
            if caseNumber == 5:
                self.buyDrops()
            if caseNumber == 6:
                self.transactionHistory()
            if caseNumber == 7:
                self.withdrawRACA()
            if caseNumber == 8:
                self.calculatingUpScore()
            if caseNumber == 0:
                return


if __name__ == "__main__":
    helloContent = """
    1. Play game
    2. Market game
    0. Exit
    Please select you want to choose
    """
    mtm = MetamonPlayer(address=ADDRESS_WALLET, sign=SIGN_WALLET, msg=MSG_WALLET)
    while 1 != 0:
        caseNumber = int(input(helloContent))
        if caseNumber == 1:
            mtm.playGame()
        if caseNumber == 2:
            mtm.marketGame()
        if caseNumber == 0:
            exit()
