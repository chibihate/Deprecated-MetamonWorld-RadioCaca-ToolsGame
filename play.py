import requests
from prettytable import PrettyTable
import time
import json

# Global constants
## The attributes of metamon
attrType = {
    "1": "luck",
    "2": "courage",
    "3": "wisdom",
    "4": "size",
    "5": "stealth",
}
# URLs to make api calls
BASE_URL = "https://metamon-api.radiocaca.com/usm-api"


class MetamonPlayer:
    def __init__(self, address, accessToken):
        """! The MetamonPlayer base class initializer

        @param address The address of wallet connect to Metamon Game
        @param accessToken The accessToken of wallet connect to Metamon Game
        """
        ## The accessToken of wallet
        self.accessToken = accessToken
        self.headers = {
            "accessToken": self.accessToken,
        }
        ## The address of wallet
        self.address = address
        ## Initialization fragment numbers, numbers of battle win and lose
        # when we start battle in Island
        self.fragmentNum = 0
        self.battleWin = 0
        self.battleLose = 0
        self.status = True
        self.payload_address = {"address": self.address}
        self.id = 0
        self.level = 0
        self.exp = 0
        self.expMax = 0
        self.hi = 0
        self.rarity = "N"

    def post_data(self, url, payload, isData=True):
        if isData != True:
            return json.loads(
                requests.Session().post(url, json=payload, headers=self.headers).text
            )
        else:
            return json.loads(
                requests.Session().post(url, data=payload, headers=self.headers).text
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
            "Exp",
            "Luck",
            "Cour",
            "Wis",
            "Size",
            "Steal",
            "HI",
            "Race",
            "Unlock Date",
        ]
        ## Align of these field names
        table.align["Rare"] = "r"
        table.align["Lv"] = "r"
        table.align["Exp"] = "r"
        table.align["Luck"] = "r"
        table.align["Cour"] = "r"
        table.align["Wis"] = "r"
        table.align["Size"] = "r"
        table.align["Steal"] = "r"
        table.align["HI"] = "r"
        table.align["Race"] = "l"
        ## Loop in each metamon of list, add them to these field names
        for metamon in metamonList:
            table.add_row(
                [
                    metamon["tokenId"],
                    metamon["rarity"],
                    metamon["level"],
                    metamon["sca"],
                    metamon["exp"],
                    metamon["luk"],
                    metamon["crg"],
                    metamon["inte"],
                    metamon["con"],
                    metamon["inv"],
                    metamon["healthy"],
                    metamon["race"],
                    metamon["kingdomUnLockDate"],
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

    def autoAddAttrAllMetamon(self):
        metamonList = []
        metamonsAtIsland = self.getMetamonsAtIsland()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        metamonList = metamonList + metamonsAtIsland
        metamonList = metamonList + metamonsAtLostWorld
        print("\nAdd attr follow Luck > Courage > Stealth > Wisdom > Size")
        for metamon in metamonList:
            print("\n" + metamon["tokenId"])
            time.sleep(5)
            if metamon["luk"] != metamon["lukMax"]:
                print("Luck")
                if self.addAttrNeedAsset(metamon["id"], "1") != "SUCCESS":
                    continue
                else:
                    self.addAttr(metamon["id"], "1")
                    continue
            if metamon["crg"] != metamon["crgMax"]:
                print("Courage")
                if self.addAttrNeedAsset(metamon["id"], "2") != "SUCCESS":
                    continue
                else:
                    self.addAttr(metamon["id"], "2")
                    continue
            if metamon["inv"] != metamon["invMax"]:
                print("Stealth")
                if self.addAttrNeedAsset(metamon["id"], "5") != "SUCCESS":
                    continue
                else:
                    self.addAttr(metamon["id"], "5")
                    continue
            if metamon["inte"] != metamon["inteMax"]:
                print("Wisdom")
                if self.addAttrNeedAsset(metamon["id"], "3") != "SUCCESS":
                    continue
                else:
                    self.addAttr(metamon["id"], "3")
                    continue
            if metamon["con"] != metamon["conMax"]:
                print("Size")
                if self.addAttrNeedAsset(metamon["id"], "4") != "SUCCESS":
                    continue
                else:
                    self.addAttr(metamon["id"], "4")
                    continue

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

    def checkBag(self, itemBeChecked):
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

    def buyItemInDrops(self, orderId, num):
        payload = {"address": self.address, "orderId": orderId, "num": num}
        url = f"{BASE_URL}/official-sale/buy"
        response = self.post_data(url, payload)
        if response["code"] != "SUCCESS":
            print("buy: " + response["message"])
        else:
            print("Buy items successfully")
        return response["code"]

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

    def checkAbility(self):
        if self.level == 60 and self.exp >= 395:
            potion = self.checkBag(2)
            if potion == 0:
                self.buyQuickly(2, 1, 1, 1000)
            self.resetMonster(self.id)
            self.exp = 0
        if self.level == 59 and self.exp == 600:
            if self.rarity == "N":
                itemNeedToBuy = self.checkBag(2)
                if itemNeedToBuy == 0:
                    self.buyQuickly(2, 1, 1, 1000)
            if self.rarity == "R":
                itemNeedToBuy = self.checkBag(3)
                if itemNeedToBuy == 0:
                    self.buyQuickly(3, 1, 1, 100000)
            if self.rarity == "SR" or self.rarity == "SSR":
                itemNeedToBuy = self.checkBag(4)
                if itemNeedToBuy == 0:
                    self.buyQuickly(4, 1, 1, 1000000)
            self.updateMonster(self.id)
            self.level = 60
            self.exp = 0
            self.status = False
        if self.level != 59 and self.exp >= self.expMax:
            if self.rarity == "N":
                itemNeedToBuy = self.checkBag(2)
                if itemNeedToBuy == 0:
                    self.buyQuickly(2, 1, 1, 1000)
            if self.rarity == "R":
                itemNeedToBuy = self.checkBag(3)
                if itemNeedToBuy == 0:
                    self.buyQuickly(3, 1, 1, 100000)
            if self.rarity == "SR" or self.rarity == "SSR":
                itemNeedToBuy = self.checkBag(4)
                if itemNeedToBuy == 0:
                    self.buyQuickly(4, 1, 1, 1000000)
            self.updateMonster(self.id)
            self.exp = 0
            self.level += 1
        if self.hi <= 90 and self.addFatigueNeedAsset(self.id) == "SUCCESS":
            hiPotion = self.checkBag(11)
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
