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

    def getMetamonsAtIsland(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "orderType": "-1"}

        url = "https://metamon-api.radiocaca.com/usm-api/getWalletPropertyList"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("data").get("metamonList")

    def getMetamonsAtLostWorld(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "orderType": "2", "position": 2}

        url = "https://metamon-api.radiocaca.com/usm-api/kingdom/monsterList"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("data")

    def showAllMetamons(self):
        metamonsAtIsland = self.getMetamonsAtIsland()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        resultContent = ""
        for metamon in metamonsAtLostWorld:
            resultContent = resultContent + "\nID\tLv\tExp\tLuck\tCourage\n"
            resultContent = resultContent + str(metamon["tokenId"]) + "\t"
            resultContent = resultContent + str(metamon["level"]) + "\t"
            resultContent = resultContent + str(metamon["exp"]) + "\t"
            resultContent = resultContent + str(metamon["luk"]) + "\t"
            resultContent = resultContent + str(metamon["crg"]) + "\t"
            resultContent = resultContent + "\nWisdom\tSize\tStealth\tHI\tDate\n"
            resultContent = resultContent + str(metamon["inte"]) + "\t"
            resultContent = resultContent + str(metamon["con"]) + "\t"
            resultContent = resultContent + str(metamon["inv"]) + "\t"
            resultContent = resultContent + str(metamon["healthy"]) + "\t"
            resultContent = resultContent + str(metamon["kingdomUnLockDate"])
            resultContent = resultContent + "\n---------------------------------------"
        for metamon in metamonsAtIsland:
            resultContent = resultContent + "\nID\tLv\tExp\tLuck\tCourage\n"
            resultContent = resultContent + str(metamon["tokenId"]) + "\t"
            resultContent = resultContent + str(metamon["level"]) + "\t"
            resultContent = resultContent + str(metamon["exp"]) + "\t"
            resultContent = resultContent + str(metamon["luk"]) + "\t"
            resultContent = resultContent + str(metamon["crg"]) + "\t"
            resultContent = resultContent + "\nWisdom\tSize\tStealth\tHI\tDate\n"
            resultContent = resultContent + str(metamon["inte"]) + "\t"
            resultContent = resultContent + str(metamon["con"]) + "\t"
            resultContent = resultContent + str(metamon["inv"]) + "\t"
            resultContent = resultContent + str(metamon["healthy"]) + "\t"
            resultContent = resultContent + str(metamon["kingdomUnLockDate"])
            resultContent = resultContent + "\n---------------------------------------"
        print(resultContent)

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
        code = json.get("code")
        if code == "SUCCESS":
            print("Reseted monster successfully")
        else:
            print("Can't reset monster")

    def updateMonster(self, metamonId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "nftId": metamonId}
        url = "https://metamon-api.radiocaca.com/usm-api/updateMonster"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        code = json.get("code")
        if code == "SUCCESS":
            print("Updated monster successfully")
        else:
            print("Can't update monster")

    def addHealthy(self, metamonId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "nftId": metamonId}
        url = "https://metamon-api.radiocaca.com/usm-api/addHealthy"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        code = json.get("code")
        if code == "SUCCESS":
            print("Add healthy monster successfully")
        else:
            print("Can't add healthy monster")

    def addFatigueNeedAsset(self, metamonId):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "nftId": metamonId}
        url = "https://metamon-api.radiocaca.com/usm-api/addFatigueNeedAsset"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("code")

    def addAttrAllMetamon(self):
        helloContent = """
        1. Luck
        2. Courage
        3. Wisdom
        4. Size
        5. Stealth
        Please choose attr to add all metamons
        """
        metamonsAtIsland = self.getMetamonsAtIsland()
        metamonsAtLostWorld = self.getMetamonsAtLostWorld()
        caseNumber = input(helloContent)
        for metamon in metamonsAtIsland:
            if self.addAttrNeedAsset(metamon["id"], caseNumber) == "SUCCESS":
                self.addAttr(metamon["id"], caseNumber)
        for metamon in metamonsAtLostWorld:
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
                self.battleIsland(id, minScareBattleObjectAllLevel, levelBattleObject)
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
            "Score",
            "Mons",
            "R Mons",
            "Group",
            "ID",
        ]
        table.align["Score"] = "r"
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
            "Mons",
            "My score",
            "R mons",
            "Team score",
            "Unlock date",
        ]
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
