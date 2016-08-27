import re
import sys
#read in 2 deck files, print out their differences

deckpat = re.compile('(\d+)x?-?\s*(\w.*)')
notcard = re.compile('^\s*$')

def deck_to_dict(deck_path):
    deck_file = open(deck_path, 'r')
    deck = deck_file.readlines()
    deck_dict = dict()
    for line in deck:
        if notcard.match(line):
            continue
        m = deckpat.match(line)
        if m:
            deck_dict[m.groups()[1].lower()] =  int(m.groups()[0])
        else:
            deck_dict[line.lower()] = 1

    ##collections.Counter(['Lightning Bolt','Lightning Bolt','Lightning Bolt'])
    # for if there are no nums

    return deck_dict
    #TODO detect sideboard
        
#TODO maybe use counter instead of dict
def main(deck_paths):
    deck1 = deck_to_dict(deck_paths[0])
    deck2 = deck_to_dict(deck_paths[1])
    difflist1 = []
    difflist2 = []
    ###commondict = dict() #Bolt (1, both, 2)
    for card in deck1.keys():
        if card in deck2:
            diff = deck1[card] - deck2[card]
            if diff>0:
                difflist1.append((diff, card))
        else:
            difflist1.append((deck1[card], card))

    for card in deck2.keys():
        if card in deck1:
            diff = deck2[card] - deck1[card]
            if diff>0:
                difflist2.append((diff, card))
        else:
            difflist2.append((deck2[card], card))

    for i in difflist1:
        print 'deck1 :',i

    for i in difflist2:
        print 'deck2 :',i

if __name__ == '__main__':
    main(sys.argv[1:])

    
def dict_to_difflist(dict1, dict2):
    return 0


