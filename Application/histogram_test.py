# written by: Meron
"""Test of the Histogram.py file module."""
import unittest
from unittest.mock import patch
from io import StringIO
from histogram import Histogram
from player import Player


class TestHistogram(unittest.TestCase):
    """Test the class."""

    def setUp(self):
        """Set up variables for test purposes."""
        self.p_1 = Player("John")
        self.p_1.score = 50
        self.p_2 = Player("Mike")
        self.p_2.score = 40
        self.file = "HighScore.txt"
        self.histo = Histogram(self.p_1, self.p_2)

    def test_class_attributes(self):
        """Testing the class attributes."""
        self.assertIsNotNone(self.histo.winner)
        self.assertIsNotNone(self.histo.loser)
        self.assertIsNotNone(self.histo.score_difference)
        self.assertEqual(self.histo.file, "HighScore.txt")

    def test_init_object(self):
        """Testing the instantiation."""
        instance = Histogram
        self.assertIsInstance(self.histo, instance)

    def test_assigner(self):
        """Test if we assign the attributes right."""
        self.assertEqual(self.histo.winner, self.p_1)
        self.assertEqual(self.histo.loser, self.p_2)
        self.p_2.score = 60
        self.histo = Histogram(self.p_1, self.p_2)
        self.assertEqual(self.histo.winner, self.p_2)
        self.assertEqual(self.histo.loser, self.p_1)
        self.assertEqual(self.histo.score_difference, 10)
        self.assertEqual(self.histo.file, "HighScore.txt")

    def test_save(self):
        """Test if we save to the file right."""
        with patch('builtins.open', unittest.mock.mock_open()) as file:
            self.histo.save(file)
            file.assert_called_once_with(file, "a")

    def test_load(self):
        """Test if we load from a file right."""
        with patch("builtins.open", unittest.mock.mock_open(
                read_data="John, Mike, 10")):
            expected = [["John", " Mike", " 10"]]
            loaded = self.histo.load()
            self.assertEqual(loaded, expected)

    def test_display(self):
        """Test if we display the right way."""
        list_input = [["John", "Mike", "10"]]
        expected = "Winner: John, against: Mike, Difference: 10\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Histogram, "load",
                              create=True,
                              return_value=list_input):
                self.histo.display()
                self.assertEqual(fake_out.getvalue(), expected)
