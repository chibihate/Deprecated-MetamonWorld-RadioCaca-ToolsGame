import requests
import os
import telebot
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()

ADDRESS_WALLET = os.getenv("ADDRESS_WALLET")
SIGN_WALLET = os.getenv("SIGN_WALLET")
MSG_WALLET = os.getenv("MSG_WALLET")
API_TELEGRAM = os.getenv("API_TELEGRAM")
CHAT_GROUP_ID = os.getenv("CHAT_GROUP_ID")

bot = telebot.TeleBot(API_TELEGRAM)

BASE_URL = "https://metamon-api.radiocaca.com/usm-api"
TOKEN_URL = f"{BASE_URL}/login"
SHOP_ORDER_URL = f"{BASE_URL}/shop-order"
SELL_LIST_URL = f"{SHOP_ORDER_URL}/sellList"

types = {
    "Egg": "6",
    "Potion": "2",
    "Yellow_Diamond": "3",
    "Purple_Diamond": "4",
    "Valhalla": "8",
    "Space_Ticket": "7",
    "Purple_Potion": "10",
    "Anti_Fatigue_Potion": "11",
    "N_Stimulant": "12",
    "R_Stimulant": "13",
    "SR_Stimulant": "14",
    "Villa_Fragments": "1015",
    "Mansion_Fragments": "1016",
    "Castle_Fragments": "1017",
    "Donuts": "1004",
}
orderType = {
    "LowestPrice": "2",
    "HighestPrice": "-2",
    "LowestTotalPrice": "3",
    "HighestTotalPrice": "-3",
}


def getAccessToken():
    payload = {
        "address": ADDRESS_WALLET,
        "sign": SIGN_WALLET,
        "msg": MSG_WALLET,
        "network": "1",
        "clientType": "MetaMask",
    }
    response = requests.request("POST", TOKEN_URL, data=payload)
    json = response.json()
    return json.get("data").get("accessToken")


def getLowestPrice(headers, type):
    response = requests.request(
        "POST",
        SELL_LIST_URL,
        headers=headers,
        data={
            "address": ADDRESS_WALLET,
            "type": types[type],
            "orderType": orderType["LowestPrice"],
            "orderId": "-1",
            "pageSize": "1",
        },
    )
    json = response.json()
    return json.get("data").get("orderAmount")


def getPriceItems():
    priceItems = {}
    headers = {
        "accessToken": getAccessToken(),
    }
    for type in types:
        priceItems[type] = getLowestPrice(headers, type)
    return priceItems


def getScoreGroupInKingdom():
    headers = {
        "accessToken": getAccessToken(),
    }
    url = "https://metamon-api.radiocaca.com/usm-api/kingdom/teamList"
    totalSca = []
    monsterNum = []
    nameGroup = []
    idGroup = []

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data={
            "address": ADDRESS_WALLET,
            "teamId": -1,
            "pageSize": 100,
        },
    )
    json = response.json()
    listGroup = json.get("data").get("list")
    for i in range(len(listGroup)):
        if int(listGroup[i]["monsterNum"]) >= 100:
            totalSca.append(listGroup[i]["totalSca"])
            monsterNum.append(listGroup[i]["monsterNum"])
            nameGroup.append(listGroup[i]["name"])
            idGroup.append(listGroup[i]["id"])
    tableItems = PrettyTable()
    tableItems.field_names = [
        "Score average",
        "Monster number",
        "ID group",
        "Group name",
    ]
    tableItems.align["Score average"] = "r"
    tableItems.align["Monster number"] = "r"
    tableItems.align["ID"] = "r"
    tableItems.align["Group"] = "l"

    for i in range(len(totalSca)):
        tableItems.add_row(
            [
                round(int(totalSca[i]) / int(monsterNum[i])),
                monsterNum[i],
                idGroup[i],
                nameGroup[i],
            ]
        )
    return tableItems


