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
        if json.get("code") != "SUCCESS":
            print("Can't verify login code")
            exit()
        else:
            print("Email is verified")

    def initAccessToken(self):
        self.getAccessToken()
        self.changeAccessTokenInSetting()
        self.getLoginCode()
        print("Please fill your code:")
        self.verifyLoginCode(loginCode=input())


def playGame():
    if accessTokenGame == "":
        mtm = play.MetamonPlayer(address=ADDRESS_WALLET, accessToken=ACCESS_TOKEN)
    else:
        mtm = play.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessTokenGame)
    helloContent = """
    1. Battle in Island
    2. Mint eggs
    3. Up attribute all monsters    
    0. Exit
    Please select you want to choose
    """
    while 1 != 0:
        caseNumber = int(input(helloContent))
        if caseNumber == 1:
            mtm.startBattleIsland()
        if caseNumber == 2:
            mtm.mintEgg()
        if caseNumber == 3:
            mtm.addAttrAllMetamon()
        if caseNumber == 0:
            return


def marketGame():
    if accessTokenGame == "":
        mtm = market.MetamonPlayer(address=ADDRESS_WALLET, accessToken=ACCESS_TOKEN)
    else:
        mtm = market.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessTokenGame)
    helloContent = """
    1. Check bag
    2. Check price in the market
    3. Shopping
    4. Shelling unit item
    5. Canceling
    0. Exit
    Please select you want to choose
    """
    while 1 != 0:
        caseNumber = int(input(helloContent))
        if caseNumber == 1:
            mtm.checkBag()
        if caseNumber == 2:
            typeItem = market.getTypeItem()
            orderType = market.getOrderType()
            while 1 != 0:
                mtm.getPriceInMarket(typeItem, orderType)
        if caseNumber == 3:
            mtm.shopping()
        if caseNumber == 4:
            mtm.shellingUnitItem()
        if caseNumber == 5:
            mtm.canceling()
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
