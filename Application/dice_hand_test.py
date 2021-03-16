"""Unit testing."""

import unittest
from unittest.mock import patch
import dice_hand
from dice_hand import Dicehand
from dice import Dice


class TestingDiceHand(unittest.TestCase):
    """Tests dice hand class."""

    def test_init(self):
        """Tests initializer and its properties."""
        hand = Dicehand()
        self.assertIsInstance(hand, Dicehand)
        self.assertEqual(hand.current_score, 0)

    def setUp(self):
        """Set up for variable."""
        self.the_dice_hand = dice_hand.Dicehand()

    def test_throw_with_two_dices_having_more_than_value_of_one(self):
        """Testing purpose."""
        self.the_dice_hand.current_score = 0
        dice_values = [6, 6]
        with patch.object(Dice, "throw", create=True,
                          side_effect=dice_values):
            self.the_dice_hand.throw(Dice, Dice)
            self.assertEqual(12, self.the_dice_hand.get_round_score())

    def test_throw_with_one_dice_having_value_of_one(self):
        """Testing purpose."""
        self.the_dice_hand.current_score = 20
        dice_values = [6, 1]
        with patch.object(Dice, "throw", create=True,
                          side_effect=dice_values):
            self.the_dice_hand.throw(Dice, Dice)
            self.assertEqual(0, self.the_dice_hand.get_round_score())

    def test_get_score(self):
        """Tests get score method which returns score."""
        hand = dice_hand.Dicehand()
        res = hand.get_round_score()
        exp = res == hand.current_score
        self.assertTrue(exp)
