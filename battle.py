"""Battle manager for turn-based combat."""

from character import Character


class Battle:
    """Manages turn-based combat between two characters."""

    def __init__(self, hero: Character, enemy: Character) -> None:
        """
        Initialize a battle between two characters.

        Args:
            hero (Character): The player's character
            enemy (Character): The opposing character
        """
        self.hero = hero
        self.enemy = enemy
        self.round_number = 0

    def play_round(self) -> None:
        """
        Play a single round of combat:
        1. Hero attacks the enemy
        2. If the enemy is still alive, the enemy attacks the hero
        """
        self.round_number += 1

        # Hero attacks first
        self.hero.attack(self.enemy)

        # Enemy only retaliates if still alive
        if self.enemy.is_alive:
            self.enemy.attack(self.hero)

    def simulate_battle(self, verbose: bool = True) -> Character:
        """
        Run the full battle until one character is defeated.

        Args:
            verbose (bool): If True, print the state after each round.

        Returns:
            Character: The winning character
        """
        if verbose:
            print("=" * 55)
            print(f"BATTLE START: {self.hero.name} vs {self.enemy.name}")
            print("=" * 55)
            print(f"  {self.hero}")
            print(f"  {self.enemy}")
            print()

        while self.hero.is_alive and self.enemy.is_alive:
            self.play_round()

            if verbose:
                print(f"--- Round {self.round_number} ---")
                print(f"  {self.hero}")
                print(f"  {self.enemy}")
                print()

        # Determine winner
        winner = self.hero if self.hero.is_alive else self.enemy

        if verbose:
            print("=" * 55)
            print(f"BATTLE OVER - Winner: {winner.name}")
            print("=" * 55)

        return winner

    def __repr__(self) -> str:
        return (
            f"<Battle hero={self.hero.name!r} "
            f"enemy={self.enemy.name!r} "
            f"round={self.round_number}>"
        )
    