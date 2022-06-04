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

    def post_data(self, url, payload):
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
        return response["data"]

    def showAllMetamons(self):
        """! Show off all metamons"""
        ## Init metamons of Island via getMetamonsAtIsland()
        metamonsAtIsland = self.getMetamonsAtIsland()
        ## Init metamons of Lost world via getMetamonsAtLostWorld()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        ## Creata a table with these field names
        table = PrettyTable()
        table.field_names = [
            "ID",
            "Rare",
            "Level",
            "Exp",
            "Luck",
            "Courage",
            "Wisdom",
            "Size",
            "Stealth",
            "HI",
            "Position",
            "Race",
            "Unlock Date",
        ]
        ## Align of these field names
        table.align["ID"] = "r"
        table.align["Rare"] = "r"
        table.align["Level"] = "r"
        table.align["Exp"] = "r"
        table.align["Luck"] = "r"
        table.align["Courage"] = "r"
        table.align["Wisdom"] = "r"
        table.align["Size"] = "r"
        table.align["Stealth"] = "r"
        table.align["HI"] = "r"
        table.align["Position"] = "l"
        table.align["Race"] = "l"
        ## Loop in each metamon of lost world, add them to these field names
        for metamon in metamonsAtLostWorld:
            table.add_row(
                [
                    metamon["tokenId"],
                    metamon["rarity"],
                    metamon["level"],
                    metamon["exp"],
                    metamon["luk"],
                    metamon["crg"],
                    metamon["inte"],
                    metamon["con"],
                    metamon["inv"],
                    metamon["healthy"],
                    "Lost world",
                    metamon["race"],
                    metamon["kingdomUnLockDate"],
                ]
            )
        ## Loop in each metamon of island, add them to these field names
        for metamon in metamonsAtIsland:
            table.add_row(
                [
                    metamon["tokenId"],
                    metamon["rarity"],
                    metamon["level"],
                    metamon["exp"],
                    metamon["luk"],
                    metamon["crg"],
                    metamon["inte"],
                    metamon["con"],
                    metamon["inv"],
                    metamon["healthy"],
                    "Island",
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
        ## The upper number of data
        upperNum = response["data"]["upperNum"]
        ## Show the metamon is updated
        print(f"{metamonId} up {attrType[type]} is {upperNum}")

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
        if response["code"] == "SUCCESS":
            print("Reseted monster successfully")
        else:
            print("Can't reset monster")

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
        if response["code"] == "SUCCESS":
            print("Updated monster successfully")
        else:
            print("Can't update monster")

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
        if response["code"] == "SUCCESS":
            print("Add healthy monster successfully")
        else:
            print("Can't add healthy monster")

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
        return response["code"]

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
        metamonsAtIsland = self.getMetamonsAtIsland()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        caseNumber = input(helloContent)
        ## Loop through all metamons, first check ability to add attribute
        ## of the memontamon, if it is "SUCCESS", do add attribute to the metamon
        metamonNumbers = 0
        for metamon in metamonsAtIsland:
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)
                metamonNumbers += 1
        for metamon in metamonsAtLostWorld:
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)
                metamonNumbers += 1
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
        return response["data"]["objects"]

    def getMinScareBattleObject(self, metamonId, level):
        """! Get the mininum score battle object in the battle fields
        @param metamonId The id of metamon inside Metamon Game
        @param level The level of the battle fields
        @return The list of mininum score battle object in the battle field
        """
        ## Init the maximum score
        scareScore = 650
        ## Get battel objects via method getBattelObjects
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

    def battleIsland(self, myMonId, battleMonId, battleLevel):
        payload = {
            "address": self.address,
            "monsterA": myMonId,
            "monsterB": battleMonId,
            "battleLevel": battleLevel,
        }
        url = f"{BASE_URL}/startBattle"
        response = self.post_data(url, payload)
        self.fragmentNum += response["data"]["bpFragmentNum"]
        if response["data"]["challengeExp"] == 5:
            self.battleWin += 1
            return True
        else:
            self.battleLose += 1
            return False

    def checkAbility(self, id, level, exp, expMax, hi):
        if level == 60 and exp == 395:
            self.resetMonster(id)
            exp = 0
        if level == 59 and exp == 600:
            self.updateMonster(id)
            level = 60
            exp = 0
            self.status = False
        if level != 59 and exp >= expMax:
            self.updateMonster(id)
            exp = 0
            level += 1
        if hi <= 90:
            if self.addFatigueNeedAsset(id) == "SUCCESS":
                self.addHealthy(id)
                hi += 10
            else:
                print("Please check HI is available or not")
        return level, exp, hi

    def startBattleIsland(self):
        metamonAtIslandList = self.getMetamonsAtIsland()
        for metamon in metamonAtIslandList:
            self.status = True
            tokenId = metamon["tokenId"]
            id = metamon["id"]
            level = int(metamon["level"])
            exp = int(metamon["exp"])
            expMax = int(metamon["expMax"])
            hi = int(metamon["healthy"])
            tear = int(metamon["tear"])
            print(
                f"Start {tokenId} with level:{level}, exp:{exp}, HI:{hi} and {tear} turns"
            )
            # Check ability of metamon before start battle
            level, exp, hi = self.checkAbility(id, level, exp, expMax, hi)
            # Get the mininum score scare object battle
            (
                minScareBattleObjectAllLevel,
                levelBattleObject,
            ) = self.getMinScareBattleObjectAllLevel(id, level)
            for i in range(tear):
                # Update ability of metamon
                level, exp, hi = self.checkAbility(id, level, exp, expMax, hi)
                if self.status == False:  # This case for metamon lv 59 -> 60
                    break
                statusBattle = self.battleIsland(
                    id, minScareBattleObjectAllLevel, levelBattleObject
                )
                if statusBattle == True:
                    exp += 5
                else:
                    exp += 3
            print(f"End {tokenId}")
            if self.status == False:  # This case for metamon lv 59 -> 60
                continue
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
            print("Mint eggs failed!")
            return
        print(f"Minted eggs are success")

    def getScoreGroupInKingdom(self, thresholdSca):
        payload = {
            "address": self.address,
            "page": 1,
            "pageSize": 100,
            "orderField": "monsterNum",
        }
        url = f"{BASE_URL}/kingdom/teamList"
        response = self.post_data(url, payload)
        squadList = response["data"]["list"]
        table = PrettyTable()
        table.field_names = [
            "Index",
            "Group",
            "Min",
            "Score",
            "Monsters",
            "R",
        ]
        table.align["Index"] = "r"
        table.align["Group"] = "l"
        table.align["Score"] = "r"
        table.align["Min"] = "r"
        table.align["Monsters"] = "r"
        table.align["R"] = "r"
        indexSquad = 0
        idSquadList = {}
        monSquadList = {}
        scaSquadList = {}
        for squad in squadList:
            if (
                int(squad["monsterNum"]) >= 100
                and str(squad["lockTeam"]).lower() == "false"
                and int(squad["monsterScaThreshold"]) <= thresholdSca
            ):
                indexSquad += 1
                idSquadList[indexSquad] = int(squad["id"])
                monSquadList[indexSquad] = int(squad["monsterNum"])
                scaSquadList[indexSquad] = int(squad["averageSca"])
                table.add_row(
                    [
                        indexSquad,
                        squad["name"],
                        squad["monsterScaThreshold"],
                        squad["averageSca"],
                        squad["monsterNum"],
                        squad["monsterNumRarity"],
                    ]
                )
        print(table)
        return idSquadList, monSquadList, scaSquadList

    def getMetamonIsReadyInKingdom(self):
        metamons = self.getMetamonsAtLostWorld()
        metamonsList = []
        sca = 650
        for metamon in metamons:
            if str(metamon["kingdomLock"]).lower() == "false":
                nftId = '{nftId: "' + str(metamon["id"]) + '"}'
                metamonsList.append(nftId)
                if int(metamon["sca"]) < sca:
                    sca = int(metamon["sca"])
        return metamonsList, sca

    def joinLostWorldManual(self, metamonsList, sca):
        print(f"We have {len(metamonsList)} metamons are available")
        metamons = ", ".join(metamonsList)

        while 1 != 0:
            idSquadList, monSquadList, scaSquadList = self.getScoreGroupInKingdom(sca)
            caseNumber = int(
                input(
                    f"Select number in range {len(idSquadList)} to join - 0 to refresh\n"
                )
            )
            if caseNumber == 0:
                continue
            elif caseNumber in range(len(idSquadList) + 1):
                self.teamJoin(idSquadList[caseNumber], metamons)
                continue
            else:
                return

    def joinLostWorldAutomatic(
        self, _scoreAverage=650, _monsterNum=900, metamonsList=[], sca=650
    ):
        print(f"We have {len(metamonsList)} metamons are available")
        metamons = ", ".join(metamonsList)

        while 1 != 0:
            idSquadList, monSquadList, scaSquadList = self.getScoreGroupInKingdom(sca)

            for i in range(len(idSquadList)):
                if (monSquadList[i + 1] >= _monsterNum) and (
                    scaSquadList[i + 1] >= _scoreAverage
                ):
                    print(
                        f"Found the squad as your demand with score average is {_scoreAverage} and monster number is {_monsterNum}"
                    )
                    self.teamJoin(idSquadList[i + 1], metamons)
                    return
            time.sleep(5)

    def teamJoin(self, teamId, metamons):
        payload = {"address": self.address, "teamId": teamId}
        url = f"{BASE_URL}/kingdom/teamJoin"
        response = self.post_data(url, payload)
        print(response)

    def joinTheBestSquad(self):
        joinSquadContent = """
        1. Manual
        2. Automatic
        Please select you want to choose
        """
        metamonsList, sca = self.getMetamonIsReadyInKingdom()
        if metamonsList == []:
            print("No metamons are available")
            return
        caseNumber = int(input(joinSquadContent))
        if caseNumber == 2:
            scoreAverage = int(input("Please enter your score average:\n"))
            monsterNum = int(input("Please enter your monster number:\n"))
        while 1 != 0:
            metamonsList, sca = self.getMetamonIsReadyInKingdom()
            if metamonsList == []:
                print("No metamons are available")
                return
            if caseNumber == 1:
                self.joinLostWorldManual(metamonsList, sca)
                continue
            if caseNumber == 2:
                self.joinLostWorldAutomatic(scoreAverage, monsterNum, metamonsList, sca)
                continue

    def battleRecord(self):
        payload = {"address": self.address, "pageSize": 15, "battleId": -1}
        url = f"{BASE_URL}/kingdom/battleRecord"
        response = self.post_data(url, payload)
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
        battles = response["data"]
        table = PrettyTable()
        table.field_names = [
            "My monsters",
            "My average",
            "R monsters",
            "Team average",
            "Unlock date",
        ]
        table.align["My monsters"] = "r"
        table.align["My average"] = "r"
        table.align["R monsters"] = "r"
        table.align["Team average"] = "r"
        for battle in battles:
            myAverage = int(battle["mytotalSca"]) / int(battle["myMonsterNum"])
            table.add_row(
                [
                    battle["myMonsterNum"],
                    myAverage,
                    battle["monsterNumRarity"],
                    battle["averageSca"],
                    battle["unlockDate"],
                ]
            )
        print(table)
