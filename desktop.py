import market
import play
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ADDRESS_WALLET = os.getenv("ADDRESS_WALLET")
SIGN_WALLET = os.getenv("SIGN_WALLET")
MSG_WALLET = os.getenv("MSG_WALLET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# URLs to make api calls
BASE_URL = "https://metamon-api.radiocaca.com/usm-api"


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
        self.getInfo()

    def post_data(self, url, payload):
        return json.loads(
            requests.Session().post(url, data=payload, headers=self.headers).text
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
        if response["code"] != "SUCCESS":
            self.initAccessToken()
        else:
            return

    def getAccessToken(self):
        """Obtain token for game session to perform battles and other actions"""
        url = f"{BASE_URL}/login"
        response = self.post_data(url, self.payload_login)
        if response["code"] != "SUCCESS":
            print("Can't get accessToken")
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
            print("Can't send login code to email")
            exit()
        else:
            print("Code is sending to your email. Kindly check")

    def verifyLoginCode(self, loginCode):
        payload = {"address": self.address, "code": loginCode}
        url = f"{BASE_URL}/owner-setting/email/verifyLoginCode"
        response = self.post_data(url, payload)
        return response["code"]

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


def playGame(accessToken):
    mtm = play.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessToken)
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
            mtm.startBattleIsland()
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


def marketGame(accessToken):
    mtm = market.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessToken)
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
    1. Play game
    2. Market game
    0. Exit
    Please select you want to choose
    """
    mtm = MetamonPlayer(address=ADDRESS_WALLET, sign=SIGN_WALLET, msg=MSG_WALLET)
    while 1 != 0:
        caseNumber = int(input(helloContent))
        if caseNumber == 1:
            playGame(mtm.accessToken)
        if caseNumber == 2:
            marketGame(mtm.accessToken)
        if caseNumber == 0:
            exit()
