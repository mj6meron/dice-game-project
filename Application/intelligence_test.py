# written by: Meron
"""Test of the Intelligence class module."""
import unittest
from unittest.mock import patch
from intelligence import Intelligence


class TestIntelligence(unittest.TestCase):
    """Test the class Intelligence."""

    def setUp(self):
        """Set up variables for test purposes."""
        self.instance = Intelligence()
        self.boolean_check = None

    def test_class_attributes(self):
        """Test the default 'level of different'."""
        self.assertEqual(Intelligence.level_of_difficulty, 1)

    def test_change_level_difficulty(self):
        """Test adjusting difficulty."""
        self.instance = Intelligence()
        self.instance.change_level_of_difficulty(2)
        self.assertEqual(self.instance.level_of_difficulty, 2)

    def test_would_it_be_enough_to_win(self):
        """Create variables for the tests."""
        self.instance = Intelligence()
        boolean_check = self.instance.would_it_be_enough_to_win(33, 45)
        self.assertEqual(boolean_check, False)
        boolean_check = self.instance.would_it_be_enough_to_win(10, 90)
        self.assertEqual(boolean_check, True)

    def test_evaluate(self):
        """Test the Evaluate method."""
        # testing die_1_value == 1 or die_2_value
        self.boolean_check = self.instance.evaluate(1, 2, 20, 35)
        self.assertEqual(self.boolean_check, False)
        self.boolean_check = self.instance.evaluate(2, 1, 20, 35)
        self.assertEqual(self.boolean_check, False)
        self.boolean_check = self.instance.evaluate(1, 1, 20, 35)
        self.assertEqual(self.boolean_check, False)
        # testing executing of either level_one or level_methods
        # returning true form level_one
        with patch.object(Intelligence,
                          "level_one", create=True, return_value=True):
            self.boolean_check = self.instance.evaluate(2, 2, 20, 35)
            self.assertEqual(self.boolean_check, True)
        with patch.object(Intelligence,
                          "level_one", create=True, return_value=False):
            self.boolean_check = self.instance.evaluate(2, 2, 20, 35)
            self.assertEqual(self.boolean_check, False)
        # returning False from level_two
        self.instance.level_of_difficulty = 2
        self.boolean_check = self.instance.evaluate(2, 2, 20, 90)
        self.assertEqual(self.boolean_check, False)
        # returning True from level_two
        self.boolean_check = self.instance.evaluate(2, 2, 10, 80)
        self.assertEqual(self.boolean_check, True)
        # returning false by default
        self.instance.change_level_of_difficulty(0)
        self.boolean_check = self.instance.evaluate(2, 2, 10, 80)
        self.assertEqual(self.boolean_check, False)

    def test_level_one(self):
        """Test level_one returns random boolean."""
        self.boolean_check = Intelligence.level_one()
        assert (self.boolean_check is True) or (self.boolean_check is False)

    def test_level_two(self):
        """Test level_two returns the correct boolean."""
        self.boolean_check = self.instance.level_two(15, 90)
        self.assertEqual(self.boolean_check, False)
        self.boolean_check = self.instance.level_two(16, 10)
        self.assertEqual(self.boolean_check, False)
        self.boolean_check = self.instance.level_two(14, 10)
        self.assertEqual(self.boolean_check, True)
