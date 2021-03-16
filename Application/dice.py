"""Dice imports."""

import random


class Dice():
    """Class Dice."""

    def __init__(self):
        """Initialize its attributes."""
        self.min_value = 1
        self.max_value = 6

    def throw(self):
        """Generate new number between bounds of 1 to 6."""
        return random.randint(self.min_value, self.max_value)

    def cheat(self):
        """Change min value to two."""
        self.min_value = 2
        return self.min_value

    def uncheat(self):
        """Change min value to one."""
        self.min_value = 1
        return self.min_value
