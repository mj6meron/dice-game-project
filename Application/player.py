"""Player class has no imports."""


class Player():
    """Player class."""

    name = None
    score = None

    def __init__(self, name):
        """Initialize its attributes."""
        self.score = 0
        self.name = name

    def rename(self, name):
        """Rename old name and return new name."""
        self.name = name
        return self.name

    def get_name(self):
        """Return name."""
        return self.name

    def get_score(self):
        """Return score."""
        return self.score

    def add_to_score(self, round_score):
        """Return new score."""
        self.score += round_score
        return self.score

    def empty_the_score(self):
        """Change score to 0."""
        self.score = 0
