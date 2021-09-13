

def best(hand):
    boolSF, valSF = SFlush(hand)
    bool4, val4, kicker4 = Quads(hand)
    boolB, valB, kickerB = FullHouse(hand)
    boolF, valF = Flush(hand)
    boolS, valS = Straight(hand)
    bool3, val3, kicker3 = Trips(hand)
    bool2, val2, kicker2 = TwoPair(hand)
    boolP, valP, kickerP = Pair(hand)
    kicker = None
    print(boolSF, bool4, boolB, boolF, boolS, bool3, bool2, boolP)
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
        copyx = 0
        copy = hand.copy()
        for x in copy:
            num = x % 13
            if num > val:
                val = num
                copyx = x
        copy.remove(copyx)

        kicker = 0 # second high card
        for x in copy:
            num = x % 13
            if num > kicker:
                kicker = num

    return rank, val, kicker
    
def SFlush(hand):
    Sbool, val = Straight(hand)
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
    Tbool, val, kicker3 = Trips(hand)
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
    Tbool, val, useless = Trips(hand)
    if not Tbool:
        return False, None, None
    TwoBool, val2, kicker2 = TwoPair(hand)
    if not TwoBool:
        return False, None, None
    if val == val2:
        return True, val, kicker2
    return True, val, val2
    

def Flush(hand):
    board = hand[2:].copy()
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
    for i in hand:
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

def Trips(hand):
    copyHand = hand.copy()
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

def TwoPair(hand):
    copyHand = hand.copy()
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
        copyHand = [i for i in copyHand if i != val]
    if len(pairs) > 1:
        pairs.sort(reverse=True)
        return True, pairs[0], pairs[1]
    return False, None, None


def Pair(hand):
    copyHand = hand.copy()
    for i in range(len(copyHand)):
        copyHand[i] = (copyHand[i]) % 13
    new = []
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
        else:
            new.append(card)
    return False, None, None




hand1 = [0, 5, 13, 26, 51, 34, 50]  # 3 of a kind
hand1copy = hand1.copy()
hand2 = [2, 15, 12, 25, 38, 0, 5]  # full house
hand3 = [16, 18, 17, 9, 20, 35, 19]  # straight flush
hand4 = [0, 13, 26, 5, 18, 9, 22]  # broken full house



print(best(hand1))
#print(best(hand2))
#print(best(hand3))
#print(best(hand4))


