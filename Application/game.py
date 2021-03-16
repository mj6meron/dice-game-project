# -*- coding: utf-8 -*-
# Written by Aki Sirkiä

"""Working flow and logic for the two dice pig game."""

import dice
import player
import dice_hand
import intelligence
import histogram


class Game():
    """Game class that holds logic of the game."""

    player_one = None
    player_two = None
    active_player = None

    rules = "\nRules of the game\n" \
            "-----------------\n" \
            "-If the player rolls a 1, they score " \
            "nothing and it becomes the next player's turn.\n" \
            "-If the player rolls any other number, " \
            "it is added to their turn total and the " \
            "player's turn continues.\n" \
            "-If a player chooses to \"hold\", " \
            "their turn total is added to their score, " \
            "and it becomes the next player's turn.\n" \
            "-If two 1s are rolled, the player’s entire score is lost, " \
            "and the turn ends.\n"

    computer = None

    dice_hand = None
    die_1 = dice.Dice()
    die_2 = dice.Dice()

    def start(self):
        """Start the game."""
        self.player_one = self.create_player(input("Enter name: "))
        self.player_two = self.create_player(input("Enter name: "))
        if self.player_two.get_name() == "PC":
            self.computer = intelligence.Intelligence()
        self.assign_active_player()

    @staticmethod
    def create_player(name):
        """Create and return a player object."""
        return player.Player(name)

    def assign_active_player(self):
        """Assign player objects to active player.

        Initialize the dice_hand, and assign player_one or player_two
        to be active_player
        Activates computers play.
        """
        self.dice_hand = dice_hand.Dicehand()
        if self.is_active_player_none_or_player_two():
            self.active_player = self.player_one
            return
        if self.is_active_player_one_and_not_pc():
            self.active_player = self.player_two

        if self.active_player_is_one_and_playing_against_pc():
            self.active_player = self.player_two
            self.computer_playing()

    def is_active_player_none_or_player_two(self):
        """Check to see if active player is none or player two."""
        return \
            self.active_player is None \
            or self.active_player is self.player_two

    def is_active_player_one_and_not_pc(self):
        """Check if active player is one and player two is not named "PC"."""
        return \
            self.active_player is self.player_one \
            and self.player_two.get_name() != "PC"

    def active_player_is_one_and_playing_against_pc(self):
        """Check if second player is named pc."""
        return \
            self.active_player is self.player_one \
            and self.player_two.get_name() == "PC"

    def throw(self):
        """Return int from dice_hand object, pass in the dice object."""
        return self.dice_hand.throw(self.die_1, self.die_2)

    def cheat(self):
        """Minimum value of the dice becomes 2."""
        self.die_1.cheat()
        self.die_2.cheat()

    def uncheat(self):
        """Minimum value of the dice becomes 1."""
        self.die_1.uncheat()
        self.die_2.uncheat()

    def display_rules(self):
        """Return rules."""
        return self.rules

    def rename(self, name):
        """Rename active player."""
        self.active_player.rename(name)

    def show_scores_of_the_current_game(self):
        """Return names and scores."""
        return "{} has {} points, {} has {} points.".\
            format(self.player_one.get_name(), self.player_one.get_score(),
                   self.player_two.get_name(), self.player_two.get_score())

    def does_active_player_have_enough_points_to_win(self):
        """Check if active player has enough score points."""
        return \
            self.active_player.get_score() + \
            self.dice_hand.get_round_score() >= 100

    def end_active_players_turn(self):
        """Save round score to total score, call assign active player()."""
        self.active_player.add_to_score(self.dice_hand.get_round_score())
        self.assign_active_player()

    def computer_throw(self):
        """Throw, and decision what to do with values."""
        die1_value, die2_value = \
            self.dice_hand.throw(self.die_1, self.die_2)

        if die1_value and die2_value == 1:
            print("Both dice had value of one! Computers total score is now 0"
                  " and its turn has ended")
            self.active_player.empty_the_score()
            return die1_value, die2_value

        if die1_value == 1 or die2_value == 1:
            print(
                "One of the computers dice had a value of 1,"
                " so its turn has ended!")
            return die1_value, die2_value

        print("Computers dice had values of {} and {},"
              " it's total for the round is {}".
              format(die1_value, die2_value,
                     self.dice_hand.get_round_score()))
        return die1_value, die2_value

    def computer_playing(self):
        """Call computer throw(), use evaluate() for values."""
        sentinel = True
        while sentinel:
            die_1_value, die_2_value = self.computer_throw()
            sentinel = self.computer.evaluate(
                die_1_value,
                die_2_value,
                self.dice_hand.get_round_score(),
                self.active_player.get_score()
            )
        if self.does_active_player_have_enough_points_to_win():
            print("Computer won! Game is restarting")
            self.end_active_players_turn()
            self.data_saving_at_the_end_of_the_game()
            self.start()
        else:
            self.end_active_players_turn()

    def adjust_difficulty(self, number):
        """Change computer objects difficulty attribute to number ."""
        self.computer.change_level_of_difficulty(number)

    def data_saving_at_the_end_of_the_game(self):
        """Create an histogram object and pass in players to it."""
        self.active_player.add_to_score(self.dice_hand.get_round_score())
        histogram.Histogram(self.player_one, self.player_two)

    @staticmethod
    def display_data():
        """Call histogram to display data from saved file."""
        histogram.Histogram.display()
