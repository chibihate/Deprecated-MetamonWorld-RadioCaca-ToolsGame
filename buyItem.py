import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ADDRESS_WALLET = os.getenv("ADDRESS_WALLET")


def buyOfficialSale(orderId):
    headers = {
        "accessToken": ACCESS_TOKEN,
    }
    payload = {"address": ADDRESS_WALLET}

    url = "https://metamon-api.radiocaca.com/usm-api/official-sale/buy?orderId="
    urlOrderID = f"{url}{orderId}"
    while 1 != 0:
        response = requests.request("POST", urlOrderID, headers=headers, data=payload)
        json = response.json()
        print(json.get("code", {}))


if __name__ == "__main__":
    helloContent = """
    Official sale 
    1. Purple Potion         - 111
    2. SR Stimulant          - 110
    3. R Stimulant           - 109
    4. N Stimulant           - 108
    5. Space Ticket          - 105
    6. Anti-Fatigue Potion   - 106
    0. Exit
    Please select you want to buy it
    """
    caseNumber = int(input(helloContent))
    if caseNumber == 1:
        buyOfficialSale("111")
    if caseNumber == 2:
        buyOfficialSale("110")
    if caseNumber == 3:
        buyOfficialSale("109")
    if caseNumber == 4:
        buyOfficialSale("108")
    if caseNumber == 5:
        buyOfficialSale("105")
    if caseNumber == 6:
        buyOfficialSale("106")
