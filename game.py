import time
import random

hand1 = [0, 5, 22, 26, 51, 34, 50]  # 1 pair
hand2 = [2, 15, 12, 25, 38, 0, 5]  # full house
hand3 = [16, 18, 17, 9, 20, 35, 19]  # straight flush
hand4 = [0, 13, 26, 5, 18, 9, 22]  # broken full house

print(hand1.best)

class CreateDeck:
    def shuffle():
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

class HandRanks:
    def best(hand):
        boolSF, valSF = HandRanks.SFlush(hand)
        bool4, val4, kicker4 = HandRanks.Quads(hand)
        boolB, valB, kickerB = HandRanks.FullHouse(hand)
        boolF, valF = HandRanks.Flush(hand)
        boolS, valS = HandRanks.Straight(hand)
        bool3, val3, kicker3 = HandRanks.Trips(hand)
        bool2, val2, kicker2 = HandRanks.TwoPair(hand)
        boolP, valP, kickerP = HandRanks.Pair(hand)
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
            for x in hand:
                num = x % 13
                if num > val:
                    val = num
            copy = hand
            copy.remove(val)

            kicker = 0 # second high card
            for x in copy:
                num = x % 13
                if num > kicker:
                    kicker = num

        return rank, val, kicker
        
    def SFlush(hand):
        Sbool, val = HandRanks.Straight(hand)
        if not Sbool:
            return False, None
        cardList = [val, val+13, val+26, val+39]
        newList = []
        for top in cardList:
            if top in hand:
                newList.append(top)
        for card in newList:
            for i in range(5):
                if (card-i) not in hand:
                    return False, None
        return True, val  
    
    def Quads(hand):
        Tbool, val, kicker3 = HandRanks.Trips(hand)
        if not Tbool:
            return False, None, None
        if val in hand:
            if val+13 in hand:
                if val+26 in hand:
                    if val+39 in hand:
                        high = 0 # kicker
                        for x in hand:
                            num = x % 13
                            if num != val and num > high:
                                high = num
                        return True, val, high
        return False, None, None
    
    def FullHouse(hand):
        Tbool, val, useless = HandRanks.Trips(hand)
        if not Tbool:
            return False, None
        TwoBool, val2, kicker2 = HandRanks.TwoPair(hand)
        if not TwoBool:
            return False, None
        if val == kicker2:
            return True, kicker2, val2
        if val == val2:
            return True, val, kicker2
        return True, val, val2
        
        
        """
        countVal2 = 0
        if val2 in hand:
            countVal2 += 1
        if (val2+13) in hand:
            countVal2 += 1
        if (val2+26) in hand:
            countVal2 += 1
        if (val2+39) in hand:
            countVal2 += 1
        if countVal2 == 3 and val2 > val:
            return True, val2, val
"""


    def Flush(hand):
        board = hand[2:]
        suitCount = [0,0,0,0]
        boardCount = [0,0,0,0]
        for card in hand:
            suitCount[int(card/13)] += 1
        for card in board:
            boardCount[int(card/13)] += 1
        if max(suitCount) < 5:
            return False, None
        index = 0
        while suitCount[index] < 5:
            index += 1
        
        card1suit = int(hand[0] / 13)
        card2suit = int(hand[1] / 13)

        if card1suit == card2suit:
            higher = max([hand[0], hand[1]])
            if card1suit == index:
                if max(boardCount) < 5:
                    value = higher % 13
                elif min(board) < higher:
                    value = higher % 13
                else:
                    value = min(board) % 13
            else:
                value = min(board) % 13

        elif card1suit == index:
            if max(boardCount) < 5:
                value = hand[0] % 13
            elif min(board) < hand[0]:
                value = hand[0] % 13
            else:
                value = min(board) % 13
            
        elif card2suit == index:
            if max(boardCount) < 5:
                value = hand[1] % 13
            elif min(board) < hand[1]:
                value = hand[1] % 13
            else:
                value = min(board) % 13 

        else:
            value = min(board) % 13

        return True, value


    def Straight(hand):
        copyHand = []
        for i in range(len(hand)):
            if i % 13 not in copyHand:
                copyHand.append(i%13)
        copy2 = copyHand # we're going to make aces low in this copy
        for i in range(len(copy2)):
            copy2[i] = (copy2[i] + 1) % 13
    
        while len(copyHand) >= 5:
            high = max(copyHand)
            if high -1 in copyHand and high -2 in copyHand and high -3 in copyHand and high -4 in copyHand:
                return True, high
            copyHand.remove(high)
            
        if 0 in copy2 and 1 in copy2 and 2 in copy2 and 3 in copy2 and 4 in copy2:
            return True, 5

        return False, None

    def Trips(hand):
        copyHand = hand
        for i in range(len(copyHand)):
            copyHand[i] = (copyHand[i] + 1) % 13
        copyHand.sort(reverse=True)
        kicker = 0
        while len(copyHand > 2):
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

    def TwoPair(hand):
        copyHand = hand
        for i in range(len(copyHand)):
            copyHand[i] = (copyHand[i] + 1) % 13
        pairs = []
        while len(copyHand > 1):
            val = copyHand[0]
            count = 0
            for card in copyHand:
                if card == val:
                    count += 1
            if count > 1:
                pairs.append(val)
            copyHand.remove(copyHand[0])
        if len(pairs) > 1:
            pairs.sort(reverse=True)
            return True, pairs[0], pairs[1]

    def Pair(hand):
        copyHand = hand
        for i in range(len(copyHand)):
            copyHand[i] = (copyHand[i] + 1) % 13
        new = []
        high = 0
        for card in copyHand:
            if card in new:
                if (hand[0] % 13) == card:
                    if (hand[1] % 13) == card:
                        kicker = None
                    else:
                        kicker = hand[1] % 13
                elif (hand[1] % 13) == card:
                    kicker = hand[0] % 13
                else:
                    kicker = max([(hand[0] % 13), (hand[1] % 13)])
                return True, card, kicker
            copyHand.remove(card)
        return False, None, None
            
        

## look through all rankings and make sure kicker is high card FROM HAND if its a single card
# fix full house if 3 pair and trips on the lowest pair 2,2,2,5,5,9,9 (example that breaks it)