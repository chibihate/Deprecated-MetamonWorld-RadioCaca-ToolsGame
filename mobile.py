import market
import play
import json
import requests

ADDRESS_WALLET = "your_ADDRESS_WALLET"
SIGN_WALLET = "your_ADDRESS_WALLET"
MSG_WALLET = "your_MSG_WALLET"

# URLs to make api calls
BASE_URL = "https://metamon-api.radiocaca.com/usm-api"


class MetamonPlayer:
    def __init__(self, address, sign, msg):
        self.accessToken = ""
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

    def post_data(self, url, payload):
        return json.loads(
            requests.Session().post(url, data=payload, headers=self.headers).text
        )

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


def playGame(accessToken):
    mtm = play.MetamonPlayer(address=ADDRESS_WALLET, accessToken=accessToken)
    helloContent = """
    1. Battle in Island
    2. Mint eggs
    3. Up attribute all monsters   
    4. Join the best squad in Lost world
    5. Battle record in Lost world
    6. Get status my teams in Lost world
    0. Exit
    Please select you want to choose
    """
    addAttrContent = """
    1. Manual
    2. Automatic
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
                mtm.startBattleIsland(1)
                continue
            if caseNumber == 2:
                mtm.startBattleIsland(2)
                continue
            if caseNumber == 3:
                mtm.startBattleIsland(3)
                continue
            if caseNumber == 4:
                mtm.startBattleIsland(4)
                continue
            if caseNumber == 0:
                continue
        if caseNumber == 2:
            mtm.mintEgg()
        if caseNumber == 3:
            caseNumber = int(input(addAttrContent))
            if caseNumber == 1:
                mtm.addAttrAllMetamon()
                continue
            if caseNumber == 2:
                mtm.autoAddAttrAllMetamon()
                continue
            if caseNumber == 0:
                continue
        if caseNumber == 4:
            mtm.joinTheBestSquad()
        if caseNumber == 5:
            mtm.battleRecord()
        if caseNumber == 6:
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
    7. Withdraw
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
                continue
            if caseNumber == 2:
                mtm.shoppingWithSetPrice()
                continue
            if caseNumber == 0:
                continue
        if caseNumber == 3:
            caseNumber = int(input(shellingContent))
            if caseNumber == 1:
                mtm.shelling(caseNumber)
                continue
            if caseNumber == 2:
                mtm.shelling(caseNumber)
                continue
            if caseNumber == 0:
                continue
        if caseNumber == 4:
            mtm.canceling()
        if caseNumber == 5:
            mtm.buyDrops()
        if caseNumber == 6:
            mtm.transactionHistory()
        if caseNumber == 7:
            mtm.withdrawRACA()
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
