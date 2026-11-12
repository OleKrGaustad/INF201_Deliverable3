"""Items that characters can equip (currently only weapons)."""

from dice import Dice


class Weapon:
    """A weapon that deals damage based on a dice roll."""

    def __init__(self, name: str, damage_dice: Dice) -> None:
        """
        Args:
            name (str): Name of the weapon (e.g. "Longsword", "Fire Staff")
            damage_dice (Dice): The dice used to determine damage
        """
        self.name = name
        self.damage_dice = damage_dice

    def roll_damage(self) -> int:
        """Roll the weapon's damage dice and return the result."""
        return self.damage_dice.roll()

    def __repr__(self) -> str:
        return f"Weapon(name={self.name!r}, damage_dice={self.damage_dice})"

    def __str__(self) -> str:
        return f"{self.name} ({self.damage_dice})"
    