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
    

def input_cards():

    valid_number = False

    while valid_number == False:

        num_of_cards = input("Please enter the number of cards you wish to draw (1-5), or enter 0 to quit: ")

        if num_of_cards.isdigit():

            if int(num_of_cards) > 5 or int(num_of_cards) < 0:
                valid_number = False
                print("Invalid entry -- try again")
            else:
                valid_number = True

        else:
            valid_number = False
            print("Invalid entry -- try again")

    return num_of_cards


        


def main():

    end_game = False

    while end_game == False:

        play_game = input("Would you like to play a game of War? Enter Y or N: ")

        if play_game.lower() == "y":

            display_rules()

            num_of_decks = "1"

            deck_id = shuffle_deck(num_of_decks)

            print(deck_id)

            while end_game == False:

                #ask player how many cards to draw and validate response (0-5 are acceptable)
                num_of_cards = input_cards()

                if num_of_cards == "0":
                    print("GAME OVER")
                    end_game = True

                else:

                    user_cards = draw_cards(num_of_cards, deck_id)

                    cpu_cards = draw_cards(num_of_cards, deck_id)

                    user_score = calc_score(user_cards)

                    print("Player Score: ", user_score)

                    cpu_score = calc_score(cpu_cards)

                    print("Computer Score: ", cpu_score)

                    if user_score > cpu_score:
                        print("You win!\n\n")
                    elif user_score < cpu_score:
                        print("Computer wins!\n\n")
                    else:
                        print("The scores are tied!\n\n")

        elif play_game.lower() == "n":
            print("Closing program")
            end_game = True

        else:
            print("Invalid input - try again")
    



main()
        
