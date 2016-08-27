import re
import sys
import collections
#read in 2 deck files, print out their differences

deckpat = re.compile('(\d+)x?-?\s*(\w.*)')
notcard = re.compile('^\s*$')

def deck_to_dict(deck_path):
    deck_file = open(deck_path, 'r')
    deck = deck_file.readlines()
    deck_dict = collections.defaultdict(int)
    for line in deck:
        if notcard.match(line):
            continue
        m = deckpat.match(line)
        if m:
            deck_dict[m.groups()[1].lower()] =  int(m.groups()[0])
        else:
            deck_dict[line.lower()] = 1

    ##TODO collections.Counter(['Lightning Bolt','Lightning Bolt','Lightning Bolt'])
    # for if there are no nums

    return deck_dict
    #TODO detect sideboard

def dict_to_difflist(deck1, deck2):
    commondict = dict() #Bolt (d1, both, d2)

    for card in (deck1.viewkeys() | deck2.viewkeys()): #these are lists
        if deck1[card] == 0:
            commondict[card] = ('','',deck2[card])
        elif deck2[card] == 0:
            commondict[card] = (deck1[card],'','')
        elif deck1[card] > deck2[card]:
            diff = deck1[card] - deck2[card]
            common = deck2[card]
            commondict[card] = (diff,common,'')
        elif deck2[card] > deck1[card]:
            diff = deck2[card] - deck1[card]
            common = deck1[card]
            commondict[card] = ('',common,diff)
        else: #completely shared
            commondict[card] = ('',deck1[card],'')
    return commondict
        
def main(deck_paths):
    deck1 = deck_to_dict(deck_paths[0])
    deck2 = deck_to_dict(deck_paths[1])

    cd = dict_to_difflist(deck1, deck2)
    output_format = '%-30s|%-5s|%-5s|%-5s'
    print output_format % ('Card', 'Deck1', 'Both', 'Deck2')
    for card, (d1, both, d2) in cd.iteritems():
        #print '%-12i%-12i' % (10 ** i, 20 ** i)
        print output_format % (card, d1, both, d2)


if __name__ == '__main__':
    main(sys.argv[1:])

    
