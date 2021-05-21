import time
import random


class Dealer:
    def __init__(self, players):
        self.deck = self.shuffle()
        self.players = players

    def shuffle(self):
        handKey = int(round(time.time_ns()))
        handKey /= 100
        handKey %= 1000000000
        handKey = int(handKey)

        random.seed(handKey)
        numCards = 52
        cardsLeft = [1] * numCards
        deck = []
        for i in range(numCards):
            val = int(random.random() * 1000000000)
            card = val % (numCards-i)
            x = 0
            while x <= card:
                if cardsLeft[x] == 0:
                    card += 1
                x += 1
            cardsLeft[card] -= 1
            deck.append(card)
        return deck

    def deal(self):
        hands = []
        for i in range(self.players):
            playerHand = []
            playerHand.append(self.deck[i])
            playerHand.append(self.deck[i+self.players])
            hands.append(playerHand)
        for i in range(self.players):
            self.deck.pop(0)
            self.deck.pop(0)
        board = [self.deck[0], self.deck[1], self.deck[2], self.deck[4], self.deck[6]]
        return [hands, board]

class HandRanks:
    def __init__(self, hand):
        self.hand = hand

    def best(self):
        boolSF, valSF = self.SFlush()
        bool4, val4, kicker4 = self.Quads()
        boolB, valB, kickerB = self.FullHouse()
        boolF, valF = self.Flush()
        boolS, valS = self.Straight()
        bool3, val3, kicker3 = self.Trips()
        bool2, val2, kicker2 = self.TwoPair()
        boolP, valP, kickerP = self.Pair()
        kicker = None
        if boolSF:
            rank = 8
            val = valSF
        elif bool4:
            rank = 7
            val = val4
            kicker = kicker4
        elif boolB:
            rank = 6
            val = valB
            kicker = kickerB
        elif boolF:
            rank = 5
            val = valF
        elif boolS:
            rank = 4
            val = valS
        elif bool3:
            rank = 3
            val = val3
            kicker = kicker3
        elif bool2:
            rank = 2
            val = val2
            kicker = kicker2
        elif boolP:
            rank = 1
            val = valP
            kicker = kickerP
        else:
            rank = 0
            val = 0 # high card
            for x in self.hand:
                num = x % 13
                if num > val:
                    val = num
                    copyx = x
            copy = self.hand.copy()
            copy.remove(copyx)

            kicker = 0 # second high card
            for x in copy:
                num = x % 13
                if num > kicker:
                    kicker = num

        return rank, val, kicker

        
    def SFlush(self):
        Sbool, val = self.Straight()
        if not Sbool:
            return False, None
        cardList = [val, val+13, val+26, val+39]
        newList = []
        for top in cardList:
            if top in self.hand:
                newList.append(top)
        for card in newList:
            for i in range(5):
                if (card-i) not in self.hand:
                    return False, None
        return True, val  

    
    def Quads(self):
        Tbool, val, kicker3 = self.Trips()
        if not Tbool:
            return False, None, None
        if val in self.hand:
            if val+13 in self.hand:
                if val+26 in self.hand:
                    if val+39 in self.hand:
                        high = 0 # kicker
                        for x in self.hand:
                            num = x % 13
                            if num != val and num > high:
                                high = num
                        return True, val, high
        return False, None, None
    

    def FullHouse(self):
        Tbool, val, useless = self.Trips()
        if not Tbool:
            return False, None, None
        TwoBool, val2, kicker2 = self.TwoPair()
        if not TwoBool:
            return False, None, None
        if val == val2:
            return True, val, kicker2
        return True, val, val2


    def Flush(self):
        board = self.hand[2:].copy()
        suitCount = [0,0,0,0]
        boardCount = [0,0,0,0]
        for card in self.hand:
            suitCount[int(card/13)] += 1
        for card in board:
            boardCount[int(card/13)] += 1
        if max(suitCount) < 5:
            return False, None
        index = 0
        while suitCount[index] < 5:
            index += 1
        
        card1suit = int(self.hand[0] / 13)
        card2suit = int(self.hand[1] / 13)

        if card1suit == card2suit:
            higher = max([self.hand[0], self.hand[1]])
            if card1suit == index:
                if max(boardCount) < 5:
                    value = higher % 13
                elif min(board) < higher: # fix this so it only looks at the correct suits
                    value = higher % 13
                else:
                    value = min(board) % 13
            else:
                value = min(board) % 13

        elif card1suit == index:
            if max(boardCount) < 5:
                value = self.hand[0] % 13
            elif min(board) < self.hand[0]: # fix this so it only looks at the correct suits
                value = self.hand[0] % 13
            else:
                value = min(board) % 13
            
        elif card2suit == index:
            if max(boardCount) < 5:
                value = self.hand[1] % 13
            elif min(board) < self.hand[1]: # fix this so it only looks at the correct suits
                value = self.hand[1] % 13
            else:
                value = min(board) % 13 

        else:
            value = min(board) % 13

        return True, value


    def Straight(self):
        copyHand = []
        for i in self.hand:
            if i % 13 not in copyHand:
                copyHand.append(i%13)
        copy2 = copyHand.copy() # we're going to make aces low in this copy
        for i in range(len(copy2)):
            copy2[i] = (copy2[i] + 1) % 13
    
        while len(copyHand) >= 5:
            high = max(copyHand)
            if high -1 in copyHand and high -2 in copyHand and high -3 in copyHand and high -4 in copyHand:
                return True, high
            copyHand.remove(high)
            
        if 0 in copy2 and 1 in copy2 and 2 in copy2 and 3 in copy2 and 4 in copy2:
            return True, 3

        return False, None

    def Trips(self):
        copyHand = self.hand.copy()
        for i in range(len(copyHand)):
            copyHand[i] = (copyHand[i]) % 13
        copyHand.sort(reverse=True)
        kicker = 0
        while len(copyHand) > 2:
            val = copyHand[0]
            count = 0
            for card in copyHand:
                if card == val:
                    count += 1
            if count > 2:
                copyHand.remove(copyHand[0])
                kicker = max(copyHand + [kicker])
                return True, val, kicker
            kicker = max([kicker] + [copyHand[0]])
            copyHand.remove(copyHand[0])
        
        return False, None, None

    def TwoPair(self):
        copyHand = self.hand.copy()
        for i in range(len(copyHand)):
            copyHand[i] = copyHand[i] % 13
        pairs = []
        while len(copyHand) > 1:
            val = copyHand[0]
            count = 0
            for card in copyHand:
                if card == val:
                    count += 1
            if count > 1:
                pairs.append(val)
            copyHand = [i for i in copyHand if i != val] # replace all .remove() with this
        if len(pairs) > 1:
            pairs.sort(reverse=True)
            return True, pairs[0], pairs[1]
        return False, None, None

    def Pair(self):
        copyHand = self.hand.copy()
        for i in range(len(copyHand)):
            copyHand[i] = copyHand[i] % 13
        new = []
        for card in copyHand:
            if card in new:
                if (self.hand[0] % 13) == card:
                    if (self.hand[1] % 13) == card:
                        kicker = None
                    else:
                        kicker = self.hand[1] % 13
                elif (self.hand[1] % 13) == card:
                    kicker = self.hand[0] % 13
                else:
                    kicker = max([(self.hand[0] % 13), (self.hand[1] % 13)])
                return True, card, kicker
            else:
                new.append(card)
        return False, None, None
            
        

## look through all rankings and make sure kicker is high card FROM HAND if its a single card
# fix full house if 3 pair and trips on the lowest pair 2,2,2,5,5,9,9 (example that breaks it)


players = 2
game = Dealer(players)
hands = game.deal()
board = hands[1]
for i in range(players):
    hand = [hands[0][0] + board]
    hands.append(hand)
    hands[0].pop(0)
hands.pop(0)
hands.pop(0)

for x in range(len(hands)):
    hands[x] = hands[x][0]


print(hands)
ranks = []
for x in hands:
    hand = HandRanks(x)
    ranks.append(hand.best())

print(ranks)

#print(hand4.best())