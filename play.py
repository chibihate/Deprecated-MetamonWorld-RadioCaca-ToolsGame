import requests
import os
from dotenv import load_dotenv

load_dotenv()

ADDRESS_WALLET = os.getenv("ADDRESS_WALLET")
SIGN_WALLET = os.getenv("SIGN_WALLET")
MSG_WALLET = os.getenv("MSG_WALLET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

attrType = {
    "1": "luck",
    "2": "courage",
    "3": "wisdom",
    "4": "size",
    "5": "stealth",
}


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
        print(json)
        print("Code is sending to your email. Kindly check")

    def verifyLoginCode(self, loginCode):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "code": loginCode}
        url = "https://metamon-api.radiocaca.com/usm-api/owner-setting/email/verifyLoginCode"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        print(json)

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

    def getMetamonList(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "orderType": "-1"}

        url = "https://metamon-api.radiocaca.com/usm-api/getWalletPropertyList"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        # print(json)
        return json.get("data").get("metamonList")

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
            # print("numberBattleField is " + str(numberBattleField))
        elif 41 <= int(metamonLevel) <= 60:
            numberBattleField = 3
            # print("numberBattleField is " + str(numberBattleField))
        else:
            numberBattleField = 1
            # print("numberBattleField is " + str(numberBattleField))
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


if __name__ == "__main__":
    accessTokenGame = ""

    helloContent = """
    1. Get access token game
    2. Get metamon player
    3. Up attribute all monsters
    4. Battle in Island
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
            mtm.addAttrAllMetamon()
        if caseNumber == 4:
            mtm.startBattleIsland()
        if caseNumber == 0:
            exit()
