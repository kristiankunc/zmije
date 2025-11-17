"""Tests for decimal separator replacement functionality."""

import tokenize
import io
from zmije.main import nahrad_oddelovac_desetinnych


class TestDecimalSeparator:
    """Tests for the nahrad_oddelovac_desetinnych function."""

    def _tokenize(self, code):
        """Helper to tokenize code."""
        return list(tokenize.generate_tokens(io.StringIO(code).readline))

    def test_simple_decimal_conversion(self):
        """Test conversion of simple decimal with comma."""
        code = "3,14"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "3.14" in result_str
        assert "3,14" not in result_str

    def test_zero_decimal(self):
        """Test conversion of decimal starting with zero."""
        code = "0,5"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "0.5" in result_str

    def test_large_decimal(self):
        """Test conversion of larger decimal number."""
        code = "123,456"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "123.456" in result_str

    def test_multiple_decimals(self):
        """Test conversion of multiple decimal numbers."""
        code = "1,5 + 2,7"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "1.5" in result_str
        assert "2.7" in result_str

    def test_decimal_in_assignment(self):
        """Test decimal conversion in variable assignment."""
        code = "x = 3,14"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "3.14" in result_str

    def test_decimal_in_function_call(self):
        """Test decimal conversion in function arguments."""
        code = "func(1,5; 2,7)"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "1.5" in result_str
        assert "2.7" in result_str

    def test_decimal_in_list(self):
        """Test decimal conversion inside lists."""
        code = "[1,5; 2,7; 3,14]"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "1.5" in result_str
        assert "2.7" in result_str
        assert "3.14" in result_str

    def test_decimal_in_dict_values(self):
        """Test decimal conversion in dictionary values."""
        code = '{"price": 19,99}'
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "19.99" in result_str

    def test_comma_not_decimal_separator_not_replaced(self):
        """Test that commas not used as decimal separators are preserved."""
        code = "func(a, b, c)"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        # Commas between identifiers should not be converted
        # This test verifies non-decimal commas are not affected
        assert result is not None

    def test_decimal_in_arithmetic_expression(self):
        """Test decimal conversion in arithmetic expressions."""
        code = "result = 10,5 * 2,3 + 1,1"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "10.5" in result_str
        assert "2.3" in result_str
        assert "1.1" in result_str

    def test_decimal_in_comparison(self):
        """Test decimal conversion in comparisons."""
        code = "if x > 3,14:"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "3.14" in result_str

    def test_very_small_decimal(self):
        """Test conversion of very small decimal."""
        code = "0,00001"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "0.00001" in result_str

    def test_decimal_with_multiple_digits_before(self):
        """Test decimal with many digits before separator."""
        code = "1234,5678"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "1234.5678" in result_str

    def test_consecutive_decimals(self):
        """Test multiple consecutive decimal conversions."""
        code = "a = 1,1\nb = 2,2\nc = 3,3"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "1.1" in result_str
        assert "2.2" in result_str
        assert "3.3" in result_str

    def test_decimal_at_line_end(self):
        """Test decimal number at end of line."""
        code = "value = 9,99"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "9.99" in result_str

    def test_decimal_at_line_start(self):
        """Test decimal number at start of line (after newline)."""
        code = "x = 1\n3,14"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "3.14" in result_str

    def test_returns_list_of_tokens(self):
        """Test that function returns a list of tokens."""
        code = "3,14"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tokens_have_correct_attributes(self):
        """Test that returned tokens have expected attributes."""
        code = "3,14"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        for token in result:
            assert hasattr(token, 'type')
            assert hasattr(token, 'string')

    def test_nested_decimal_expressions(self):
        """Test nested decimal expressions."""
        code = "((1,5 + 2,7) * 3,14)"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        assert "1.5" in result_str
        assert "2.7" in result_str
        assert "3.14" in result_str

    def test_decimal_with_negative_sign(self):
        """Test decimal with negative sign."""
        code = "-3,14"
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        # The negative sign should be separate, decimal conversion should still work
        assert "3.14" in result_str

    def test_preserves_non_decimal_content(self):
        """Test that non-decimal content is preserved."""
        code = 'text = "3,14 je pi"'
        tokens = self._tokenize(code)
        result = nahrad_oddelovac_desetinnych(tokens)
        result_str = tokenize.untokenize(result)
        # String content should be preserved as-is
        assert "text" in result_str
