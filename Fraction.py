
from __future__ import annotations

from math import gcd


class Fraction:
    """A fraction with a numerator and a positive denominator"""


#initialization

    def __init__(self, numerator: int, denominator: int = 1) -> None:
        if isinstance(numerator, bool) or not isinstance(numerator, int):
            raise TypeError("Numerator must be an integer")

        if isinstance(denominator, bool) or not isinstance(denominator, int):
            raise TypeError("Denominator must be an integer")

        if denominator <= 0:
            raise ValueError("Denominator must be positive")

        divisor = gcd(numerator, denominator)
        self._numerator = numerator // divisor
        self._denominator = denominator // divisor

    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator



#Helpers
    @staticmethod
    def _coerce(other):
        """Turns an int into a fraction, leave Fractions alone, else None"""
        if isinstance(other, Fraction):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Fraction(other)
        return None

    @staticmethod
    def _from_ratio(num: int, den: int) -> Fraction:
        """Makes a fraction with a positive denominator"""
        if den < 0:
            num, den = -num, -den
        return Fraction(num, den)



#string representations
    def __repr__(self) -> str:
        return f"Fraction({self._numerator}, {self._denominator})"

    def __str__(self) -> str:
        if self._denominator == 1:
            return str(self._numerator)
        return f"{self._numerator}/{self._denominator}"

    

#comparisons (cross multiply since denominator > 0 )

    def __eq__(self, other: object):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return (
            self._numerator == o._numerator
            and self._denominator == o._denominator
        )

    def __ne__(self, other: object):
        result = self.__eq__(other)
        return result if result is NotImplemented else not result

    def __lt__(self, other: object):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._numerator * o._denominator < o._numerator * self._denominator

    def __le__(self, other: object):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._numerator * o._denominator <= o._numerator * self._denominator

    def __gt__(self, other: object):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._numerator * o._denominator > o._numerator * self._denominator

    def __ge__(self, other: object):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._numerator * o._denominator >= o._numerator * self._denominator


# spesials
    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(
            self._numerator * o._denominator
            + o._numerator * self._denominator,
            self._denominator * o._denominator,
        )

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(
            self._numerator * o._denominator
            - o._numerator * self._denominator,
            self._denominator * o._denominator,
        )

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(
            self._numerator * o._numerator,
            self._denominator * o._denominator,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        if o._numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return self._from_ratio(
            self._numerator * o._denominator,
            self._denominator * o._numerator,
        )