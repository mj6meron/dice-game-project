"""Dice hand imports."""

import dice


class Dicehand():
    """Dice hand class."""

    def __init__(self):
        """Initialize class attributes."""
        self.current_score = 0
        self.dice_value = dice.Dice()

    def get_round_score(self):
        """Return the current score."""
        return self.current_score

    def throw(self, die_1, die_2):
        """Generate a number and returns a number."""
        die_1_throw = die_1.throw()
        die_2_throw = die_2.throw()
        if die_1_throw == 1 or die_2_throw == 1:
            self.current_score = 0
            return die_1_throw, die_2_throw
        if die_1_throw != 1 and die_2_throw != 1:
            self.current_score += die_1_throw + die_2_throw
        return die_1_throw, die_2_throw
