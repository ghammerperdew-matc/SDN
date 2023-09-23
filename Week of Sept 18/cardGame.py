import requests

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

response = response.json()

deck_id = response["deck_id"]

print("Your deck is shuffled and ready. Your deck ID is: ", deck_id)


num_of_cards = input("Enter the number of cards you would like to draw: ")

url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" + num_of_cards

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

response = response.json()

print(response)

for card in response["cards"]:
    print(card["value"] + " of " + card["suit"])
