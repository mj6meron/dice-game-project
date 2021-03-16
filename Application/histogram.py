# written by Meron
"""Class to keep track of winners and losers history."""


class Histogram:
    """Declaring the attributes."""

    winner = None
    loser = None
    score_difference = 0
    file = "HighScore.txt"

    def __init__(self, player_1, player_2):
        """Initialize an object."""
        self.assigner(player_1, player_2)
        self.save(self.file)

    def assigner(self, player_1, player_2):
        """Initialize attributes."""
        if player_1.get_score() > player_2.get_score():
            self.winner = player_1
            self.loser = player_2
            s_d = abs(player_1.get_score() - player_2.get_score())
            self.score_difference = s_d
            return
        self.winner = player_2
        self.loser = player_1
        s_d = abs(player_1.get_score() - player_2.get_score())
        self.score_difference = s_d

    def save(self, the_file):
        """Save attributes to the file."""
        with open(the_file, 'a') as file:
            file.write(f"{self.winner.get_name()},"
                       f" {self.loser.get_name()},"
                       f" {self.score_difference} \n")

    @staticmethod
    def load():
        """Load as a list for each line from the file."""
        list_of_lines = []
        with open(Histogram.file, 'r') as file:
            for line in file:
                list_of_lines.append(line.rstrip('\n').split(','))
        return list_of_lines

    @staticmethod
    def display():
        """Display the history of games played."""
        list_from_file = Histogram.load()
        for i in list_from_file:
            print(f"Winner: {i[0]},"
                  f" against: {i[1]},"
                  f" Difference: {i[2]}")
