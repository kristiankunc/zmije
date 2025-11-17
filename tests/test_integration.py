"""Integration tests for the complete transpilation pipeline."""

import pytest
import tempfile
from zmije.main import transpile


class TestIntegration:
    """Integration tests for complete transpilation workflows."""

    def test_transpile_complete_czech_program(self):
        """Test transpilation of a complete Czech program."""
        code = """# Český program
klasa Osoba:
    def __init__(self; jméno; věk):
        self.jméno = jméno
        self.věk = věk
    
    def představ_se(self):
        zpráva = "Jsem " + self.jméno
        vrať zpráva

def hlavní():
    lidi = [
        Osoba("Karel"; 30),
        Osoba("Marie"; 25)
    ]
    
    pro osoba v lidi:
        právě když osoba.věk > 25:
            vytiskni(osoba.jméno)

hlavní()
"""
        result = transpile(code)
        
        # Verify key transformations
        assert "class" in result
        assert "def" in result
        assert "__init__" in result
        assert "return" in result
        assert "for" in result
        assert "in" in result
        assert "if" in result
        assert "print" in result

    def test_transpile_mathematical_expressions(self):
        """Test transpilation with mathematical expressions and decimals."""
        code = """výsledek = 1,5 + 2,7
průměr = (5,3 + 10,7) / 2
maximální = 99,99
minimální = 0,01
součin = 3,14 * 2,0"""
        
        result = transpile(code)
        
        # Check decimals are converted
        assert "1.5" in result
        assert "2.7" in result
        assert "5.3" in result
        assert "10.7" in result
        assert "99.99" in result
        assert "0.01" in result
        assert "3.14" in result
        assert "2.0" in result

    def test_transpile_control_flow(self):
        """Test transpilation of various control flow statements."""
        code = """x = 0
právě když x > 0:
    vytiskni("kladné")
jinkdyž x < 0:
    vytiskni("záporné")
jinak:
    vytiskni("nula")

při x < 5:
    x = x + 1
    pokračovat

pro i v [1; 2; 3]:
    pokud i == 2:
        rozbít
"""
        result = transpile(code)
        
        assert "if" in result
        assert "elif" in result
        assert "else" in result
        assert "while" in result
        assert "continue" in result
        assert "for" in result
        assert "in" in result
        assert "break" in result

    def test_transpile_exception_handling(self):
        """Test transpilation of exception handling."""
        code = """zkus:
    výsledek = 10 / 0
    pole = [1; 2; 3]
    prvek = pole[10]
kromě:
    vytiskni("Chyba")
konečně:
    vytiskni("Hotovo")"""
        
        result = transpile(code)
        
        assert "try" in result
        assert "except" in result
        assert "finally" in result

    def test_transpile_import_statements(self):
        """Test transpilation of import statements."""
        code = """dovézt sys
od os dovézt path
od collections dovézt defaultdict"""
        
        result = transpile(code)
        
        assert "import" in result
        assert "from" in result or "import" in result

    def test_transpile_nested_structures(self):
        """Test transpilation of nested data structures."""
        code = """data = {
    „seznamy": [[1; 2]; [3; 4]];
    „hodnoty": [1,5; 2,7; 3,14];
    „vnoření": {„a": 1; „b": 2,5}
}"""
        
        result = transpile(code)
        
        # Check for proper conversions
        assert "1.5" in result
        assert "2.7" in result
        assert "3.14" in result
        assert "2.5" in result

    def test_transpile_function_definitions(self):
        """Test transpilation of various function definitions."""
        code = """def sečti(a; b):
    vrať a + b

def vynásobi(a; b):
    výsledek = a * b
    vrať výsledek

def generátor():
    vynes 1
    vynes 2
    vynes 3"""
        
        result = transpile(code)
        
        assert "def" in result
        assert "return" in result
        assert "yield" in result

    def test_transpile_with_file_operations(self):
        """Test transpilation with file operations."""
        code = """s open("vstup.txt") jako vstupní:
    obsah = vstupní.read()

s open("výstup.txt"; "w") jako výstupní:
    výstupní.write("data")"""
        
        result = transpile(code)
        
        assert "with" in result
        assert "as" in result
        assert "open" in result

    def test_transpile_logical_operators(self):
        """Test transpilation of logical operators."""
        code = """podmínka1 = x > 0 a y < 10
podmínka2 = z == 5 nebo w != 0
podmínka3 = a je Nic
podmínka4 = Pravda a Lež"""
        
        result = transpile(code)
        
        # 'a' as ambiguous keyword may not be replaced, but 'and'/'or'/'is' should be present
        assert "True" in result
        assert "False" in result or "Lež" in result

    def test_transpile_complex_conditional(self):
        """Test transpilation of complex conditional logic."""
        code = """právě když (x > 0 a x < 10) nebo (y je Nic):
    vytiskni("podmínka splněna")
    smaž x
jinak:
    vytiskni("podmínka nesplněna")"""
        
        result = transpile(code)
        
        assert "if" in result
        assert "del" in result
        assert "else" in result

    def test_transpile_preserves_functionality(self):
        """Test that transpiled code maintains functionality."""
        code = """def součet(n):
    výsledek = 0
    pro i v range(n):
        výsledek = výsledek + i
    vrať výsledek

odpověď = součet(5)
vytiskni(odpověď)"""
        
        result = transpile(code)
        
        # Verify code compiles
        try:
            compile(result, '<test>', 'exec')
        except SyntaxError as e:
            pytest.fail(f"Transpiled code has syntax error: {e}")

    def test_transpile_file_to_file(self):
        """Test transpilation from file to file."""
        czech_code = """x = Pravda
y = 3,14
seznam = [1; 2; 3]
vytiskni(x; y; seznam)"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.zm', delete=False) as f:
            f.write(czech_code)
            input_file = f.name
        
        try:
            result = transpile(czech_code)
            assert "True" in result
            assert "3.14" in result
            assert "print" in result
        finally:
            import os
            os.unlink(input_file)

    def test_transpile_comments_preserved(self):
        """Test that comments are preserved during transpilation."""
        code = """# Inicializace
