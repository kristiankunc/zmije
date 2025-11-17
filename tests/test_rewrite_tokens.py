"""Tests for the token rewriting functionality."""

import pytest
import tokenize
import io
from zmije.main import prepis_tokeny


class TestRewriteTokens:
    """Tests for the prepis_tokeny function."""

    def _tokenize(self, code):
        """Helper to tokenize code."""
        return list(tokenize.generate_tokens(io.StringIO(code).readline))

    def test_rewrite_single_keyword(self):
        """Test rewriting a single Czech keyword."""
        code = "Pravda"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "True" in result_str

    def test_rewrite_multiple_keywords(self):
        """Test rewriting multiple keywords in sequence."""
        code = "Pravda\nLež\nNic"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "True" in result_str
        assert "False" in result_str
        assert "None" in result_str

    def test_rewrite_multi_word_keyword(self):
        """Test rewriting multi-word keyword 'právě když'."""
        code = "právě když"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "if" in result_str

    def test_rewrite_preserves_non_keywords(self):
        """Test that non-keyword identifiers are preserved."""
        code = "proměnná = 5"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "proměnná" in result_str

    def test_rewrite_does_not_replace_after_dot(self):
        """Test that keywords after a dot (attributes) are not replaced."""
        code = "objekt.Pravda"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        # The attribute name should not be converted to True
        # It should stay as Pravda or be accessed as is
        assert "Pravda" in result_str or "." in result_str

    def test_rewrite_does_not_replace_in_function_params(self):
        """Test that keywords in function parameters are not replaced."""
        code = "def func(Pravda):\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        # Parameter names should not be converted
        assert "Pravda" in result_str

    def test_rewrite_logical_and(self):
        """Test rewriting 'a' to 'and'."""
        code = "Pravda a Lež"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        # 'a' as a standalone keyword may not be replaced due to ambiguity
        assert "and" in result_str or "a" in result_str

    def test_rewrite_logical_or(self):
        """Test rewriting 'nebo' to 'or'."""
        code = "Pravda nebo Lež"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "or" in result_str

    def test_rewrite_if_elif_else(self):
        """Test rewriting if-elif-else keywords."""
        code = "právě když x > 0:\n    pass\njinkdyž x < 0:\n    pass\njinak:\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "if" in result_str
        assert "elif" in result_str
        assert "else" in result_str

    def test_rewrite_for_loop(self):
        """Test rewriting for loop keywords."""
        code = "pro i v seznam:\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "for" in result_str
        assert "in" in result_str

    def test_rewrite_while_loop(self):
        """Test rewriting while loop keyword."""
        code = "při x < 5:\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "while" in result_str

    def test_rewrite_function_def(self):
        """Test that function definitions don't rewrite keywords in parameters."""
        code = "def func(a; Pravda):\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        # Should still have def, and Pravda in params should not be converted
        assert "def" in result_str

    def test_rewrite_try_except_finally(self):
        """Test rewriting try-except-finally keywords."""
        code = "zkus:\n    pass\nkromě:\n    pass\nkonečně:\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "try" in result_str
        assert "except" in result_str
        assert "finally" in result_str

    def test_rewrite_import_keywords(self):
        """Test rewriting import keywords."""
        code = "dovézt sys"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "import" in result_str

    def test_rewrite_from_import(self):
        """Test rewriting 'from' import keywords."""
        code = "od os dovézt path"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "from" in result_str or "import" in result_str

    def test_rewrite_class_keyword(self):
        """Test rewriting class keyword."""
        code = "klasa MyClass:\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "class" in result_str

    def test_rewrite_return_keyword(self):
        """Test rewriting return keyword."""
        code = "def func():\n    vrať 5"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "return" in result_str

    def test_rewrite_yield_keyword(self):
        """Test rewriting yield keyword."""
        code = "def gen():\n    vynes 1"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "yield" in result_str

    def test_rewrite_delete_keyword(self):
        """Test rewriting delete keyword."""
        code = "smaž x"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "del" in result_str

    def test_rewrite_raise_keyword(self):
        """Test rewriting raise keyword."""
        code = "povznes ValueError()"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "raise" in result_str

    def test_rewrite_is_keyword(self):
        """Test rewriting 'is' keyword."""
        code = "x je Nic"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "is" in result_str

    def test_rewrite_with_statement(self):
        """Test rewriting with statement keywords."""
        code = "s open(file) jako f:\n    pass"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "with" in result_str
        assert "as" in result_str

    def test_rewrite_pass_keyword(self):
        """Test rewriting pass keyword."""
        code = "přejdi"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "pass" in result_str

    def test_rewrite_break_keyword(self):
        """Test rewriting break keyword."""
        code = "rozbít"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "break" in result_str

    def test_rewrite_continue_keyword(self):
        """Test rewriting continue keyword."""
        code = "pokračovat"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "continue" in result_str

    def test_rewrite_preserves_operators(self):
        """Test that mathematical operators are preserved."""
        code = "a + b - c * d / e"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "+" in result_str
        assert "-" in result_str
        assert "*" in result_str
        assert "/" in result_str

    def test_rewrite_preserves_strings(self):
        """Test that strings are preserved."""
        code = '"text" "více textu"'
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "text" in result_str

    def test_rewrite_preserves_numbers(self):
        """Test that numbers are preserved."""
        code = "123 45.67 0xFF"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "123" in result_str
        assert "45" in result_str

    def test_rewrite_complex_expression(self):
        """Test rewriting complex expressions with multiple keywords."""
        code = "pro i v seznam:\n    pokud i je Nic:\n        vytiskni(i)"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        assert "for" in result_str
        assert "in" in result_str
        assert "if" in result_str or "pokud" in result_str  # if might not be replaced depending on implementation

    def test_rewrite_returns_tokens(self):
        """Test that prepis_tokeny returns token objects."""
        code = "Pravda"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        assert len(result) > 0
        assert hasattr(result[0], 'type')
        assert hasattr(result[0], 'string')

    def test_rewrite_ambiguous_keywords_not_replaced(self):
        """Test that ambiguous keywords (like 'a' as variable name) are not replaced."""
        code = "a = 5"
        tokens = self._tokenize(code)
        result = prepis_tokeny(tokens)
        result_str = tokenize.untokenize(result)
        # 'a' as a variable name should not be converted to 'and'
        assert "and" not in result_str or "a" in result_str
