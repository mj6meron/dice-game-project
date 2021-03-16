"""Computers interaction and strategy."""
# written by: Meron

import random


class Intelligence:
    """Intelligence class - Interaction and Logic."""

    level_of_difficulty = 1

    def change_level_of_difficulty(self, number):
        """Change the level of difficulty of the game."""
        self.level_of_difficulty = number

    @staticmethod
    def would_it_be_enough_to_win(current_round_score, computer_score):
        """Logic to keep the computer hold."""
        return current_round_score + computer_score >= 100

    def evaluate(self, die_1_value, die_2_value,
                 current_round_score, computer_score):
        """Evaluate Logic of the game."""
        decision = False
        if die_1_value == 1 or die_2_value == 1:
            return decision
        if self.level_of_difficulty == 1:
            return self.level_one()
        if self.level_of_difficulty == 2:
            return self.level_two(current_round_score, computer_score)
        return decision

    @staticmethod
    def level_one():
        """Level one of the game."""
        return random.choice([True, False])

    def level_two(self, current_round_score, computer_score):
        """Level two of the game."""
        if self.would_it_be_enough_to_win(current_round_score, computer_score):
            return False
        if current_round_score >= 15:
            return False
        return True
