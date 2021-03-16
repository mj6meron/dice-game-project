# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
# Written by Aki Sirkiä

"""Unit testing for shell.py."""

import unittest
from unittest.mock import patch
from io import StringIO
import shell
import game
from game import Game


class ShellTestClass(unittest.TestCase):
    """Tests for Shell class."""

    def setUp(self):
        """Create variables for the tests."""
        self.the_shell = shell.Shell()

    def test_init_default_object(self):
        """Initialize a game and shell objects."""
        instance = shell.Shell
        the_game = game.Game
        self.assertIsInstance(self.the_shell, instance)
        self.assertIsInstance(self.the_shell.game, the_game)

    def test_attributes(self):
        """Test Intro and prompt."""
        self.assertIsNotNone(self.the_shell.intro)
        self.assertIsNotNone(self.the_shell.prompt)

    def test_change_prompt_to_currently_active_player(self):
        """Test that prompt changes."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            self.assertEqual(
                "\ntest_name_for_player: ", self.the_shell.prompt)

    def test_one_of_the_die_landed_one_up(self):
        """Test shell's throw."""
        expected_output = "One of your dice landed on one, " \
                          "so your turn has ended!\n"
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            with patch('sys.stdout', new=StringIO()) as fake_out:
                dice_values = [1, 2]
                with patch.object(
                        Game, "throw", create=True, return_value=dice_values):
                    self.the_shell.do_throw("")
                    self.assertEqual(expected_output, fake_out.getvalue())

    def test_neither_of_the_dice_landed_one_up(self):
        """Test shell's throw."""
        expected_output = "Your dice landed 3 and 4 up, " \
                          "your points for this round 0. " \
                          "Do you wanna throw again or hold?\n"
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            with patch('sys.stdout', new=StringIO()) as fake_out:
                dice_values = [3, 4]
                with patch.object(
                        Game, "throw", create=True, return_value=dice_values):
                    self.the_shell.do_throw("")
                    self.assertEqual(expected_output, fake_out.getvalue())

    def test_both_dice_landed_one_up(self):
        """Test when both dice lands one up."""
        expected_output = "Both your dices landed one up!!" \
                          " This means you lost all of your" \
                          " saved points and your turn has ended!\n"
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            self.the_shell.game.active_player.add_to_score(50)
            with patch('sys.stdout', new=StringIO()) as fake_out:
                dice_values = [1, 1]
                with patch.object(
                        Game, "throw", create=True, return_value=dice_values):
                    self.the_shell.do_throw("")
                    self.assertEqual(expected_output, fake_out.getvalue())
                    self.assertEqual(
                        0,
                        self.the_shell.game.player_one.get_score())
                    self.assertNotEqual(self.the_shell.game.active_player,
                                        self.the_shell.game.player_one)

    # ------------DO_SOMETHING---------------

    def test_do_hold_with_enough_points_to_win(self):
        """Test saving the round score to the total and winning the game."""
        expected_output = "You won the game! Game will restart now\n"
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            self.the_shell.game.active_player.add_to_score(99)
            self.the_shell.game.dice_hand.current_score = 2
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.the_shell.do_hold("")
                self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_hold_without_enough_points_to_win(self):
        """Test saving the round score to the total and ending the turn."""
        expected_output = "You hold the score, " \
                          "now it's another players turn!\n"
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.the_shell.do_hold("")
                self.assertEqual(expected_output, fake_out.getvalue())
                self.assertNotEqual(self.the_shell.game.active_player,
                                    self.the_shell.game.player_one)

    def test_do_rules(self):
        """Test displaying of the rules to the user."""
        expected_outcome = "{}\n".format(self.the_shell.game.rules)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.the_shell.do_rules("")
            self.assertEqual(expected_outcome, fake_out.getvalue())

    def test_do_start(self):
        """Test start."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
        self.assertIsNotNone(self.the_shell.game.player_one.get_name())
        self.assertIsNotNone(self.the_shell.game.player_two.get_name())

    def test_do_restart(self):
        """Test restart."""
        with patch("builtins.input",
                   return_value="test_name_before_restart"):
            self.the_shell.do_start("")
            with patch(
                    "builtins.input",
                    return_value="name_test_for_after_restarting"):
                self.the_shell.do_restart("")
                self.assertEqual("name_test_for_after_restarting",
                                 self.the_shell.game.active_player.get_name())

    def test_do_cheat(self):
        """Test cheating, makes die min value to 2."""
        self.the_shell.do_cheat("")
        self.assertEqual(self.the_shell.game.die_1.min_value, 2)
        self.assertEqual(self.the_shell.game.die_2.min_value, 2)

    def test_do_uncheat(self):
        """Test uncheating, makes die min value to 1."""
        self.the_shell.do_cheat("")
        self.the_shell.do_uncheat("")
        self.assertEqual(self.the_shell.game.die_1.min_value, 1)
        self.assertEqual(self.the_shell.game.die_1.min_value, 1)

    def test_do_show_scores(self):
        """Test displaying the scores of the current round."""
        expected_output =\
            "test_name_for_player has 10 points, " \
            "test_name_for_player has 20 points.\n"
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            self.the_shell.game.player_one.add_to_score(10)
            self.the_shell.game.player_two.add_to_score(20)
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.the_shell.do_scores("")
                self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_exit(self):
        """Test ending the application."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            with self.assertRaises(SystemExit):
                self.the_shell.do_exit("")

    def test_do_difficulty_to_one(self):
        """Test for adjusting the difficulty to level 1."""
        with patch("builtins.input", return_value="PC"):
            self.the_shell.do_start("")
            self.the_shell.game.computer.change_level_of_difficulty(2)
            self.the_shell.do_computer_to_random("")
            self.assertEqual(
                1,
                self.the_shell.game.computer.level_of_difficulty)

    def test_do_difficulty_to_two(self):
        """Test for adjusting the difficulty to level 2."""
        with patch("builtins.input", return_value="PC"):
            self.the_shell.do_start("")
            self.the_shell.do_computer_to_plan("")
            self.assertEqual(
                2,
                self.the_shell.game.computer.level_of_difficulty)

    def test_do_rename(self):
        """Test the renaming of active player."""
        with patch("builtins.input", return_value="test_name_for_player"):
            self.the_shell.do_start("")
            with patch("builtins.input", return_value="second_test_name"):
                self.the_shell.do_rename("")
                self.assertEqual(
                    "second_test_name",
                    self.the_shell.game.active_player.get_name())

    @patch.object(Game, 'display_data')
    def test_do_histogram(self, mock):
        """Test game.display_data call."""
        self.the_shell.do_histogram("")
        self.assertTrue(mock.called)

    # ------------Exceptions---------------

    def test_do_show_scores_exception(self):
        """Test for raising error."""
        expected_output = "You need to start the game " \
                          "before trying to see the scores\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game, "show_scores_of_the_current_game",
                              create=True, side_effect=AttributeError):
                self.the_shell.do_scores("")
                self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_throw_exception(self):
        """Test for raising error."""
        expected_output = "You need to start the game before throwing!\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game, "throw",
                              create=True, side_effect=AttributeError):
                self.the_shell.do_throw("")
                self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_hold_exception(self):
        """Test for raising error."""
        expected_output = "You need to start the game before holding!\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game,
                              "does_active_player_have_enough_points_to_win",
                              create=True, side_effect=AttributeError):
                self.the_shell.do_hold("")
                self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_difficulty_changes_exception(self):
        """Test for raising error."""
        expected_output = "You need to start the game " \
                          "before trying to adjust the difficulty\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game, "adjust_difficulty",
                              create=True, side_effect=AttributeError):
                self.the_shell.do_computer_to_random("")
                self.assertEqual(expected_output, fake_out.getvalue())

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game, "adjust_difficulty",
                              create=True, side_effect=AttributeError):
                self.the_shell.do_computer_to_plan("")
                self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_rename_exception(self):
        """Test for raising error."""
        expected_output = "You need to start " \
                          "the game before trying renaming\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game, "rename",
                              create=True, side_effect=AttributeError):
                with patch("builtins.input", return_value="second_test_name"):
                    self.the_shell.do_rename("")
                    self.assertEqual(expected_output, fake_out.getvalue())

    def test_do_histogram_exception(self):
        """Test for raising error."""
        expected_output = "File not found, or empty\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Game, "display_data",
                              create=True, side_effect=FileNotFoundError):
                self.the_shell.do_histogram("")
                self.assertEqual(expected_output, fake_out.getvalue())
