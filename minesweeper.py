import itertools

class MinesweeperAI:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        new_cells = set()
        i, j = cell

        for x, y in itertools.product([-1, 0, 1], repeat=2):
            if 0 <= i + x < self.height and 0 <= j + y < self.width:
                neighbor = (i + x, j + y)
                if neighbor not in self.safes:
                    new_cells.add(neighbor)

        new_sentence = Sentence(new_cells, count)
        self.knowledge.append(new_sentence)

        for sentence in self.knowledge:
            if new_sentence != sentence:
                if new_sentence.cells.issubset(sentence.cells):
                    new_inference = Sentence(sentence.cells - new_sentence.cells, sentence.count - new_sentence.count)
                    if new_inference not in self.knowledge:
                        self.knowledge.append(new_inference)

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    return cell
        return None

class Sentence:
    def __init__(self, cells, count):
        self.cells = cells
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        return hash((tuple(self.cells), self.count))

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)

#Example usage
ai = MinesweeperAI(height=4, width=4)
ai.add_knowledge((0, 0), 0)
ai.add_knowledge((0, 1), 2)
ai.add_knowledge((0, 2), 0)
