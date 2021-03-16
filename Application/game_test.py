# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
# Written by Aki Sirkiä

"""Unit test for game.py."""

import unittest
from unittest.mock import patch
from io import StringIO
import game
from game import Game
from player import Player
from dice_hand import Dicehand
from intelligence import Intelligence
from histogram import Histogram


class TestGameClass(unittest.TestCase):
    """Tests for Game class."""

    def setUp(self):
        """Set up the variable."""
        self.the_game = game.Game()

    def test_init_object(self):
        """Initialize the game and check the properties."""
        instance = game.Game
        self.assertIsInstance(self.the_game, instance)

    def test_game_class_attributes(self):
        """Test the attributes from the game class."""
        self.assertIsNotNone(self.the_game.die_1)
        self.assertIsNotNone(self.the_game.die_2)
        self.assertIsNotNone(self.the_game.rules)
        self.assertIsNone(self.the_game.player_one)
        self.assertIsNone(self.the_game.player_two)
        self.assertIsNone(self.the_game.active_player)
        self.assertIsNone(self.the_game.computer)
        self.assertIsNone(self.the_game.dice_hand)

    def test_create_players(self):
        """Create a object of a player class."""
        names = ["player_one", "player_two"]
        with patch("builtins.input", side_effect=names):
            self.the_game.start()
            self.assertEqual(self.the_game.active_player,
                             self.the_game.player_one)
            self.assertEqual("player_one",
                             self.the_game.player_one.get_name())
            self.assertEqual("player_two",
                             self.the_game.player_two.get_name())

    def test_start_with_human_players(self):
        """Test start."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.assertIsInstance(self.the_game.player_one, Player)
        self.assertIsInstance(self.the_game.player_two, Player)
        self.assertEqual(self.the_game.active_player,
                         self.the_game.player_one)

    def test_start_with_computer_player(self):
        """Test start with PC as player."""
        players = ["test_name_player_one", "PC"]
        with patch("builtins.input", side_effect=players):
            self.the_game.start()
        self.assertIsNotNone(self.the_game.computer)

    def test_assign_active_player_initialize_dice_hand(self):
        """Test initializing the dice_hand."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.the_game.assign_active_player()
        self.assertIsNotNone(self.the_game.dice_hand)

    def test_is_active_player_none_or_player_two(self):
        """Test for check if active player is either none or player two."""
        players = ["test_name_player_one", "test_name_player_two"]
        with patch("builtins.input", side_effect=players):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_two
            self.assertTrue(
                self.the_game.is_active_player_none_or_player_two()
            )

            self.the_game.active_player = None
            self.assertTrue(
                self.the_game.is_active_player_none_or_player_two()
            )

    def test_is_active_player_one_and_not_pc(self):
        """Test methods return value."""
        players = ["test_name_player_one", "test_name_player_two"]
        with patch("builtins.input", side_effect=players):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_one
            self.assertTrue(self.the_game.is_active_player_one_and_not_pc())

            self.the_game.player_two.rename("PC")
            self.assertFalse(self.the_game.is_active_player_one_and_not_pc())

    def test_active_player_is_one_and_playing_against_pc(self):
        """Test for check if active player is one and playing against PC."""
        players = ["test_name_player_one", "PC"]
        with patch("builtins.input", side_effect=players):
            self.the_game.start()
            self.assertTrue(
                self.the_game.active_player_is_one_and_playing_against_pc())

    def test_assign_active_player_computers_turn(self):
        """Test computers playing."""
        players = ["test_name_player_one", "PC"]
        with patch("builtins.input", side_effect=players):
            self.the_game.start()
            self.the_game.assign_active_player()
            self.assertEqual(self.the_game.active_player,
                             self.the_game.player_one)

    def test_throw(self):
        """Test int return."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
            die_1, die_2 = self.the_game.throw()
        self.assertTrue(1 <= die_1 <= 6)
        self.assertTrue(1 <= die_2 <= 6)

    def test_cheat(self):
        """Test that die objects value has changed to 2."""
        self.the_game.cheat()
        self.assertEqual(self.the_game.die_1.min_value, 2)
        self.assertEqual(self.the_game.die_2.min_value, 2)

    def test_uncheat(self):
        """Test that die objects value has changed to 1."""
        self.the_game.cheat()
        self.the_game.uncheat()
        self.assertEqual(self.the_game.die_1.min_value, 1)
        self.assertEqual(self.the_game.die_2.min_value, 1)

    def test_display_rules(self):
        """Test return value from display_rules method."""
        self.assertEqual(self.the_game.display_rules(),
                         self.the_game.rules)

    def test_get_name(self):
        """Test return active players name."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.assertEqual(
            self.the_game.active_player.get_name(),
            self.the_game.active_player.name)

    def test_rename(self):
        """Test renaming active player."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        player_name_before_rename = self.the_game.active_player.get_name()
        self.the_game.rename("testing_rename_method")
        player_name_after_rename = self.the_game.active_player.get_name()
        self.assertNotEqual(player_name_before_rename,
                            player_name_after_rename)

    def test_show_scores_for_current_game(self):
        """Test score display."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.the_game.active_player.score = 50
        self.the_game.player_two.score = 1
        expected_output = \
            "test_name_for_player has 50 points, " \
            "test_name_for_player has 1 points."
        self.assertEqual(
            self.the_game.show_scores_of_the_current_game(),
            expected_output)

        self.the_game.active_player.score = 5
        self.the_game.player_two.score = 3
        expected = "test_name_for_player has 5 points," \
                   " test_name_for_player has 3 points."
        self.assertEqual(
            self.the_game.show_scores_of_the_current_game(),
            expected)

    def test_does_active_player_have_enough_points_to_win(self):
        """Test to see if game should be ended."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.the_game.active_player.score = 0
        self.assertFalse(
            self.the_game.does_active_player_have_enough_points_to_win())

        self.the_game.active_player.score = 99
        self.assertFalse(
            self.the_game.does_active_player_have_enough_points_to_win())

        self.the_game.active_player.score = 90
        self.the_game.dice_hand.current_score = 9
        self.assertFalse(
            self.the_game.does_active_player_have_enough_points_to_win())

        self.the_game.active_player.score = 90
        self.the_game.dice_hand.current_score = 11
        self.assertTrue(
            self.the_game.does_active_player_have_enough_points_to_win())

        self.the_game.active_player.score = 100
        self.the_game.dice_hand.current_score = 0
        self.assertTrue(
            self.the_game.does_active_player_have_enough_points_to_win())

    def test_end_active_players_turn(self):
        """Save current players score and switch to the another player."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.the_game.active_player.score = 14
        self.the_game.dice_hand.current_score = 1
        self.the_game.end_active_players_turn()
        self.assertEqual(self.the_game.player_one.get_score(), 15)
        self.assertEqual(
            self.the_game.active_player,
            self.the_game.player_two)

        self.the_game.active_player.score = 45
        self.the_game.dice_hand.current_score = 16
        self.the_game.end_active_players_turn()
        self.assertEqual(self.the_game.player_two.get_score(), 61)
        self.assertEqual(
            self.the_game.active_player,
            self.the_game.player_one)

    @patch.object(Histogram, 'display')
    def test_histogram_call(self, mock):
        """Test histogram call."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_game.start()
        self.the_game.display_data()
        self.assertTrue(mock.called)

    # ------Computer player tests------

    def test_computer_throw_with_one_dice_having_value_of_one(self):
        """Test method output when one of the dice has value of one."""
        expected_output = "One of the computers dice had a value of 1, " \
                          "so its turn has ended!\n"
        with patch("builtins.input", return_value="PC"):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_two
            with patch('sys.stdout', new=StringIO()) as fake_out:
                values = [1, 2]
                with patch.object(
                        Dicehand, "throw", create=True, return_value=values):
                    self.the_game.computer_throw()
                    self.assertEqual(expected_output, fake_out.getvalue())

    def test_computer_throw_with_both_dice_having_value_of_one(self):
        """Test method output when both of the dice has value of one."""
        expected_output = \
            "Both dice had value of one! Computers total score is now 0" \
            " and its turn has ended\n"
        with patch("builtins.input", return_value="PC"):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_two
            self.the_game.active_player.add_to_score(50)
            self.assertTrue(
                self.the_game.active_player,
                self.the_game.player_two)

            with patch('sys.stdout', new=StringIO()) as fake_out:
                values = [1, 1]
                with patch.object(
                        Dicehand, "throw", create=True, return_value=values):
                    self.the_game.computer_throw()
                    self.assertEqual(expected_output, fake_out.getvalue())
                    self.assertEqual(self.the_game.player_two.get_score(), 0)
                    self.assertTrue(
                        self.the_game.active_player,
                        self.the_game.player_one)

    def test_computer_throw_with_die_value_two(self):
        """Test method output when both dice have value over one."""
        expected_output = "Computers dice had values of 2 and 2, " \
                          "it's total for the round is 4\n"
        with patch("builtins.input", return_value="PC"):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_two
            self.the_game.active_player.add_to_score(50)
            self.assertTrue(
                self.the_game.active_player,
                self.the_game.player_two)

            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.the_game.dice_hand.current_score = 4
                values = [2, 2]
                with patch.object(
                        Dicehand, "throw", create=True, return_value=values):
                    self.the_game.computer_throw()
                    self.assertEqual(expected_output, fake_out.getvalue())

    def test_computer_playing_switching_back_to_player_one(self):
        """Test computers interaction with application."""
        with patch("builtins.input", return_value="PC"):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_two
            with patch.object(
                    Intelligence, "evaluate", create=True, return_value=False
            ):
                self.the_game.computer_playing()
                self.assertEqual(
                    self.the_game.active_player,
                    self.the_game.player_one)

    def test_computer_winning_the_game(self):
        """Test computer winning the game."""
        expected_output = "Computer won! Game is restarting\n"
        with patch("builtins.input", return_value="PC"):
            self.the_game.start()
            self.the_game.active_player = self.the_game.player_two
            with patch.object(
                    Intelligence, "evaluate",
                    create=True, return_value=False):
                with patch.object(
                        Game, "does_active_player_have_enough_points_to_win",
                        create=True, return_value=True):
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        self.the_game.computer_playing()
                        self.assertTrue(
                            expected_output in fake_out.getvalue())

    def test_adjust_difficult(self):
        """Test adjust difficulty with 1 and 2."""
        with patch("builtins.input", return_value="PC"):
            self.the_game.start()
        self.the_game.adjust_difficulty(2)
        self.assertEqual(self.the_game.computer.level_of_difficulty, 2)
        self.the_game.adjust_difficulty(1)
        self.assertEqual(self.the_game.computer.level_of_difficulty, 1)
