import nltk
import sys

# Download the required NLTK data files
#nltk.download('punkt')

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
S -> NP VP | S Conj S | NP VP Conj S
NP -> Det N | Det Adj N | N | NP PP | NP Conj NP | Det N PP | Det AdjP N | Det AdjP N PP
VP -> V | V NP | V NP PP | Adv V | V Adv | VP Conj VP | V PP | Adv V NP | V NP PP Adv | V PP Adv
PP -> P NP
AdjP -> Adj | Adj AdjP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # We use nltk to separate the sentence into individual words
    words = nltk.word_tokenize(sentence)
    # Create an empty list
    words_lower_case=[]
    # We go through each word turning them into lower case
    for word in words:
        word_lower = word.lower()
        # We check that the word contains at least one alphabetic character
        if any(char.isalpha() for char in word_lower):
            # If it does contain we added to the list
            words_lower_case.append(word_lower)
    # We return the list
    return words_lower_case

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    # Iterate over all subtrees in the tree with label 'NP'
    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        # Check if this subtree contains any nested 'NP'
        if not any(child.label() == 'NP' for child in subtree):
            np_chunks.append(subtree)

    return np_chunks



if __name__ == "__main__":
    main()
 # type: ignore