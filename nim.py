import numpy as np
import random
import time

class Nim:

    def __init__(self, initial=np.array([1, 3, 5, 7])):
        self.piles = initial
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        return {(i, j) for i, pile in enumerate(piles) for j in range(1, pile + 1)}

    @classmethod
    def other_player(cls, player):
        return 1 - player

    def switch_player(self):
        self.player = Nim.other_player(self.player)

    def move(self, action):
        pile, count = action
        if self.winner is not None:
            raise Exception("Game already won")
        if not (0 <= pile < len(self.piles) and 1 <= count <= self.piles[pile]):
            raise Exception("Invalid move")
        self.piles[pile] -= count
        self.switch_player()
        if np.all(self.piles == 0):
            self.winner = self.player

class NimAI:

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.alpha = alpha
        self.epsilon = epsilon
        self.q = np.zeros((8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 12), dtype=float)

    def update(self, old_state, action, new_state, reward):
        q_old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        q_new = q_old + self.alpha * (reward + best_future - q_old)
        self.q[old_state][action] = q_new

    def get_q_value(self, state, action):
        return self.q[state][action]

    def best_future_reward(self, state):
        available_actions = Nim.available_actions(state)
        if not available_actions:
            return 0
        q_values = [self.get_q_value(state, action) for action in available_actions]
        return max(q_values)

    def choose_action(self, state, epsilon=True):
        if epsilon and random.random() < self.epsilon:
            return random.choice(list(Nim.available_actions(state)))
        best_actions = []
        best_value = -float('inf')
        for action in Nim.available_actions(state):
            value = self.get_q_value(state, action)
            if value > best_value:
                best_actions = [action]
                best_value = value
            elif value == best_value:
                best_actions.append(action)
        return random.choice(best_actions)

def train(n):
    player = NimAI()
    for i in range(n):
        game = Nim()
        last = {0: {"state": None, "action": None}, 1: {"state": None, "action": None}}
        while True:
            state = game.piles.copy()
            action = player.choose_action(state)
            last[game.player]["state"] = state
            last[game.player]["action"] = action
            game.move(action)
            new_state = game.piles.copy()
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(last[game.player]["state"], last[game.player]["action"], new_state, 1)
                break
            elif last[game.player]["state"] is not None:
                player.update(last[game.player]["state"], last[game.player]["action"], new_state, 0)

def play(ai, human_player=None):
    if human_player is None:
        human_player = random.randint(0, 1)
    game = Nim()
    while True:
        print("\nCurrent Piles:")
        print(game.piles)
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")
        game.move((pile, count))
        if game.winner is not None:
            print("\nGame Over")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            break

# Train the AI
train(10000)

# Play the game
play(NimAI(alpha=0.5, epsilon=0.1))
