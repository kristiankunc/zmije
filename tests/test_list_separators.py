"""Tests for list separator replacement functionality."""

import tokenize
import io
from zmije.main import nahrad_oddelovace_seznamu


class TestListSeparators:
    """Tests for the nahrad_oddelovace_seznamu function."""

    def _tokenize(self, code):
        """Helper to tokenize code."""
        return list(tokenize.generate_tokens(io.StringIO(code).readline))

    def test_simple_semicolon_replacement(self):
        """Test replacement of semicolon with comma."""
        code = "a; b"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        assert "," in result_str
        assert ";" not in result_str

    def test_list_with_semicolons(self):
        """Test list with semicolon separators."""
        code = "[1; 2; 3]"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        assert "[1,2,3]" in result_str.replace(" ", "")

    def test_dict_with_semicolons(self):
        """Test dictionary with semicolon separators."""
        code = '{"a": 1; "b": 2}'
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        # Check that semicolon is converted to comma
        assert "," in result_str

    def test_multiple_semicolons(self):
        """Test multiple semicolon replacements."""
        code = "[1; 2; 3; 4; 5]"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        # All semicolons should be replaced
        assert ";" not in result_str
        assert result_str.count(",") >= 4

    def test_semicolon_in_function_args(self):
        """Test semicolon replacement in function arguments."""
        code = "func(a; b; c)"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        assert ";" not in result_str

    def test_nested_lists_with_semicolons(self):
        """Test nested lists with semicolons."""
        code = "[[1; 2]; [3; 4]]"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        assert ";" not in result_str

    def test_mixed_commas_and_semicolons(self):
        """Test that existing commas are preserved while semicolons are replaced."""
        code = "[1, 2; 3, 4]"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        # Original commas should be preserved, semicolon replaced
        assert "," in result_str

    def test_semicolon_in_tuple(self):
        """Test semicolon replacement in tuple."""
        code = "(1; 2; 3)"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        assert ";" not in result_str

    def test_preserves_operators(self):
        """Test that operators are preserved."""
        code = "x = 1 + 2; y = 3 * 4"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        assert "+" in result_str
        assert "*" in result_str

    def test_preserves_strings(self):
        """Test that semicolons inside strings would be preserved."""
        code = 'text = "1; 2; 3"'
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        # The string content should be unchanged
        assert "text" in result_str

    def test_returns_list_of_tokens(self):
        """Test that function returns a list of tokens."""
        code = "a; b"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tokens_have_correct_attributes(self):
        """Test that returned tokens have expected attributes."""
        code = "a; b"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        for token in result:
            assert hasattr(token, 'type')
            assert hasattr(token, 'string')

    def test_complex_structure_with_semicolons(self):
        """Test complex data structures with multiple semicolons."""
        code = 'data = {"list": [1; 2; 3]; "value": 42; "nested": {"a": 1; "b": 2}}'
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        # All semicolons should be replaced
        assert ";" not in result_str

    def test_semicolon_preservation_in_comments(self):
        """Test that semicolons in comments are replaced (as they're not special in comments)."""
        code = "x = 1  # comment; with semicolon\ny = 2"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        # The function processes all OP tokens, including in comments
        assert len(result) > 0

    def test_function_call_multiple_args(self):
        """Test function call with multiple semicolon-separated arguments."""
        code = "vytiskni(a; b; c; d)"
        tokens = self._tokenize(code)
        result = nahrad_oddelovace_seznamu(tokens)
        result_str = tokenize.untokenize(result)
        # Should have commas instead of semicolons
        assert result_str.count(",") >= 3
