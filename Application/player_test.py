"""Unit testing."""

import unittest
import player


class TestPlayer(unittest.TestCase):
    """Test the class."""

    def test_init_default_object(self):
        """Instantiate an object and check its properties."""
        name = 'test'
        play = player.Player(name)
        self.assertIsInstance(play, player.Player)
        self.assertEqual(play.score, 0)
        self.assertEqual(play.name, name)

    def test_rename(self):
        """Test the rename method checks if passed name is name."""
        name = 'test'
        play = player.Player(name)
        rename = 'test2'
        res = play.rename(rename)
        exp = res == play.name
        self.assertTrue(exp)

    def test_get_name(self):
        """Test the get name method which returns name."""
        name = 'test'
        play = player.Player(name)
        res = play.get_name()
        exp = res == play.name

        self.assertTrue(exp)

    def test_get_score(self):
        """Test the get score method which returns score."""
        name = 'test'
        play = player.Player(name)

        res = play.get_score()
        exp = play.score

        self.assertEqual(res, exp)

    def test_add_to_score(self):
        """Test set score which returns modified score."""
        name = 'test'
        play = player.Player(name)
        round_score = 5

        res = play.add_to_score(round_score)
        exp = play.score
        self.assertEqual(res, exp)

    def test_empty_the_score(self):
        """Test this function if it changes the score to 0."""
        name = 'test'
        play = player.Player(name)
        play.score = 20
        play.empty_the_score()
        res = play.score == 0
        self.assertTrue(res)
