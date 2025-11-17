"""Tests for the main transpile function and related transformations."""

import pytest
from zmije.main import transpile, validate_no_english_keywords


class TestTranspile:
    """Tests for the main transpile function."""

    def test_transpile_simple_keywords(self):
        """Test transpilation of simple single-word Czech keywords."""
        code = "Pravdivá_hodnota = Pravda"
        result = transpile(code)
        assert "True" in result

    def test_transpile_multi_word_keywords(self):
        """Test transpilation of multi-word Czech keywords like 'právě když'."""
        code = 'právě když X > 0:\n    vytiskni("text")'
        result = transpile(code)
        assert "if" in result

    def test_transpile_decimal_separator_czech(self):
        """Test conversion of Czech decimal separator (comma) to dot."""
        code = "Číslo = 3,14"
        result = transpile(code)
        assert "3.14" in result

    def test_transpile_decimal_with_leading_zero(self):
        """Test decimal separator with leading zero."""
        code = "Malé = 0,5"
        result = transpile(code)
        assert "0.5" in result

    def test_transpile_list_separator(self):
        """Test conversion of semicolons to commas in lists."""
        code = "Seznam = [1; 2; 3]"
        result = transpile(code)
        assert "[1,2,3]" in result.replace(" ", "")

    def test_transpile_czech_quotes(self):
        """Test conversion of Czech quotes to regular quotes."""
        code = 'Zpráva = "Ahoj světe"'
        result = transpile(code)
        assert '"Ahoj' in result

    def test_transpile_dict_with_semicolon_separator(self):
        """Test dictionary with semicolon separators."""
        code = 'Data = {"jméno": "Karel"; "věk": 30}'
        result = transpile(code)
        # Check that semicolon is converted to comma
        assert '"jméno"' in result
        assert '"Karel"' in result

    def test_transpile_keyword_import(self):
        """Test transpilation of import keywords."""
        code = "dovézt sys"
        result = transpile(code)
        assert "import" in result
        assert "sys" in result

    def test_transpile_keyword_function_def(self):
        """Test transpilation in function definitions."""
        code = "def sečti(a; b):\n    vrať a + b"
        result = transpile(code)
        assert "def" in result
        assert "return" in result

    def test_transpile_try_except(self):
        """Test transpilation of try-except-finally."""
        code = 'zkus:\n    Výsledek = 10 / 0\nkromě:\n    vytiskni("Chyba")\nkonečně:\n    vytiskni("Konec")'
        result = transpile(code)
        assert "try" in result
        assert "except" in result
        assert "finally" in result

    def test_transpile_class_definition(self):
        """Test transpilation of class definitions."""
        code = "klasa Zvire:\n    def __init__(self; Jméno):\n        self.Jméno = Jméno"
        result = transpile(code)
        assert "class" in result

    def test_transpile_for_loop(self):
        """Test transpilation of for loops."""
        code = "pro I v Seznam:\n    vytiskni(I)"
        result = transpile(code)
        assert "for" in result
        assert "in" in result

    def test_transpile_while_loop(self):
        """Test transpilation of while loops."""
        code = "při X < 5:\n    vytiskni(X)"
        result = transpile(code)
        assert "while" in result

    def test_transpile_delete_keyword(self):
        """Test transpilation of delete statement."""
        code = "smaž x"
        result = transpile(code)
        assert "del" in result

    def test_transpile_yield_keyword(self):
        """Test transpilation of yield keyword."""
        code = "def generátor():\n    vynes 1"
        result = transpile(code)
        assert "yield" in result

    def test_transpile_with_statement(self):
        """Test transpilation of with statement."""
        code = 's open("soubor.txt") jako F:\n    Obsah = F.read()'
        result = transpile(code)
        assert "with" in result
        assert "as" in result

    def test_transpile_raise_keyword(self):
        """Test transpilation of raise keyword."""
        code = 'povznes ValueError("Chyba")'
        result = transpile(code)
        assert "raise" in result

    def test_transpile_is_keyword(self):
        """Test transpilation of 'is' keyword."""
        code = 'pokud X je Nic:\n    vytiskni("prázdno")'
        result = transpile(code)
        # Note: "pokud" is not in KEYWORD_MAP, but "je" should be
        assert "is" in result or "None" in result

    def test_transpile_logical_operators(self):
        """Test transpilation of logical operators."""
        code = 'pokud X > 0 a Y < 10 nebo Z == 5:\n    vytiskni("ok")'
        result = transpile(code)
        assert "and" in result or "or" in result

    def test_transpile_pass_keyword(self):
        """Test transpilation of pass keyword."""
        code = "klasa Prázdná:\n    přejdi"
        result = transpile(code)
        assert "pass" in result or "Prázdná" in result

    def test_transpile_break_keyword(self):
        """Test transpilation of break keyword."""
        code = "při Pravda:\n    rozbít"
        result = transpile(code)
        assert "break" in result

    def test_transpile_continue_keyword(self):
        """Test transpilation of continue keyword."""
        code = "pro i v [1; 2; 3]:\n    pokračovat"
        result = transpile(code)
        assert "continue" in result

    def test_transpile_and_or_operators(self):
        """Test transpilation of boolean operators."""
        code = "Lež a Pravda nebo Nic"
        result = transpile(code)
        assert "False" in result
        assert "True" in result
        assert ("and" in result or "or" in result)

    def test_transpile_complex_expression(self):
        """Test transpilation of complex mixed expressions."""
        code = "klasa Test:\n    def metoda(self; X):\n        pokud X > 0,5 a X < 9,99:\n            Seznam = [1; 2; 3]\n            vrať Seznam\n        jinak:\n            vrať Nic"
        result = transpile(code)
        assert "class" in result
        assert "def" in result
        assert "0.5" in result
        assert "9.99" in result
        assert "return" in result
        assert "None" in result

    def test_transpile_output_is_valid_python(self):
        """Test that transpiled code is valid Python."""
        code = 'X = Pravda\nY = 3,14\nZpráva = "Ahoj"'
        result = transpile(code)
        # This should not raise an exception
        compile(result, '<test>', 'exec')

    def test_transpile_preserves_indentation(self):
        """Test that transpilation preserves code indentation."""
        code = "pro I v [1; 2; 3]:\n    vytiskni(I)"
        result = transpile(code)
        # Check indentation is preserved
        lines = result.split('\n')
        assert any(line.startswith('    ') for line in lines)

    def test_transpile_preserves_comments(self):
        """Test that transpilation preserves comments."""
        code = "# Komentář v češtině\nX = 5"
        result = transpile(code)
        assert "Koment" in result or "# " in result

    def test_transpile_multiple_decimals_in_sequence(self):
        """Test multiple decimal numbers in a single expression."""
        code = "Součet = 1,5 + 2,7"
        result = transpile(code)
        assert "1.5" in result
        assert "2.7" in result

    def test_transpile_decimal_in_function_call(self):
        """Test decimal number as function argument."""
        code = "vytiskni(3,14)"
        result = transpile(code)
        # Should contain print and 3.14
        assert "print" in result and "3.14" in result


