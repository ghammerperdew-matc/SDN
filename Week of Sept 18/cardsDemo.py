import requests

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

deck = response.json()
deck_id = deck["deck_id"]


print(response)
print(deck_id)



url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=3"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

cards = response.json()
cards_drawn = cards["cards"]

print(response)
print(cards_drawn)

for card in cards_drawn:
    print(card["value"], "of", card["suit"])

