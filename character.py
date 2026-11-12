"""Character classes for the mini-RPG battle simulator."""

from typing import Optional

from items import Weapon


class Character:
    """Represents a character in the RPG."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Optional[Weapon] = None,
    ) -> None:
        """
        Initialise the Character.

        Args:
            name (str): The name of the character.
            hp_max (int): Max hit points (default = 100)
            damage (int): Base damage dealt when character has no weapon (default = 10)
            weapon (Weapon | None): Optional equipped weapon
        """
        self.name = name
        self._hp = hp_max
        self.hp_max = hp_max
        self.damage = damage
        self.weapon = weapon

    @property
    def hp(self) -> int:
        """Public read-only property to inspect current HP."""
        return self._hp

    @property
    def is_alive(self) -> bool:
        """Read-only property. True if the character has HP remaining."""
        return self._hp > 0

    def take_damage(self, amount: int) -> None:
        """Apply damage to this character. HP never goes below 0."""
        if amount < 0:
            raise ValueError("Damage amount cannot be negative")
        self._hp = max(self._hp - amount, 0)

    def heal(self, amount: int) -> None:
        """Restore hit points. HP never exceeds hp_max."""
        if amount < 0:
            raise ValueError("Heal amount cannot be negative")
        self._hp = min(self._hp + amount, self.hp_max)

    def attack(self, target: "Character") -> None:
        """
        Attack another character.
        Uses the equipped weapon's damage roll if present,
        otherwise falls back to the character's base damage.
        """
        if self.weapon is not None:
            damage = self.weapon.roll_damage()
        else:
            damage = self.damage

        target.take_damage(damage)

    def introduce(self) -> None:
        """Print a short introduction."""
        print(f"Hi, my name is {self.name}!")

    def __repr__(self) -> str:
        weapon_str = f", weapon={self.weapon}" if self.weapon else ""
        return (
            f"<Character name={self.name!r} "
            f"hp={self.hp}/{self.hp_max} "
            f"damage={self.damage}{weapon_str} "
            f"alive={self.is_alive}>"
        )

    def __str__(self) -> str:
        status = "alive" if self.is_alive else "defeated"
        weapon_info = f", weapon={self.weapon.name}" if self.weapon else ""
        return (
            f"Character: {self.name} "
            f"({self.hp}/{self.hp_max} HP, {self.damage} base dmg{weapon_info}) [{status}]"
        )


class Warrior(Character):
    """Defensive specialist. Reduces incoming damage with armor."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Optional[Weapon] = None,
        armor: int = 5,
    ) -> None:
        super().__init__(name=name, hp_max=hp_max, damage=damage, weapon=weapon)
        self.armor = armor

    def take_damage(self, amount: int) -> None:
        """
        Reduce incoming damage by the warrior's armor before applying it.
        Damage after armor reduction cannot go below 0.
        """
        if amount < 0:
            raise ValueError("Damage amount cannot be negative")

        reduced_damage = max(amount - self.armor, 0)
        self._hp = max(self._hp - reduced_damage, 0)

    def __repr__(self) -> str:
        weapon_str = f", weapon={self.weapon}" if self.weapon else ""
        return (
            f"<Warrior name={self.name!r} "
            f"hp={self.hp}/{self.hp_max} "
            f"damage={self.damage} "
            f"armor={self.armor}{weapon_str} "
            f"alive={self.is_alive}>"
        )

    def __str__(self) -> str:
        status = "alive" if self.is_alive else "defeated"
        weapon_info = f", weapon={self.weapon.name}" if self.weapon else ""
        return (
            f"Warrior: {self.name} "
            f"({self.hp}/{self.hp_max} HP, {self.damage} base dmg, "
            f"armor={self.armor}{weapon_info}) [{status}]"
        )


class Mage(Character):
    """Resource-based attacker. Uses mana for powerful magic attacks."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Optional[Weapon] = None,
        mana_max: int = 30,
    ) -> None:
        super().__init__(name=name, hp_max=hp_max, damage=damage, weapon=weapon)
        self.mana_max = mana_max
        self.mana = mana_max  # start at full mana

    def attack(self, target: "Character") -> None:
        """
        Magical attack logic:
        - If mana >= 10: spend 10 mana and deal double damage (ignores weapon).
        - If mana < 10: fall back to normal attack (uses weapon if equipped)
          and restore 5 mana.
        """
        if self.mana >= 10:
            # Magical spell attack – ignores weapon
            self.mana -= 10
            damage = self.damage * 2
            target.take_damage(damage)
        else:
            # Not enough mana → normal attack + small mana restore
            if self.weapon is not None:
                damage = self.weapon.roll_damage()
            else:
                damage = self.damage

            target.take_damage(damage)
            self.mana = min(self.mana + 5, self.mana_max)

    def __repr__(self) -> str:
        weapon_str = f", weapon={self.weapon}" if self.weapon else ""
        return (
            f"<Mage name={self.name!r} "
            f"hp={self.hp}/{self.hp_max} "
            f"damage={self.damage} "
            f"mana={self.mana}/{self.mana_max}{weapon_str} "
            f"alive={self.is_alive}>"
        )

    def __str__(self) -> str:
        status = "alive" if self.is_alive else "defeated"
        weapon_info = f", weapon={self.weapon.name}" if self.weapon else ""
        return (
            f"Mage: {self.name} "
            f"({self.hp}/{self.hp_max} HP, {self.damage} base dmg, "
            f"mana={self.mana}/{self.mana_max}{weapon_info}) [{status}]"
        )
