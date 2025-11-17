"""Tests for variable capitalization validation."""

import pytest
from zmije.main import validate_variables_capitalized, transpile


class TestValidateVariablesCapitalized:
    """Tests for the validate_variables_capitalized function."""

    def test_validate_capitalized_variables_passes(self):
        """Test that properly capitalized variables pass validation."""
        code = """
Proměnná = 5
Výsledek = 10
Název = "test"
"""
        # Should not raise
        validate_variables_capitalized(code)

    def test_validate_lowercase_variable_fails(self):
        """Test that lowercase variables fail validation."""
        code = "proměnná = 5"
        with pytest.raises(ValueError) as excinfo:
            validate_variables_capitalized(code)
        assert "proměnná" in str(excinfo.value)
        assert "capital letter" in str(excinfo.value)

    def test_validate_multiple_lowercase_variables(self):
        """Test validation catches first lowercase variable."""
        code = """
Správná = 1
špatná = 2
"""
        with pytest.raises(ValueError) as excinfo:
            validate_variables_capitalized(code)
        assert "špatná" in str(excinfo.value)

    def test_validate_allows_self(self):
        """Test that 'self' is allowed to be lowercase."""
        code = """
klasa Třída:
    def metoda(self):
        self.Atribut = 5
"""
        # Should not raise
        validate_variables_capitalized(code)

    def test_validate_allows_dunder_names(self):
        """Test that dunder names like __init__ are allowed."""
        code = """
if __name__ == "__main__":
    pass
"""
        # Should not raise
        validate_variables_capitalized(code)

    def test_validate_allows_attribute_names(self):
        """Test that attribute names (after dot) are allowed to be lowercase."""
        code = """
Objekt.atribut = 5
Hodnota = Objekt.metoda()
"""
        # Should not raise
        validate_variables_capitalized(code)

    def test_validate_mixed_czech_quotes(self):
        """Test validation works with Czech quotes."""
        code = 'Zpráva = „Ahoj světe"'
        # Should not raise
        validate_variables_capitalized(code)

    def test_validate_with_keywords(self):
        """Test that Czech keywords are not flagged."""
        code = """
Quando x > 0:
    Když x < 10:
        Vytiskni("test")
"""
        # Should not raise - Když is a keyword
        validate_variables_capitalized(code)

    def test_validate_error_includes_line_number(self):
        """Test that error message includes line number."""
        code = """
Správná = 1
Taky_správná = 2
špatná = 3
"""
        with pytest.raises(ValueError) as excinfo:
            validate_variables_capitalized(code)
        assert "line 3" in str(excinfo.value).lower() or "3" in str(excinfo.value)

    def test_validate_cls_allowed(self):
        """Test that 'cls' is allowed for class methods."""
        code = """
klasa Třída:
    @classmethod
    def metoda(cls):
        Výsledek = cls.atribut
"""
        # Should not raise
        validate_variables_capitalized(code)

    def test_transpile_fails_with_lowercase_variables(self):
        """Test that transpile fails when variables are lowercase."""
        code = "proměnná = 5"
        with pytest.raises(ValueError) as excinfo:
            transpile(code)
        assert "capital letter" in str(excinfo.value)

    def test_transpile_succeeds_with_capitalized_variables(self):
        """Test that transpile succeeds when variables are capitalized."""
        code = """
Číslo = 5
Výsledek = Číslo + 3
Vytiskni(Výsledek)
"""
        result = transpile(code)
        assert "print" in result
        assert "5" in result

    def test_validate_numeric_variable_names(self):
        """Test that variables starting with numbers fail appropriately."""
        # Python doesn't allow variable names starting with numbers,
        # so this should be caught by tokenizer before our validation
        code = "5Proměnná = 10"
        # This should fail during tokenization, not our validation
        with pytest.raises((ValueError, Exception)):
            validate_variables_capitalized(code)

    def test_validate_with_underscores(self):
        """Test that capitalization works with underscored variable names."""
        code = """
Moje_proměnná = 5
KONSTANTA = 10
"""
        # Should not raise - both start with capital letter
        validate_variables_capitalized(code)

    def test_validate_lowercase_with_underscore(self):
        """Test that lowercase with underscore fails."""
        code = "moje_proměnná = 5"
        with pytest.raises(ValueError) as excinfo:
            validate_variables_capitalized(code)
        assert "moje_proměnná" in str(excinfo.value)
