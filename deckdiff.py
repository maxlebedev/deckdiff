import re
import sys
import collections
#read in 2 deck files, print out their differences

deckpat = re.compile('(\d+)x?-?\s*(\w.*)')
notcard = re.compile('^\s*$')

def deck_to_dict(deck):
    deck_dict = collections.defaultdict(int)
    for line in deck:
        if notcard.match(line):
            continue
        m = deckpat.match(line)
        if m:
            deck_dict[m.groups()[1].lower()] =  int(m.groups()[0])
        else:
            deck_dict[line.lower()] = 1
    return deck_dict

def dict_to_difflist(deck1, deck2):
    commondict = dict() #tuple format (d1, both, d2)

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


def split_by_section(deck): #main, sideboard, etc
    deck_parts = []
    for line in deck:
	if line.endswith(':\n'):
	    deck_parts.append((line[:-2], list()))
	else:
            if not deck_parts:
                deck_parts = [('Main',list())]#default for titleless decks
	    deck_parts[-1][1].append(line)

    return deck_parts
	
def main(deck_paths):
     #TODO add option to not split by section
    deck1_parts = split_by_section(open(deck_paths[0], 'r').readlines())
    deck2_parts = split_by_section(open(deck_paths[1], 'r').readlines())

    # determine max space needed
    max_space = max(len(max([x[0] for x in deck1_parts], key=len)), len(max([y[0] for y in deck2_parts], key=len)))+1
    output_format = '%-30s|%-{0}s|%-5s|%-{0}s'.format(max_space, max_space) #dumb formatting

    tot1 = 0
    tot_both = 0
    tot2 = 0

    for (title1, deck1), (title2, deck2) in zip(deck1_parts, deck2_parts):
        if not deck1 and not deck2:
            continue
        if title1 == title1:
            title1 += '1'
            title2 += '2'
	deck1 = deck_to_dict(deck1)
	deck2 = deck_to_dict(deck2)
        cd = dict_to_difflist(deck1, deck2)

        print output_format % ('Card', title1, 'Both', title2)
        for card, (d1, both, d2) in cd.iteritems():
            print output_format % (card, d1, both, d2)
            tot1 += int(d1 or 0)
            tot_both += int(both or 0)
            tot2 += int(d2 or 0)
        
    print 'Deck1 total:', tot1, 'Both total', tot_both, 'Deck2 total', tot2

if __name__ == '__main__':
    main(sys.argv[1:])