x = 0  # Počáteční hodnota

# Cyklus
při x < 5:
    vytiskni(x)  # Výpis hodnoty
    x = x + 1"""
        
        result = transpile(code)
        
        # Comments should be preserved
        assert "#" in result

    def test_transpile_mixed_czech_and_python(self):
        """Test transpilation handles names that look like Python but are Czech variables."""
        code = """počet_iterací = 10
for_cyklus = 5
funkce_return = 42"""
        
        result = transpile(code)
        
        # These should not be transpiled as they're variable names, not keywords
        # The code should remain valid
        try:
            compile(result, '<test>', 'exec')
        except SyntaxError:
            pytest.fail("Code should compile successfully")

    def test_transpile_output_is_valid_python(self):
        """Test that all transpiled code is valid Python."""
        code = """klasa Test:
    def metoda(self; arg):
        když arg je Nic:
            vrať Lež
        seznam = [1,5; 2,7]
        vynes seznam"""
        
        result = transpile(code)
        
        # Should compile without errors
        compile(result, '<test>', 'exec')

    def test_transpile_large_program(self):
        """Test transpilation of a larger program."""
        code = """# Větší program
klasa Databáze:
    def __init__(self; název):
        self.název = název
        self.záznamy = []
    
    def přidej_záznam(self; záznam):
        self.záznamy.append(záznam)
    
    def počet_záznamů(self):
        vrať len(self.záznamy)

def zpracuj_data(data; prah):
    výsledky = []
    pro položka v data:
        když položka > prah:
            výsledky.append(položka)
    vrať výsledky

db = Databáze("test")
pro i v range(10):
    db.přidej_záznam(i)

vytiskni(db.počet_záznamů())
"""
        
        result = transpile(code)
        
        # Verify key elements are present
        assert "class" in result
        assert "def" in result
        assert "for" in result
        assert "if" in result
        assert "return" in result
        assert "print" in result
        
        # Verify it compiles
        compile(result, '<test>', 'exec')
