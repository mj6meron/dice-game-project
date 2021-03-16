# -*- coding: utf-8 -*-
# Written by Aki Sirkiä
"""Shell operations for the two dice pig game."""

import cmd
import sys
import game


class Shell(cmd.Cmd):
    """Shell class."""

    intro = "Welcome to Two Dice Pig Game!"
    prompt = "Game: "

    def __init__(self):
        """Init the object."""
        super().__init__()
        self.game = game.Game()

    def change_prompt_to_currently_active_player(self):
        """Change prompt to active player."""
        self.prompt = "\n{}: ".format(self.game.active_player.get_name())

    def end_turn(self):
        """End Turn method calls."""
        self.game.end_active_players_turn()
        self.change_prompt_to_currently_active_player()

    def one_dice_had_value_of_one(self):
        """Actions for when player throws one."""
        print("One of your dice landed on one, so your turn has ended!")
        self.end_turn()

    def both_dice_had_value_of_one(self):
        """Actions for when both dice are 1."""
        print(
            "Both your dices landed one up!! "
            "This means you lost all of your "
            "saved points and your turn has ended!")
        self.game.active_player.empty_the_score()
        self.end_turn()

    def neither_dice_had_value_of_one(self, die_1, die_2):
        """Message for when neither of the dice landed one up."""
        print("Your dice landed {} and {} up, your points for this round {}. "
              "Do you wanna throw again or hold?".
              format(die_1, die_2, self.game.dice_hand.get_round_score()))

    def do_start(self, _):
        """Start the game."""
        self.game.start()
        self.change_prompt_to_currently_active_player()

    def do_restart(self, _):
        """Restarts the game."""
        self.__init__()
        self.game.start()
        self.change_prompt_to_currently_active_player()

    def do_rules(self, _):
        """Display Rules of the game."""
        print(self.game.display_rules())

    def do_throw(self, _):
        """Throw the dice."""
        try:
            die_1_value, die_2_value = self.game.throw()
            if die_1_value == 1 and die_2_value == 1:
                self.both_dice_had_value_of_one()
                return
            if die_1_value == 1 or die_2_value == 1:
                self.one_dice_had_value_of_one()
            else:
                self.neither_dice_had_value_of_one(
                    die_1_value, die_2_value
                )
        except AttributeError:
            print("You need to start the game before throwing!")

    def do_hold(self, _):
        """End turn and save the current score to the total score."""
        try:
            if self.game.does_active_player_have_enough_points_to_win():
                print("You won the game! Game will restart now")
                self.game.data_saving_at_the_end_of_the_game()
                self.do_restart("")
                return
            print("You hold the score, now it's another players turn!")
            self.end_turn()
        except AttributeError:
            print("You need to start the game before holding!")

    def do_cheat(self, _):
        """Minimum value of the dice becomes 2."""
        self.game.cheat()

    def do_uncheat(self, _):
        """Minimum value of the dice becomes 1."""
        self.game.uncheat()

    def do_scores(self, _):
        """Display scores of the current game."""
        try:
            print(self.game.show_scores_of_the_current_game())
        except AttributeError:
            print("You need to start the game before"
                  " trying to see the scores")

    def do_exit(self, _):
        # pylint: disable=no-self-use
        """Leave the game."""
        print("Hope you liked the game!")
        sys.exit(0)

    def do_computer_to_random(self, _):
        """Change computer decisions to random."""
        try:
            self.game.adjust_difficulty(1)
        except AttributeError:
            print("You need to start the game before "
                  "trying to adjust the difficulty")

    def do_computer_to_plan(self, _):
        """Change computer to play with strategy."""
        try:
            self.game.adjust_difficulty(2)
        except AttributeError:
            print("You need to start the game before"
                  " trying to adjust the difficulty")

    def do_rename(self, _):
        """Rename current user."""
        try:
            self.game.rename(input("Enter name: "))
            self.change_prompt_to_currently_active_player()
        except AttributeError:
            print("You need to start the game before trying renaming")

    def do_histogram(self, _):
        """Display data about played games."""
        try:
            self.game.display_data()
        except FileNotFoundError:
            print("File not found, or empty")
