"""Dice class for introducing randomness into damage calculations."""

import random


class Dice:
    """An n-sided dice that can be rolled for a random result."""

    def __init__(self, sides: int = 6) -> None:
        """
        Create a dice with the given number of sides.

        Args:
            sides (int): Number of sides (must be >= 2). Defaults to 6.
        """
        if sides < 2:
            raise ValueError("A dice must have at least 2 sides")
        self.sides = sides

    def roll(self) -> int:
        """Roll the dice and return a random integer between 1 and sides (inclusive)."""
        return random.randint(1, self.sides)

    def __call__(self) -> int:
        """
        Allow the dice object itself to be called like a function.
        Example: d20 = Dice(20); result = d20()
        """
        return self.roll()

    def __repr__(self) -> str:
        return f"Dice(sides={self.sides})"
    