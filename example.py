# Příklad kódu s českými klíčovými slovy

X = 0
Výraz = True
Počet = None
Cena = 19.99   
Průměr = 3.14   
Zpráva = "Ahoj světe"
Pokyn = "Zadej číslo"

# Seznamy se středníky jako oddělovače
Seznam = [1, 2, 3, 4, 5]
Vnořený_seznam = [[1, 2], [3, 4], [5, 6]]

# Slovníky se složitými hodnotami
Slovník = {"jméno": "Karel", "věk": 30, "město": "Praha"}
Data = {"seznam": [1, 2, 3], "vnorený": {"a": 1, "b": 2}}

# Funkce s více argumenty
print("Hodnoty:", 1, 2, 3, 4)

# Podmínka
if X > 0:
    print("x je kladné číslo")
elif X < 0:
    print("x je záporné číslo")
else:
    print("x je nula")

# Smyčka for se seznamem
for I in [1, 2, 3]:
    print("číslo v seznamu:", I)

# Smyčka while
while X < 5:
    print("x =", X)
    X = X + 1

# Definice třídy
class Zvire:
    def __init__(self, Jméno):
        self.Jméno = Jméno
    
    def zvuk(self):
        pass

# Import
import sys

# Try-except s více argumenty
try:
    Výsledek = 10 / 0
    Matice = [[1, 2], [3, 4]]
except:
    print("Chyba při dělení")
finally:
    print("Konec bloku zkus")

# Return
def sečti(A, B):
    return A + B

# With statement
with open("soubor.txt") as F:
    Obsah = F.read()

# Yield
def generátor():
    yield 1
    yield 2

# Delete
del X

# Raise
raise ValueError("Neplatná hodnota")