def getEarnRacaOfficialSale():
    headers = {
        "accessToken": getAccessToken(),
    }
    price_Valhalla_10_Items = int(getLowestPrice(headers, "Valhalla"))
    price_Valhalla_1_Item = price_Valhalla_10_Items / 10
    price_Purple_Potion = int(getLowestPrice(headers, "Purple_Potion"))
    price_Anti_Fatigue_Potion = int(getLowestPrice(headers, "Anti_Fatigue_Potion"))
    price_N_Stimulant = int(getLowestPrice(headers, "N_Stimulant"))
    price_R_Stimulant = int(getLowestPrice(headers, "R_Stimulant"))
    price_SR_Stimulant = int(getLowestPrice(headers, "SR_Stimulant"))
    price_Space_Ticket = int(getLowestPrice(headers, "Space_Ticket"))

    earn_Purple_Potion = round(price_Purple_Potion - price_Valhalla_1_Item * 4)
    earn_Anti_Fatigue_Potion = round(
        price_Anti_Fatigue_Potion - price_Valhalla_1_Item * 4
    )
    earn_N_Stimulant = round(price_N_Stimulant - price_Valhalla_10_Items)
    earn_R_Stimulant = round(price_R_Stimulant - price_Valhalla_10_Items * 2)
    earn_SR_Stimulant = round(price_SR_Stimulant - price_Valhalla_10_Items * 3)
    earn_Space_Ticket = round(price_Space_Ticket - price_Valhalla_10_Items * 2)

    tableItems = PrettyTable()
    tableItems.field_names = ["Item", "Earn", "ROI"]
    tableItems.align["Item"] = "l"
    tableItems.align["Earn"] = "r"
    tableItems.align["ROI (%)"] = "r"
    tableItems.add_row(
        [
            "Purple Poition",
            earn_Purple_Potion,
            round(earn_Purple_Potion / (price_Valhalla_1_Item * 4) * 100),
        ]
    )
    tableItems.add_row(
        [
            "SR Stimulant",
            earn_SR_Stimulant,
            round(earn_SR_Stimulant / (price_Valhalla_10_Items * 3) * 100),
        ]
    )
    tableItems.add_row(
        [
            "R Stimulant",
            earn_R_Stimulant,
            round(earn_R_Stimulant / (price_Valhalla_10_Items * 2) * 100),
        ]
    )
    tableItems.add_row(
        [
            "N Stimulant",
            earn_N_Stimulant,
            round(earn_N_Stimulant / price_Valhalla_10_Items * 100),
        ]
    )
    tableItems.add_row(
        [
            "Space Ticket",
            earn_Space_Ticket,
            round(earn_Space_Ticket / (price_Valhalla_10_Items * 2) * 100),
        ]
    )
    tableItems.add_row(
        [
            "Anti-Fatigue Potion",
            earn_Anti_Fatigue_Potion,
            round(earn_Anti_Fatigue_Potion / (price_Valhalla_1_Item * 4) * 100),
        ]
    )
    return tableItems


def getEarnRacaInGame():
    headers = {
        "accessToken": getAccessToken(),
    }
    fee_Island = 200
    price_Egg = int(getLowestPrice(headers, "Egg"))
    price_Valhalla = int(getLowestPrice(headers, "Valhalla")) / 10
    price_Purple_Poition = int(getLowestPrice(headers, "Purple_Potion"))
    price_Poition = int(getLowestPrice(headers, "Potion"))
    earnIslandLessThan60 = round(price_Egg * 75 / 100 - fee_Island - price_Poition)
    earnIslandLv60 = round(
        price_Egg * 75 / 100
        + price_Purple_Poition
        - fee_Island
        - price_Poition
        - price_Valhalla * 4
    )
    earnLW_Win = round(
        price_Valhalla * 5 + price_Purple_Poition - price_Poition - price_Valhalla * 4
    )
    earnLW_Lose = round(
        price_Valhalla + price_Purple_Poition - price_Poition - price_Valhalla * 4
    )
    resultContent = "---------- Metamon Island ----------\n"
    resultContent = (
        resultContent + f"Earn per mon less than lv 60: {earnIslandLessThan60}\n"
    )
    resultContent = resultContent + f"Earn per mon lv 60: {earnIslandLv60}\n\n"
    resultContent = resultContent + "---------- Last world ----------\n"
    resultContent = resultContent + f"Earn when pet win: {earnLW_Win}\n"
    resultContent = resultContent + f"Earn when pet lose: {earnLW_Lose}"
    return resultContent


def getPriceMarketInGame():
    url = f"https://api.telegram.org/bot{API_TELEGRAM}/sendMessage"
    while 1 != 0:
        tableItems = PrettyTable()
        tableItems.field_names = ["Item", "Price"]
        tableItems.align["Item"] = "l"
        tableItems.align["Price"] = "r"
        priceItems = getPriceItems()
        for type in types:
            tableItems.add_row([type, priceItems[type]])
        print(tableItems)
        # outputContent = "```\n" + str(tableItems) + "\n```"
        # response = requests.request(
        #     "POST",
        #     url,
        #     data={
        #         "chat_id": CHAT_GROUP_ID,
        #         "text": outputContent,
        #         "parse_mode": "Markdown",
        #     },
        # )
        # time.sleep(10)


if __name__ == "__main__":
    helloContent = """
    1. Check price in the market
    2. Check earn raca in game
    3. Check earn raca official sale
    4. Check group score
    0. Exit
    Please select you want to choose
    """
    caseNumber = int(input(helloContent))
    if caseNumber == 1:
        getPriceMarketInGame()
    if caseNumber == 2:
        print(getEarnRacaInGame())
    if caseNumber == 3:
        print(getEarnRacaOfficialSale())
    if caseNumber == 4:
        print(getScoreGroupInKingdom())
