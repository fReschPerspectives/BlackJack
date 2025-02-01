import random
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    
    # Load the card images into a dictionary
    for suit in suits:
        for card in range(1, 11):
            name = 'cards/{}_{}.png'.format(str(card), suit)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))
        for card in face_cards:
            name = 'cards/{}_{}.png'.format(str(card), suit)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def deal_card(frame, hand):
    # pop the next card off the top of the deck
    next_card = deck.pop()
    hand.append(next_card)
    # add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # return the card's face value
    return next_card


def score_hand(hand):
    ace = False
    score_corrected = False
    score = 0
    for card in hand:
        if card[0] == 1 and not ace:
            ace = True
            card = (11, card[1])
        score += card[0]
        if score > 21 and ace and not score_corrected:
            score -= 10
            score_corrected = True
    return score


def busts(score):
    return score > 21


def deal_dealer(initial_deal=False):
    stop_criteria = 17
    global dealer_score
    if initial_deal:
        deal_card(dealer_card_frame, dealer_hand)
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)
        if dealer_score >= 17:
            dealer_button["state"] = "disabled"
    while not initial_deal and score_hand(dealer_hand) < stop_criteria:
        deal_card(dealer_card_frame, dealer_hand)
        dealer_score = score_hand(dealer_hand)
        print(dealer_score)
        busted = busts(dealer_score)
        print(busted)
        if busted or dealer_score >= 17:
            dealer_score_label.set("Dealer Busted")
            dealer_button["state"] = "disabled"
        else:
            dealer_score_label.set(dealer_score)
        


def deal_player():
    deal_card(player_card_frame, player_hand)
    global player_score; player_score = score_hand(player_hand)
    print(player_score)
    busted = busts(player_score)
    print(busted)
    if busted:
        player_score_label.set("Player Busted")
        player_button["state"] = "disabled"
    else:
        player_score_label.set(player_score)


def setup_game():
    global dealer_hand
    global player_hand
    global dealer_card_frame
    global player_card_frame
    #destroy the card frames if they already exist
    dealer_card_frame.destroy()
    player_card_frame.destroy()
    # create the card frames
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
    # reset the dealer and player hands
    result_text.set("")
    dealer_hand = []
    player_hand = []

    deal_player()
    deal_dealer(True)
    deal_player()
    deal_dealer(True)


# Setup the screen and frames for the dealer and player
mainwindow = tkinter.Tk()
mainwindow.title("Black Jack")
mainwindow.geometry("640x480")
mainwindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainwindow, textvariable=result_text)

card_frame = tkinter.Frame(mainwindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', rowspan=2, columnspan=3)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)
# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tkinter.Frame(mainwindow)
button_frame.grid(row=3, column=0, sticky='w', columnspan=3)

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=setup_game)
new_game_button.grid(row=0, column=2)

# load cards
cards = []
load_images(cards)

# Create a new deck of cards and shuffle them
deck = list(cards)
random.shuffle(deck)


# Create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []



mainwindow.update()
mainwindow.mainloop()

