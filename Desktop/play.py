import requests
from prettytable import PrettyTable
import time

# Global constants
## The attributes of metamon
attrType = {
    "1": "luck",
    "2": "courage",
    "3": "wisdom",
    "4": "size",
    "5": "stealth",
}


class MetamonPlayer:
    def __init__(self, address, accessToken):
        """! The MetamonPlayer base class initializer

        @param address The address of wallet connect to Metamon Game
        @param accessToken The accessToken of wallet connect to Metamon Game
        """
        ## The accessToken of wallet
        self.accessToken = accessToken
        ## The address of wallet
        self.address = address
        ## Initialization fragment numbers, numbers of battle win and lose
        # when we start battle in Island
        self.fragmentNum = 0
        self.battleWin = 0
        self.battleLose = 0

    def getMetamonsAtIsland(self):
        """! Get list of metamon at island
        @return List of metamon at island
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {"address": self.address, "orderType": "-1"}
        ## Url of API
        url = "https://metamon-api.radiocaca.com/usm-api/getWalletPropertyList"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        return json.get("data").get("metamonList")

    def getMetamonsAtLostWorld(self):
        """! Get list of metamon at lost world
        @return List of metamon at lost world
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {"address": self.address, "orderType": "2", "position": 2}
        ## Url of API
        url = "https://metamon-api.radiocaca.com/usm-api/kingdom/monsterList"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        return json.get("data")

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
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {
            "address": self.address,
            "nftId": metamonId,
            "attrType": type,
        }
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/addAttrNeedAsset"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        return json.get("code")

    def addAttr(self, metamonId, type):
        """! Upgrade the attribute metamon
        @param metamonId The id of metamon inside Metamon Game
        @param type The type of attribute you want to upgrade
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {
            "address": self.address,
            "nftId": metamonId,
            "attrType": type,
        }
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/addAttr"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        ## The upper number of data
        upperNum = json.get("data").get("upperNum")
        ## Show the metamon is updated
        print(f"{metamonId} up {attrType[type]} is {upperNum}")

    def resetMonster(self, metamonId):
        """! Reset exp of the metamon lv 60 when she travel to island
        @param metamonId The id of metamon inside Metamon Game
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/resetMonster"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        ## The status from data
        code = json.get("code")
        ## Show off the notice when status when the status is "SUCCESS" or not
        if code == "SUCCESS":
            print("Reseted monster successfully")
        else:
            print("Can't reset monster")

    def updateMonster(self, metamonId):
        """! Up level of the metamon
        @param metamonId The id of metamon inside Metamon Game
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/updateMonster"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        ## The status from data
        code = json.get("code")
        ## Show off the notice when status when the status is "SUCCESS" or not
        if code == "SUCCESS":
            print("Updated monster successfully")
        else:
            print("Can't update monster")

    def addHealthy(self, metamonId):
        """! Add a health index of the metamon
        @param metamonId The id of metamon inside Metamon Game
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/addHealthy"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        ## The status from data
        code = json.get("code")
        ## Show off the notice when status when the status is "SUCCESS" or not
        if code == "SUCCESS":
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
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {"address": self.address, "nftId": metamonId}
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/addFatigueNeedAsset"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        return json.get("code")

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
        for metamon in metamonsAtIsland:
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)
        for metamon in metamonsAtLostWorld:
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)

    def getBattelObjects(self, metamonId, level):
        """! Get battle objects in the battle fields
        @param metamonId The id of metamon inside Metamon Game
        @param level The level of the battle fields
        @return The list of battle objects in the battle field
        """
        ## Headers of API
        headers = {
            "accessToken": self.accessToken,
        }
        ## Payload of API
        payload = {
            "address": self.address,
            "metamonId": metamonId,
            "front": level,
        }
        ## URL of API
        url = "https://metamon-api.radiocaca.com/usm-api/getBattelObjects"
        ## Get data from API via POST method
        response = requests.request("POST", url, headers=headers, data=payload)
        ## Transfrom raw data to json data
        json = response.json()
        return json.get("data").get("objects")

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
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "monsterA": myMonId,
            "monsterB": battleMonId,
            "battleLevel": battleLevel,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/startBattle"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        self.fragmentNum += json.get("data").get("bpFragmentNum")
        if json.get("data").get("challengeExp") == 5:
            self.battleWin += 1
            return True
        else:
            self.battleLose += 1
            return False

    def checkAbility(self, id, level, exp, expMax, hi):
        status = True
        if level == 60 and exp == 395:
            self.resetMonster(id)
            exp = 0
        if level == 59 and exp == 600:
            self.updateMonster(id)
            level = 60
            exp = 0
            status = False
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
        return status, level, exp

    def startBattleIsland(self):
        metamonAtIslandList = self.getMetamonsAtIsland()
        for metamon in metamonAtIslandList:
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
            status, level, exp = self.checkAbility(id, level, exp, expMax, hi)
            # Get the mininum score scare object battle
            (
                minScareBattleObjectAllLevel,
                levelBattleObject,
            ) = self.getMinScareBattleObjectAllLevel(id, level)
            for i in range(tear):
                # Update ability of metamon
                status, level, exp = self.checkAbility(id, level, exp, expMax, hi)
                if status == False:  # This case for metamon lv 59 -> 60
                    break
                statusBattle = self.battleIsland(
                    id, minScareBattleObjectAllLevel, levelBattleObject
                )
                if statusBattle == True:
                    exp += 5
                else:
                    exp += 3
            print(f"End {tokenId}")
        print(f"Total egg fragments: {self.fragmentNum}")
        print(f"Total win battle: {self.battleWin}")
        print(f"Total lose battel: {self.battleLose}")
        rateWin = 0
        if self.fragmentNum != 0:
            rateWin = self.battleWin / (self.battleLose + self.battleWin) * 100
        print(f"Rate: {round(rateWin)}%")

    def mintEgg(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address}
        url = "https://metamon-api.radiocaca.com/usm-api/composeMonsterEgg"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        code = json.get("code")
        if code != "SUCCESS":
            print("Mint eggs failed!")
            return

        print(f"Minted eggs are success")

    def getScoreGroupInKingdom(self, _scoreAverage, _monsterNum, _monsterNumRarity):
        scoreAverage = 0
        idSquad = 0
        idSquadOfTheBest = 0
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "teamId": -1,
            "pageSize": 100,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/kingdom/teamList"
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json = response.json()
        squadList = json.get("data").get("list")
        table = PrettyTable()
        table.field_names = [
            "Score average",
            "All monsters",
            "R Monsters",
            "Group name",
            "ID group",
        ]
        table.align["Score average"] = "r"
        table.align["All monsters"] = "r"
        table.align["R Monsters"] = "r"
        table.align["Group"] = "l"
        table.align["ID"] = "r"

        for squad in squadList:
            if int(squad["monsterNum"]) >= 100:
                if (
                    int(squad["monsterNum"]) > _monsterNum
                    and scoreAverage < int(squad["averageSca"])
                    or int(squad["monsterNumRarity"]) > _monsterNumRarity
                ):
                    scoreAverage = int(squad["averageSca"])
                    idSquad = int(squad["id"])
                table.add_row(
                    [
                        squad["averageSca"],
                        squad["monsterNum"],
                        squad["monsterNumRarity"],
                        squad["name"],
                        squad["id"],
                    ]
                )
        print(table)
        if (
            scoreAverage > _scoreAverage
            or int(squad["monsterNumRarity"]) > _monsterNumRarity
        ):
            idSquadOfTheBest = idSquad
            print(
                f"Found the squad as your demand with score average is {_scoreAverage} and monster number is {_monsterNum}"
            )
        return idSquadOfTheBest

    def teamJoin(self, teamId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "teamId": teamId}
        url = "https://metamon-api.radiocaca.com/usm-api/kingdom/teamJoin"
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json = response.json()
        print(json)

    def joinTheBestSquad(self):
        scoreAverage = int(input("Please enter your score average:\n"))
        monsterNum = int(input("Please enter your monster number:\n"))
        monsterNumRarity = int(input("Please enter your Rare monster number:\n"))
        while 1 != 0:
            idSquadOfTheBest = self.getScoreGroupInKingdom(
                scoreAverage, monsterNum, monsterNumRarity
            )
            if idSquadOfTheBest == 0:
                time.sleep(5)
                continue
            else:
                self.teamJoin(idSquadOfTheBest)
                return

    def battleRecord(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "pageSize": 15, "battleId": -1}
        url = "https://metamon-api.radiocaca.com/usm-api/kingdom/battleRecord"
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json = response.json()
        battleRecordDetails = json.get("data").get("battleRecordDetails")
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
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address}
        url = "https://metamon-api.radiocaca.com/usm-api/kingdom/myTeams"
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json = response.json()
        battles = json.get("data")
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
