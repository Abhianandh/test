from logic import *

#Define propositional symbols
A,B,C = symbols('A B C')

#Create the knowledge bases for each puzzle

#Puzzle0
knowledge0 = And(
    Not(And(A,B)),  #A cannot be both knight and knave
    Or(Not(A),Not(B))  #A is either a knight or a knave
)

#Puzzle1
knowledge1 = And(
    Implication(And(A,B), And(Not(A), Not(B))),  #A and B are both knaves
    Or(Not(A), Not(B))  #A and B are either knights or knaves
)

#Puzzle2
knowledge2 = And(
    Implication(And(A,B), Or(And(A,B), And(Not(A), Not(B)))),  #A and B are of the same kind
    Implication(And(A,B), Not(And(A, Not(B))), Not(And(Not(A), B))),  #A and B are not of different kinds
    Or(Not(A), Not(B))  #A and B are either knights or knaves
)

#Puzzle3
knowledge3 = And(
    Or(
        And(A, Or(AKnight, AKnave)),  #A is a knight and tells the truth
        And(Not(A), Not(Or(AKnight, AKnave)))  #A is a knave and lies
    ),
    Implication(And(B, CKnave), AKnave),  #B said "I am a knave"
    Implication(And(B, Not(CKnave)), AKnight),  #B said "I am a knight"
    Implication(And(B, CKnave), CKnave),  #B said "C is a knave"
    Implication(And(B, Not(CKnave)), CKnight),  #B said "C is a knight"
    Implication(And(C, AKnight), AKnight),  #C said "A is a knight"
    Implication(And(C, Not(AKnight)), AKnave),  #C said "A is a knave"
)

#Solve the puzzles
def solve_puzzle(knowledge):
    while True:
        updated = False
        for sentence in knowledge:
            if isinstance(sentence, Implication) and model_check(knowledge, sentence.antecedent):
                knowledge.add(sentence.consequent)
                updated = True
        if not updated:
            break

    return knowledge

#Run the solver on each puzzle
knowledge0 = solve_puzzle(knowledge0)
knowledge1 = solve_puzzle(knowledge1)
knowledge2 = solve_puzzle(knowledge2)
knowledge3 = solve_puzzle(knowledge3)

#Print the results
print("Puzzle 0: ", model_check(knowledge0, AKnight))
print("Puzzle 1: ", model_check(knowledge1, AKnight), model_check(knowledge1, BKnight))
print("Puzzle 2: ", model_check(knowledge2, AKnight), model_check(knowledge2, BKnight))
print("Puzzle 3: ", model_check(knowledge3, AKnight), model_check(knowledge3, BKnight), model_check(knowledge3, CKnight))
