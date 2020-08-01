import random
import time

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

# cards imported from http://svg-cards.sourceforge.net/


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    extension = 'png'
    # if tkinter.TkVersion >= 8.6:
    #     extension = 'png'
    # else:
    #     extension = 'ppm'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first, the number cards
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)
    # add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def _score_hand(hand):
    # Calculate the total score of all cards in the list:
    # only one ace can be 11, reduce to 1 if the hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # check for bust, then for ace
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def _deal_dealer():
    global result_text
    dealer_score = _score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = _score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = _score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer Wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player Wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer Wins")
    else:
        result_text.set("It's a push!")


def _deal_player():
    player_hand.append(_deal_card(player_card_frame))
    player_score = _score_hand(player_hand)
    player_score_label.set(_score_hand(player_hand))

    if player_score > 21:
        result_text.set("Dealer Wins!")
    # if player_score == 21:
    #     result_text.set("Blackjack! Player wins!")
    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     card_value = 11
    #     player_ace = True
    # player_score += card_value
    # # if we bust, check to see if there's an ace and subract
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set('Dealer Wins!')


def _new_game():
    global dealer_hand
    global player_hand
    global dealer_card_frame
    global player_card_frame
    global card_frame
    global player_score_label
    global dealer_score_label
    global main_window
    global result_text

    player_hand = []
    dealer_hand = []
    card_frame.destroy()
    result_text.set('')
    card_frame = tkinter.Frame(main_window, relief="sunken", borderwidth=1, background='green')
    card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

    dealer_score_label = tkinter.IntVar()
    tkinter.Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
    tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
    # embedded frame hold the card images

    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    player_score_label = tkinter.IntVar()
    tkinter.Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
    tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

    # embedded frame to hold the card images

    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    if len(deck) < 12:
        shuffle()
    # card_frame.Destroy()
    # build_card_frame()
    _deal_player()
    # time.sleep(3)
    dealer_hand.append(_deal_card(dealer_card_frame))
    # time.sleep(1)
    dealer_score_label.set(_score_hand(dealer_hand))
    _deal_player()
    player_score_label.set(_score_hand(player_hand))


def shuffle():
    global result_text
    global cards
    global deck
    global result
    for i in range(0,3):
        deck += list(cards)
    random.shuffle(deck)
    result_text.set('Shuffling Cards')
    result.update()
    time.sleep(3)



def build_window():
    global main_window
    global card_frame
    global button_frame
    global result_text
    global dealer_score_label
    global player_score_label
    global dealer_card_frame
    global player_card_frame
    global button_frame
    global dealer_button
    global player_button
    global new_game_button
    global result
    main_window = tkinter.Tk()
    main_window.title('Blackjack')
    main_window.geometry('640x480-20-200')
    main_window.configure(background='green')

    result_text = tkinter.StringVar()
    result = tkinter.Label(main_window, textvariable=result_text)
    result.grid(row=0, column=0, columnspan=3)

    card_frame = tkinter.Frame(main_window, relief="sunken", borderwidth=1, background='green')
    card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

    dealer_score_label = tkinter.IntVar()
    tkinter.Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
    tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
    # embedded frame hold the card images

    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    player_score_label = tkinter.IntVar()
    tkinter.Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
    tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

    # embedded frame to hold the card images

    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    button_frame = tkinter.Frame(main_window)
    button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

    dealer_button = tkinter.Button(button_frame, text='Dealer', command=_deal_dealer)
    dealer_button.grid(row=0, column=0)

    player_button = tkinter.Button(button_frame, text='Player', command=_deal_player)
    player_button.grid(row=0, column=1)

    new_game_button = tkinter.Button(button_frame, text="New Game", command=_new_game)
    new_game_button.grid(row=0, column=2)



def play():
    global cards
    global deck
    # load cards
    build_window()
    cards = []
    load_images(cards)
    # dealer_hand = []
    # player_hand = []

    # print(cards)

    # Create a new deck of cards and shuffle them
    deck = list(cards)
    random.shuffle(deck)

    # # create the list to store dealer's and player's hands
    # deal_player()
    # # time.sleep(3)
    # dealer_hand.append(deal_card(dealer_card_frame))
    # # time.sleep(1)
    # dealer_score_label.set(score_hand(dealer_hand))
    # deal_player()
    _new_game()

    main_window.mainloop()
# __name__ = "__main__"

if __name__ == "__main__":
    play()