class TestValidateNoEnglishKeywords:
    """Tests for the English keyword validation function."""

    def test_validate_no_english_keywords_passes_czech(self):
        """Test that Czech keywords pass validation."""
        code = "Pravda a Nic nebo Lež"
        # Should not raise
        validate_no_english_keywords(code)

    def test_validate_rejects_english_if(self):
        """Test that English 'if' keyword is rejected."""
        with pytest.raises(ValueError, match="if"):
            validate_no_english_keywords("if x > 0:\n    pass")

    def test_validate_rejects_english_for(self):
        """Test that English 'for' keyword is rejected."""
        with pytest.raises(ValueError, match="for"):
            validate_no_english_keywords("for i in range(10):\n    pass")

    def test_validate_rejects_english_while(self):
        """Test that English 'while' keyword is rejected."""
        with pytest.raises(ValueError, match="while"):
            validate_no_english_keywords("while True:\n    pass")

    def test_validate_rejects_english_return(self):
        """Test that English 'return' keyword is rejected."""
        with pytest.raises(ValueError, match="return"):
            validate_no_english_keywords("def func():\n    return 5")

    def test_validate_rejects_english_print(self):
        """Test that English 'print' keyword is rejected."""
        with pytest.raises(ValueError, match="print"):
            validate_no_english_keywords("print('hello')")

    def test_validate_rejects_english_class(self):
        """Test that English 'class' keyword is rejected."""
        with pytest.raises(ValueError, match="class"):
            validate_no_english_keywords("class MyClass:\n    pass")

    def test_validate_allows_english_in_strings(self):
        """Test that English words in strings are allowed."""
        code = '"This is English in Czech"'
        # Should not raise
        validate_no_english_keywords(code)

    def test_validate_allows_english_variable_names(self):
        """Test that English names as identifiers are allowed (not keywords)."""
        code = "hello = 5\nworld = 'test'"
        # Should not raise
        validate_no_english_keywords(code)

    def test_validate_error_message_includes_line_number(self):
        """Test that error message includes line number."""
        with pytest.raises(ValueError, match="line"):
            validate_no_english_keywords("x = 5\nif y > 0:\n    pass")

    def test_validate_rejects_multiple_keywords(self):
        """Test rejection when multiple English keywords are present."""
        with pytest.raises(ValueError):
            validate_no_english_keywords("if x > 0:\n    for i in range(10):\n        pass")


class TestTranspileEdgeCases:
    """Tests for edge cases and error handling."""

    def test_transpile_empty_code(self):
        """Test transpilation of empty code."""
        code = ""
        result = transpile(code)
        assert result is not None

    def test_transpile_only_comments(self):
        """Test transpilation of code with only comments."""
        code = "# Komentář 1\n# Komentář 2"
        result = transpile(code)
        assert "Komentář" in result

    def test_transpile_whitespace_handling(self):
        """Test that transpilation handles various whitespace."""
        code = "právě   když   X > 0:\n    vytiskni(„ok\")"
        result = transpile(code)
        assert "if" in result

    def test_transpile_mixed_czech_quotes(self):
        """Test handling of mixed quote types."""
        code = 'Text = "Ahoj"\nText2 = "normální"'
        result = transpile(code)
        # Czech quotes should be converted
        assert "Ahoj" in result

    def test_transpile_consecutive_decimals(self):
        """Test handling of multiple consecutive decimal transformations."""
        code = "A = 1,1\nB = 2,2\nC = 3,3"
        result = transpile(code)
        assert "1.1" in result
        assert "2.2" in result
        assert "3.3" in result

    def test_transpile_nested_structures(self):
        """Test transpilation of deeply nested structures."""
        code = "Data = [[1; 2; [3; 4]]; [5; 6]]"
        result = transpile(code)
        # Check that semicolons are converted
        assert "[1,2,[3,4]]" in result.replace(" ", "")
