"""Unit testing."""

import unittest
import dice


class TestDice(unittest.TestCase):
    """Test the class."""

    def test_init(self):
        """Instantiate an object."""
        die = dice.Dice()
        self.assertIsInstance(die, dice.Dice)
        self.assertEqual(die.min_value, 1)
        self.assertEqual(die.max_value, 6)

    def test_throw(self):
        """Test the throw method checking its inbound values."""
        die = dice.Dice()

        res = die.throw()
        exp = die.min_value <= res <= die.max_value

        self.assertTrue(exp)

    def test_cheat(self):
        """Test the cheat method and if minimum values is changed to 2."""
        die = dice.Dice()

        res = die.cheat()
        exp = res == die.min_value
        self.assertTrue(exp)

    def test_uncheat(self):
        """Test the uncheat method checks if minimum value is back to 1."""
        die = dice.Dice()

        res = die.uncheat()
        exp = res == die.min_value
        self.assertTrue(exp)
