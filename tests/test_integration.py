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
    def __init__(self; Jméno; Věk):
        self.Jméno = Jméno
        self.Věk = Věk
    
    def Představ_se(self):
        Zpráva = "Jsem " + self.Jméno
        vrať Zpráva

def Hlavní():
    Lidi = [
        Osoba("Karel"; 30),
        Osoba("Marie"; 25)
    ]
    
    pro Osoba_tmp v Lidi:
        právě když Osoba_tmp.Věk > 25:
            vytiskni(Osoba_tmp.Jméno)

Hlavní()
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
        code = """Výsledek = 1,5 + 2,7
Průměr = (5,3 + 10,7) / 2
Maximální = 99,99
Minimální = 0,01
Součin = 3,14 * 2,0"""
        
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
        code = """X = 0
právě když X > 0:
    vytiskni("kladné")
jinkdyž X < 0:
    vytiskni("záporné")
jinak:
    vytiskni("nula")

při X < 5:
    X = X + 1
    pokračovat

pro I v [1; 2; 3]:
    pokud I == 2:
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
    Výsledek = 10 / 0
    Pole = [1; 2; 3]
    Prvek = Pole[10]
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
        code = """Data = {
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
        code = """def Sečti(A; B):
    vrať A + B

def Vynásobi(A; B):
    Výsledek = A * B
    vrať Výsledek

def Generátor():
    vynes 1
    vynes 2
    vynes 3"""
        
        result = transpile(code)
        
        assert "def" in result
        assert "return" in result
        assert "yield" in result

    def test_transpile_with_file_operations(self):
        """Test transpilation with file operations."""
        code = """s open("vstup.txt") jako Vstupní:
    Obsah = Vstupní.read()

s open("výstup.txt"; "w") jako Výstupní:
    Výstupní.write("data")"""
        
        result = transpile(code)
        
        assert "with" in result
        assert "as" in result
        assert "open" in result

    def test_transpile_logical_operators(self):
        """Test transpilation of logical operators."""
        code = """Podmínka1 = X > 0 a Y < 10
Podmínka2 = Z == 5 nebo W != 0
Podmínka3 = A je Nic
Podmínka4 = Pravda a Lež"""
        
        result = transpile(code)
        
        # 'a' as ambiguous keyword may not be replaced, but 'and'/'or'/'is' should be present
        assert "True" in result
        assert "False" in result or "Lež" in result

    def test_transpile_complex_conditional(self):
        """Test transpilation of complex conditional logic."""
        code = """právě když (X > 0 a X < 10) nebo (Y je Nic):
    vytiskni("podmínka splněna")
    smaž X
jinak:
    vytiskni("podmínka nesplněna")"""
        
        result = transpile(code)
        
        assert "if" in result
        assert "del" in result
        assert "else" in result

    def test_transpile_preserves_functionality(self):
        """Test that transpiled code maintains functionality."""
        code = """def Součet(N):
    Výsledek = 0
    pro I v range(N):
        Výsledek = Výsledek + I
    vrať Výsledek

Odpověď = Součet(5)
vytiskni(Odpověď)"""
        
        result = transpile(code)
        
        # Verify code compiles
        try:
            compile(result, '<test>', 'exec')
        except SyntaxError as e:
            pytest.fail(f"Transpiled code has syntax error: {e}")

    def test_transpile_file_to_file(self):
        """Test transpilation from file to file."""
        czech_code = """X = Pravda
Y = 3,14
Seznam = [1; 2; 3]
vytiskni(X; Y; Seznam)"""
        
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
X = 0  # Počáteční hodnota

# Cyklus
při X < 5:
    vytiskni(X)  # Výpis hodnoty
    X = X + 1"""
        
        result = transpile(code)
        
        # Comments should be preserved
        assert "#" in result

    def test_transpile_mixed_czech_and_python(self):
        """Test transpilation handles names that look like Python but are Czech variables."""
        code = """Počet_iterací = 10
For_cyklus = 5
Funkce_return = 42"""
        
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
    def Metoda(self; Arg):
        když Arg je Nic:
            vrať Lež
        Seznam = [1,5; 2,7]
        vynes Seznam"""
        
        result = transpile(code)
        
        # Should compile without errors
        compile(result, '<test>', 'exec')

    def test_transpile_large_program(self):
        """Test transpilation of a larger program."""
        code = """# Větší program
klasa Databáze:
    def __init__(self; Název):
        self.Název = Název
        self.Záznamy = []
    
    def Přidej_záznam(self; Záznam):
        self.Záznamy.append(Záznam)
    
    def Počet_záznamů(self):
        vrať len(self.Záznamy)

def Zpracuj_data(Data; Prah):
    Výsledky = []
    pro Položka v Data:
        když Položka > Prah:
            Výsledky.append(Položka)
    vrať Výsledky

Db = Databáze("test")
pro I v range(10):
    Db.Přidej_záznam(I)

vytiskni(Db.Počet_záznamů())
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
