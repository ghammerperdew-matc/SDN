#import necessary libraries
import requests



def display_rules():
    print(
"""
--------------
Rules of War
--------------

Each player draws 1-5 cards.
The hands are then compared, and the hand with the highest total value wins.
If there is a draw, the game restarts

Card values for face cards are as follows:

Jack = 11
Queen = 12
King = 13
Ace = 14

"""
)


def shuffle_deck(num_of_decks):
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=" + num_of_decks

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    deck = response.json()
    deck_id = deck["deck_id"]

    return deck_id


def draw_cards(num_of_cards, deck_id):
    url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" + num_of_cards

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    cards = response.json()
    cards_drawn = cards["cards"]

    card_values = []
    for card in cards_drawn:
        card_values.append(card["value"])

    return card_values


def calc_score(cards):

    card_values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "JACK": 11,
        "QUEEN": 12,
        "KING": 13,
        "ACE": 14
        }

    total = 0
    for card in cards:
        total += card_values[card]

    return total


def main():
    
    
    
#ask user if they would like to play cards

    #if yes:

        display_rules()

        num_of_decks = "1"

        deck_id = shuffle_deck(num_of_decks)

        print(deck_id)

        #ask player how many cards to draw
        ##number_of_cards = input("")

        #if valid user input:

            #draw cards for the player

        num_of_cards = "5"
        user_cards = draw_cards(num_of_cards, deck_id)

        print(user_cards)

            #draw cards for cpu

            ##cpu_cards = draw_cards(number_of_cards, deck_id)

            #total hand scores

        user_score = calc_score(user_cards)

        print(user_score)

            ##cpu_score = calc_score(cpu_cards)

            #declare winner or tie

    #if no:



main()
        
