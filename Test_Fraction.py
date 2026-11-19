import pytest

from Fraction import Fraction


class TestFraction:

# initialization

    def test_basic_fraction(self): # vanlig brøk
        f = Fraction(3, 4)
        assert f.numerator == 3
        assert f.denominator == 4

    def test_default_denominator(self): # at never automatisk blir 1 på man ikke oppgir en nevner 
        f = Fraction(5)
        assert f.numerator == 5
        assert f.denominator == 1

    def test_fraction_is_reduced(self): #at brøken forkortes automatisk
        f = Fraction(6, 8)
        assert f.numerator == 3
        assert f.denominator == 4

    def test_zero_fraction(self):
        f = Fraction(0, 5)
        assert f.numerator == 0
        assert f.denominator == 1

    def test_invalid_denominator(self): #at klassen ikke lar ugyldige nevnere være med 
        with pytest.raises(ValueError):
            Fraction(1, 0)
        with pytest.raises(ValueError):
            Fraction(1, -2)

    def test_invalid_types(self):
        with pytest.raises(TypeError):
            Fraction(1.5, 2)

        with pytest.raises(TypeError):
            Fraction(1, 2.5)

        with pytest.raises(TypeError):
            Fraction("1", 2)

        with pytest.raises(TypeError):
            Fraction(1, True)

# comparisons

    def test_equal(self):
        assert Fraction(1, 2) == Fraction(2, 4) 

    def test_not_equal(self):
        assert Fraction(1, 2) != Fraction(1, 3)

    def test_less_than(self):
        assert Fraction(1, 3) < Fraction(1, 2)

    def test_less_than_or_equal(self):
        assert Fraction(1, 2) <= Fraction(2, 4)
        assert Fraction(1, 3) <= Fraction(1, 2)

    def test_greater_than(self):
        assert Fraction(3, 4) > Fraction(1, 2)

    def test_greater_than_or_equal(self):
        assert Fraction(1, 2) >= Fraction(2, 4)
        assert Fraction(3, 4) >= Fraction(1, 2)

# spesials

    def test_addition(self):
        assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6) #at man kan legge to brøker sammen

    def test_subtraction(self):
        assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6) #at man kan trekke brøker fra hverandre

    def test_multiplication(self):
        assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2) #at man kan gange to brøker

    def test_division(self):
        assert Fraction(1, 2) / Fraction(1, 4) == Fraction(2, 1) # at man kan dele en brøk på en anenn

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError): #tester om man får feil om man deler på 0
            Fraction(1, 2) / Fraction(0, 1)
