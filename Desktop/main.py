import market
import play

import requests
import os
from prettytable import PrettyTable
from dotenv import load_dotenv

load_dotenv()

ADDRESS_WALLET = os.getenv("ADDRESS_WALLET")
SIGN_WALLET = os.getenv("SIGN_WALLET")
MSG_WALLET = os.getenv("MSG_WALLET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
accessTokenGame = ""


class AccessGame:
    def __init__(self, address, sign, msg):
        self.accessToken = None
        self.address = address
        self.sign = sign
        self.msg = msg
        self.initAccessToken()

    def changeAccessTokenInSetting(self):
        envFile = open(".env")
        contentInEnvFile = envFile.readlines()
        envFile.close()

        contentInEnvFile[3] = "ACCESS_TOKEN = " + str(self.accessToken) + "\n"
        envFile = open(".env", "w")
        newContentInEnvFile = "".join(contentInEnvFile)
        envFile.write(newContentInEnvFile)
        envFile.close()

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
        if json.get("code") != "SUCCESS":
            print("Can't get accessToken")
            exit()
        else:
            self.accessToken = json.get("data").get("accessToken")

    def getLoginCode(self):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address}
        url = "https://metamon-api.radiocaca.com/usm-api/owner-setting/email/sendLoginCode"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        if json.get("code") != "SUCCESS":
            print("Can't send login code to email")
            exit()
        else:
            print("Code is sending to your email. Kindly check")

    def verifyLoginCode(self, loginCode):
        headers = {
            "accessToken": self.accessToken,
        }
        payload = {"address": self.address, "code": loginCode}
        url = "https://metamon-api.radiocaca.com/usm-api/owner-setting/email/verifyLoginCode"
        response = requests.request("POST", url, headers=headers, data=payload)
        json = response.json()
        return json.get("code")

    def initAccessToken(self):
        self.getAccessToken()
        self.changeAccessTokenInSetting()
        self.getLoginCode()
        while 1 != 0:
            print("Please fill your code:")
            code = self.verifyLoginCode(loginCode=input())
            if code != "SUCCESS":
                print("Login code is not correct")
                continue
            else:
                print("Email is verified")
                return


def playGame():
    if accessTokenGame == "":
        mtm = play.MetamonPlayer(address=ADDRESS_WALLET, accessToken=ACCESS_TOKEN)
    else:
        mtm = play.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessTokenGame)
    helloContent = """
    1. Battle in Island
    2. Mint eggs
    3. Show all metamons
    4. Up attribute all monsters   
    5. Join the best squad in Lost world
    6. Battle record in Lost world
    7. Get status my teams in Lost world
    0. Exit
    Please select you want to choose
    """
    while 1 != 0:
        caseNumber = int(input(helloContent))
        if caseNumber == 1:
            status = mtm.startBattleIsland()
            if status == 60:
                continue
            if status == 0:
                return
        if caseNumber == 2:
            mtm.mintEgg()
        if caseNumber == 3:
            mtm.showAllMetamons()
        if caseNumber == 4:
            mtm.addAttrAllMetamon()
        if caseNumber == 5:
            mtm.joinTheBestSquad()
        if caseNumber == 6:
            mtm.battleRecord()
        if caseNumber == 7:
            mtm.getMyTeams()
        if caseNumber == 0:
            return


def marketGame():
    if accessTokenGame == "":
        mtm = market.MetamonPlayer(address=ADDRESS_WALLET, accessToken=ACCESS_TOKEN)
    else:
        mtm = market.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessTokenGame)
    helloContent = """
    1. Check bag
    2. Shopping
    3. Shelling
    4. Canceling
    5. Buy item in drops
    6. Transaction history
    0. Exit
    Please select you want to choose
    """
    shoppingContent = """
    1. Manual
    2. Automatic
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
            mtm.checkBag()
        if caseNumber == 2:
            caseNumber = int(input(shoppingContent))
            if caseNumber == 1:
                mtm.shopping()
            if caseNumber == 2:
                mtm.shoppingWithSetPrice()
            if caseNumber == 0:
                continue
        if caseNumber == 3:
            caseNumber = int(input(shellingContent))
            if caseNumber == 1:
                mtm.shelling(caseNumber)
            if caseNumber == 2:
                mtm.shelling(caseNumber)
            if caseNumber == 0:
                continue
        if caseNumber == 4:
            mtm.canceling()
        if caseNumber == 5:
            mtm.buyDrops()
        if caseNumber == 6:
            mtm.transactionHistory()
        if caseNumber == 0:
            return


if __name__ == "__main__":
    helloContent = """
    1. Get access token game
    2. Play game
    3. Market game
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
            playGame()
        if caseNumber == 3:
            marketGame()
        if caseNumber == 0:
            exit()
