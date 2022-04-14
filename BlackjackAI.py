import random
import matplotlib.pyplot as plt


def totalling(lis):
    total = 0
    aces = 0
    for card in lis:
        if card[0] == "j" or card[0] == "q" or card[0] == "k":
            total += 10
        elif card[0] == "a":
            total += 1
            aces += 1
        else:
            total += card[0]
            
    for i in range(aces):
        if total + 10 <= 21:
            total += 10
    return total

def draw_cards(n):
    dealing = []
    for i in range(n):
        dealing.append(random.choice(deck))
        deck.remove(dealing[len(dealing)-1])
    return dealing
    
def unused_ace(lis):
    lis2 = []
    for c in lis:
        if c[0] == 'a':
            lis2.append([1,c[1]])
        else:
            lis2.append(c)
    return totalling(lis) != totalling(lis2)

def update_AI(c, a, sw, s, hb, h):
    for lis in AI:
        if lis[0] == c and lis[1] == a:
            l = lis
            break
    l[2] += sw
    l[3] += s
    l[4] += hb
    l[5] += h
            


cards = []
for suit in ["heart","spade","club","diamond"]:
    for num in range(2,11):
        cards.append([num, suit])
    for spec in ["a","j","q","k"]:
        cards.append([spec, suit])
        
deck = []
for card in cards:
    deck.append(card)
    
    
AI = [] #lists order is [total card value, is an ace unused? (boolean), # of times standing wins, # of times stood, # of times hitting doesnt bust, # of times hit]
for i in range(4, 22):
    AI.append([i, False, 0, 1, 0, 1])
    AI.append([i, True, 0, 1, 0, 1])

for x in range(100000):
    dealer = []
    dealer.extend(draw_cards(1))

    player = []
    player.extend(draw_cards(2))

    while(True):
        if bool(random.randint(0,1)): #1/true means hit
            current = totalling(player)
            ace = unused_ace(player)
            player.extend(draw_cards(1))
            if(totalling(player) >= 21):
                break
            update_AI(current, ace, 0, 0, 1, 1)
            
        else: #else stand
            break


    if(totalling(player) == 21):
        update_AI(totalling(player), unused_ace(player), 1, 1, 0, 0) #player has blackjack, wins
    elif(totalling(player) > 21):
        update_AI(current, ace, 0, 0, 0, 1) #player busts
    else:
        while(totalling(dealer) < 17):
            dealer.extend(draw_cards(1))
        
        if(totalling(dealer) > 21):
            update_AI(totalling(player), unused_ace(player), 1, 1, 0, 0) #dealer bust
        else:
            if(totalling(dealer) < totalling(player)):
                update_AI(totalling(player), unused_ace(player), 1, 1, 0, 0) #player wins
            elif(totalling(dealer) > totalling(player)):
                update_AI(totalling(player), unused_ace(player), 0, 1, 0, 0) #dealer wins
            else:
                update_AI(totalling(player), unused_ace(player), 1, 1, 0, 0) #tie (player wins)
    
    deck.clear()
    for card in cards:
        deck.append(card)
        
print("Read as, card total, whether an ace worth 11 is present, percentage of standing wins, percentage of hitting not loosing")
print(AI)

x = []
sy = []
hy = []
for choice in AI:
    if(choice[1] == False):
        x.append(choice[0])
        sy.append(choice[2]/choice[3])
        hy.append(choice[4]/choice[5])
    
plt.plot(x, sy, color='green', label='stand wins')
plt.plot(x, hy, color='red', label='hit not busting')
plt.xticks(range(4, 22))
plt.legend()
plt.show()



