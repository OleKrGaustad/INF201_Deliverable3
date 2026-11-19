import pytest

from Temperature import Temperature


# (celsius, fahrenheit, kelvin)
REFERENCE_POINTS = [
    (-273.15, -459.67, 0.0),     # absolute zero
    (-40.0, -40.0, 233.15),      # Celsius-fahrenheit crossover
    (0.0, 32.0, 273.15),         # freezing point of water
    (37.0, 98.6, 310.15),        # human body temperature
    (100.0, 212.0, 373.15),      # boiling point of water
]

TOLERANCE = 1e-9


# 1. Initialization

class TestInitialization:

    def test_default_unit_is_celsius(self):
        t = Temperature(25)
        assert t.unit == "C"
        assert t.value == 25.0

    @pytest.mark.parametrize("unit", ["c", "C", "f", "F", "k", "K"])
    def test_units_are_case_insensitive(self, unit):
        assert Temperature(300, unit).unit == unit.upper()

    def test_value_is_read_only(self):
        t = Temperature(25, "C")
        with pytest.raises(AttributeError):
            t.value = 30

    def test_unit_is_read_only(self):
        t = Temperature(25, "C")
        with pytest.raises(AttributeError):
            t.unit = "F"


# 2. Validation

class TestValidation:

    @pytest.mark.parametrize(
        "bad_unit",
        ["X", "", "Celsius", "CF", "°C"]
    )
    def test_invalid_unit_raises(self, bad_unit):
        with pytest.raises(ValueError):
            Temperature(20, bad_unit)

    @pytest.mark.parametrize(
        "value, unit",
        [
            (-273.16, "C"),
            (-459.68, "F"),
            (-0.001, "K"),
        ]
    )
    def test_below_absolute_zero_raises(self, value, unit):
        with pytest.raises(ValueError):
            Temperature(value, unit)


# 3. Conversions

class TestConversions:

    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_from_celsius(self, c, f, k):
        t = Temperature(c, "C")

        assert t.to_celsius() == pytest.approx(c, abs=TOLERANCE)
        assert t.to_fahrenheit() == pytest.approx(f, abs=TOLERANCE)
        assert t.to_kelvin() == pytest.approx(k, abs=TOLERANCE)

    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_from_fahrenheit(self, c, f, k):
        t = Temperature(f, "F")

        assert t.to_celsius() == pytest.approx(c, abs=TOLERANCE)
        assert t.to_fahrenheit() == pytest.approx(f, abs=TOLERANCE)
        assert t.to_kelvin() == pytest.approx(k, abs=TOLERANCE)

    @pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
    def test_from_kelvin(self, c, f, k):
        t = Temperature(k, "K")

        assert t.to_celsius() == pytest.approx(c, abs=TOLERANCE)
        assert t.to_fahrenheit() == pytest.approx(f, abs=TOLERANCE)
        assert t.to_kelvin() == pytest.approx(k, abs=TOLERANCE)

    def test_convert_to(self):
        t = Temperature(25, "C")

        f = t.convert_to("F")
        k = t.convert_to("K")

        assert f.value == pytest.approx(77.0, abs=TOLERANCE)
        assert f.unit == "F"

        assert k.value == pytest.approx(298.15, abs=TOLERANCE)
        assert k.unit == "K"

    def test_convert_to_case_insensitive(self):
        t = Temperature(25, "C")

        f = t.convert_to("f")
        k = t.convert_to("k")

        assert f.value == pytest.approx(77.0, abs=TOLERANCE)
        assert f.unit == "F"

        assert k.value == pytest.approx(298.15, abs=TOLERANCE)
        assert k.unit == "K"

    def test_convert_to_invalid_unit_raises(self):
        with pytest.raises(ValueError):
            Temperature(25, "C").convert_to("X")


# 4. Round-trip conversions

class TestRoundTrip:

    @pytest.mark.parametrize("celsius", [-273.15, -40, 0, 37, 100])
    def test_c_f_k_c_round_trip(self, celsius):
        original = Temperature(celsius, "C")

        result = (
            original
            .convert_to("F")
            .convert_to("K")
            .convert_to("C")
        )

        assert result.unit == "C"
        assert result.value == pytest.approx(celsius, abs=TOLERANCE)


# 5. cross unit comparisons

class TestComparisons:

    def test_equal(self):
        assert Temperature(0, "C") == Temperature(32, "F")

    def test_not_equal(self):
        assert Temperature(0, "C") != Temperature(100, "F")

    def test_less_than(self):
        assert Temperature(0, "C") < Temperature(50, "F")

    def test_less_equal(self):
        assert Temperature(0, "C") <= Temperature(32, "F")

    def test_greater_than(self):
        assert Temperature(100, "C") > Temperature(100, "F")

    def test_greater_equal(self):
        assert Temperature(100, "C") >= Temperature(212, "F")

    def test_comparison_with_other_types(self):
        t = Temperature(25, "C")

        assert t.__eq__(5) is NotImplemented
        assert t.__ne__(5) is NotImplemented
        assert t.__lt__(5) is NotImplemented
        assert t.__le__(5) is NotImplemented
        assert t.__gt__(5) is NotImplemented
        assert t.__ge__(5) is NotImplemented
        
# 6. formatting

class TestFormatting:

    def test_str(self):
        assert str(Temperature(25, "C")) == "25.00 °C"
        assert str(Temperature(98.6, "F")) == "98.60 °F"
        assert str(Temperature(273.15, "K")) == "273.15 K"

    def test_repr(self):
        assert repr(Temperature(25, "C")) == "Temperature(25.0, 'C')"