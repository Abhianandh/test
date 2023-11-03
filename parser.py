import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> PART | PART Conj PART
PART -> NP VP | NP Adv VP | VP
NP -> N | NA N 
NA -> Det | Adj | NA NA
VP -> V | V SUPP
SUPP -> NP | P | Adv | SUPP SUPP | SUPP SUPP SUPP
"""

def main():
    #If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    #Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    #Convert input into a list of words
    s = preprocess(s)

    #Attempt to parse the sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse the sentence.")
        return

    #Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.leaves()))

def preprocess(sentence):
    #Tokenize and preprocess the sentence
    tokens = nltk.word_tokenize(sentence)
    words = [word.lower() for word in tokens if word.isalpha()]
    return words

def np_chunk(tree):
    #Return a list of all noun phrase chunks in the sentence tree
    return [subtree for subtree in tree.subtrees(lambda t: t.label() == 'NP')]

if __name__ == "__main__":
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)
    main()
