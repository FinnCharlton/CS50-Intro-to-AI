from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
ASay0 = And(AKnight,AKnave)
knowledge0 = And(
    Or(AKnight,AKnave),
    Implication(AKnight,ASay0),
    Implication(AKnave,Not(ASay0))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
ASay1 = And(AKnave,BKnave)
knowledge1 = And(
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Implication(AKnight,ASay1),
    Implication(AKnave,Not(ASay1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
ASay2 = And(Biconditional(AKnight,BKnight),Biconditional(AKnave,BKnave))
BSay2 = And(Biconditional(AKnight,Not(BKnight)),Biconditional(AKnave,Not(BKnave)))
knowledge2 = And(
    Or(AKnight,AKnave),
    Or(BKnight,BKnave), 
    Implication(AKnight,ASay2),
    Implication(AKnave,Not(ASay2)),
    Implication(BKnight,BSay2),
    Implication(BKnave,Not(BSay2))   
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
ASay3 = And(Implication(BKnight,AKnave),Implication(BKnave,AKnight))
BSay3 = CKnave
CSay3 = AKnight
knowledge3 = And(
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight,CKnave),
    Implication(AKnight,ASay3),
    Implication(AKnave,Not(ASay3)),
    Implication(BKnight,BSay3),
    Implication(BKnave,Not(BSay3)),
    Implication(CKnight,CSay3),
    Implication(CKnave,Not(CSay3)),

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
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
