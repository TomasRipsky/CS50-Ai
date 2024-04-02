from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave
    Or(AKnight, AKnave), # A is either a knight or a knave
    Implication(AKnave, Not(And(AKnight,AKnave))),  # If A is a Knave then it can't be both a knight and a Knave
    Implication(AKnight, And(AKnight,AKnave))  # If A is a knight then A it telling the truth
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(And(AKnight, BKnave), And(AKnave, BKnight)),  # A is either a knight or a knave and B is either a knight or a knave
    Implication(AKnave, Not(And(AKnave,BKnave))),  # If A is a Knave then they cant be both knaves
    Implication(AKnight, And(AKnave,BKnave))  # If A is a knight then A it telling the truth
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(And(AKnight, BKnave), And(AKnave, BKnight)), # A is either a knight or a knave and B is either a knight or a knave
    Implication(AKnave, Not(And(AKnave,BKnave))),  # If A is a Knave then they cant be both knaves
    Implication(AKnave, Not(And(AKnight,AKnight))),  # If A is a Knave then they cant be both Knights
    Implication(AKnight, And(AKnight,BKnight)),  # If A is a knight they can be both knights
    Implication(BKnave, Not(And(AKnight, BKnave))) # If B is a knave they cant be one knave and the other a knight
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Or(CKnight, CKnave),  # C is either a knight or a knave

    Implication(AKnight, Or(AKnight, AKnave)), # If A is a knight then it could be either
    Implication(AKnave, Not(Or(AKnight, AKnave))), # If A is a knave  then it must not be either

    Implication(BKnight, CKnave), # If B is a Knight then C is a knave
    Implication(BKnight, AKnave),  # If B is a Knight then A is a Knave

    Implication(BKnave, CKnight), # If B is a knave then C is a knight
    Implication(BKnave, AKnight), # If B is a knave then A is a Knight

    Implication(CKnight, AKnight), # If C is a Knight then A is a Knight
    Implication(CKnave, AKnave) # If C is a knave then A is a knave
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
