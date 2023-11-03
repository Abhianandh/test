import sys

def read_structure(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file]

def read_words(file_path):
    with open(file_path, 'r') as file:
        return [word.strip() for word in file]

def display_crossword(crossword):
    for row in crossword:
        print(''.join(row))

def is_valid_placement(crossword, word, row, col, direction):
    if direction == 'across':
        if col + len(word) > len(crossword[row]):
            return False
        for i in range(len(word)):
            if crossword[row][col + i] != ' ' and crossword[row][col + i] != word[i]:
                return False
        return True
    elif direction == 'down':
        if row + len(word) > len(crossword):
            return False
        for i in range(len(word)):
            if crossword[row + i][col] != ' ' and crossword[row + i][col] != word[i]:
                return False
        return True
    return False

def place_word(crossword, word, row, col, direction):
    if direction == 'across':
        for i in range(len(word)):
            crossword[row][col + i] = word[i]
    elif direction == 'down':
        for i in range(len(word)):
            crossword[row + i][col] = word[i]

def remove_word(crossword, word, row, col, direction):
    if direction == 'across':
        for i in range(len(word)):
            crossword[row][col + i] = ' '
    elif direction == 'down':
        for i in range(len(word)):
            crossword[row + i][col] = ' '

def solve_crossword(crossword, words, row, col):
    if row == len(crossword):
        return True

    next_row = row
    next_col = col + 1
    if next_col == len(crossword[row]):
        next_row = row + 1
        next_col = 0

    if crossword[row][col] == ' ':
        for word in words:
            for direction in ['across', 'down']:
                if is_valid_placement(crossword, word, row, col, direction):
                    place_word(crossword, word, row, col, direction)
                    if solve_crossword(crossword, words, next_row, next_col):
                        return True
                    remove_word(crossword, word, row, col, direction)

    else:
        return solve_crossword(crossword, words, next_row, next_col)

    return False

def generate_crossword(structure_file, words_file):
    crossword_structure = read_structure(structure_file)
    crossword_words = read_words(words_file)

    if solve_crossword(crossword_structure, crossword_words, 0, 0):
        display_crossword(crossword_structure)
    else:
        print("No solution found")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_crossword.py <structure_file> <words_file>")
        sys.exit(1)

    structure_file = sys.argv[1]
    words_file = sys.argv[2]

    generate_crossword(structure_file, words_file)
