import requests
from prettytable import PrettyTable
import time

attrType = {
    "1": "luck",
    "2": "courage",
    "3": "wisdom",
    "4": "size",
    "5": "stealth",
}


class MetamonPlayer:
    def __init__(self, address, accessToken):
        self.accessToken = accessToken
        self.address = address
        self.fragmentNum = 0
        self.battleWin = 0
        self.battleLose = 0

    def getMetamonList(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "orderType": "-1"}

        url = "https://metamon-api.radiocaca.com/usm-api/getWalletPropertyList"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("data").get("metamonList")

    def showAllMetamons(self):
        metamonList = self.getMetamonList()
        position = ""
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
        ]
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
        for metamon in metamonList:
            if int(metamon["position"]) == 1:
                position = "Island"
            else:
                position = "Last world"
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
                    position,
                    metamon["race"],
                ]
            )
        print(table)

    def getMetamonAtIslandList(self):
        metamonList = self.getMetamonList()
        metamonAtIslandList = []
        for metamon in metamonList:
            if metamon["position"] == 1:
                metamonAtIslandList.append(metamon)
        return metamonAtIslandList

    def addAttrNeedAsset(self, metamonId, type):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "nftId": metamonId,
            "attrType": type,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/addAttrNeedAsset"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("code")

    def addAttr(self, metamonId, type):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "nftId": metamonId,
            "attrType": type,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/addAttr"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        upperNum = json.get("data").get("upperNum")
        print(f"{metamonId} up {attrType[type]} is {upperNum}")

    def resetMonster(self, metamonId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "nftId": metamonId}
        url = "https://metamon-api.radiocaca.com/usm-api/resetMonster"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        print(json)

    def addAttrAllMetamon(self):
        helloContent = """
        1. Luck
        2. Courage
        3. Wisdom
        4. Size
        5. Stealth
        Please choose attr to add all metamons
        """
        metamonList = self.getMetamonList()
        caseNumber = input(helloContent)
        for metamon in metamonList:
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)

    def getBattelObjects(self, metamonId, level):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {
            "address": self.address,
            "metamonId": metamonId,
            "front": level,
        }
        url = "https://metamon-api.radiocaca.com/usm-api/getBattelObjects"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("data").get("objects")

    def getMinScareBattleObject(self, metamonId, level):
        scareScore = 650
        battelObjects = self.getBattelObjects(metamonId, level)
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
            print(f"{myMonId} is win")
        else:
            self.battleLose += 1
            print(f"{myMonId} is lose")

    def startBattleIsland(self):
        metamonAtIslandList = self.getMetamonAtIslandList()
        for metamon in metamonAtIslandList:
            (
                minScareBattleObjectAllLevel,
                levelBattleObject,
            ) = self.getMinScareBattleObjectAllLevel(metamon["id"], metamon["level"])
            for i in range(metamon["tear"]):
                if int(metamon["level"]) == 60 and int(metamon["exp"]) == 395:
                    self.resetMonster(metamon["id"])
                self.battleIsland(
                    metamon["id"], minScareBattleObjectAllLevel, levelBattleObject
                )
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

    def getScoreGroupInKingdom(self, _scoreAverage, _monsterNum):
        scoreAverage = 0
        monsterNum = 0
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
            "Monster number",
            "ID group",
            "Group name",
        ]
        table.align["Score average"] = "r"
        table.align["Monster number"] = "r"
        table.align["ID"] = "r"
        table.align["Group"] = "l"

        for squad in squadList:
            if int(squad["monsterNum"]) >= 100:
                scoreAverageTemp = round(
                    int(squad["totalSca"]) / int(squad["monsterNum"])
                )
                if (
                    scoreAverage < scoreAverageTemp
                    and int(squad["monsterNum"]) > _monsterNum
                ):
                    scoreAverage = scoreAverageTemp
                    monsterNum = int(squad["monsterNum"])
                    idSquad = int(squad["id"])
                table.add_row(
                    [
                        scoreAverageTemp,
                        squad["monsterNum"],
                        squad["name"],
                        squad["id"],
                    ]
                )
        print(table)
        if scoreAverage > _scoreAverage:
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
        while 1 != 0:
            idSquadOfTheBest = self.getScoreGroupInKingdom(scoreAverage, monsterNum)
            if idSquadOfTheBest == 0:
                time.sleep(3)
                continue
            else:
                self.teamJoin(idSquadOfTheBest)
                return
