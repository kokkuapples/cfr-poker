import numpy as np
import random


class KuhnPoker:
    cards = ["J", "Q", "K"] # Cards: Jack, Queen, King
    actions = ["b", "c"] # bet (call), check (fold)
    card_values = {"J": 0, "Q": 1, "K": 2} # Obv K > Q > J

    def __init__(self, cards=None):
        self.start(cards) 

    def showdown(self):
        return 0 if self.card_values[self.dealt_cards[0]] > self.card_values[self.dealt_cards[1]] else 1 
    def get_infoset(self, plr_idx):
        """ The infoset are: "x", "xc", "xb", "xcb". Where "x" is one of the three possible cards. In total Kuhn poker has 12 infoset """
        infoset = self.dealt_cards[plr_idx] + self.history[2:]
        
        # Map each possible infoset string into an index to be used in arrays
        action_idx = ["", "c", "b", "cb"].index(infoset[1:])
        hand_idx = self.card_values[infoset[0]]
        infoset_index = 3 * action_idx + hand_idx

        return infoset_index, infoset

    def compute_utility(self, index):
        utility_value = self.stacks[index] + self.pot
        utility = [0, 0]
        utility[index] = utility_value
        utility[1 - index] = -utility_value

        self.terminate = True

        return utility

    def start(self, cards=None):
        if not cards:
            self.dealt_cards = random.sample(self.cards, 2)
        else:
            self.dealt_cards = list(cards)

        self.pot = 2
        self.stacks = [-1, -1]
        self.terminate = False
        self.history = "".join(self.dealt_cards)
        self.plr_idx = 0
        
    def play(self, action):
        if action == "b":
            self.history += "b"
            self.stacks[self.plr_idx] -= 1
            self.pot += 1
        else:
            self.history += "c"

        # The game ends after the series of actions: "bb", "cc", "bc", "cbb" "cbc"
        if self.history[-2:] == "bb" or self.history[2:] == "cc":
            utility = self.compute_utility(self.showdown())
        elif self.history[-2:] == "bc":
            utility = self.compute_utility(self.history.index("b") % 2)
        else:
            utility = [0, 0]
        
        self.plr_idx = (self.plr_idx + 1) % 2

        return self.terminate, self.history, np.array(utility)
