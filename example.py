# Příklad kódu s českými klíčovými slovy

x = 0
výraz = True
počet = None
cena = 19.99   
průměr = 3.14   
zpráva = "Ahoj světe"
pokyn = "Zadej číslo"

# Seznamy se středníky jako oddělovače
seznam = [1, 2, 3, 4, 5]
vnořený_seznam = [[1, 2], [3, 4], [5, 6]]

# Slovníky se složitými hodnotami
slovník = {"jméno": "Karel", "věk": 30, "město": "Praha"}
data = {"seznam": [1, 2, 3], "vnorený": {"a": 1, "b": 2}}

# Funkce s více argumenty
print("Hodnoty:", 1, 2, 3, 4)

# Podmínka
if      x > 0:
    print("x je kladné číslo")
elif x < 0:
    print("x je záporné číslo")
else:
    print("x je nula")

# Smyčka for se seznamem
for i in [1, 2, 3]:
    print("číslo v seznamu:", i)

# Smyčka while
while x < 5:
    print("x =", x)
    x = x + 1

# Definice třídy
class Zvire:
    def __init__(self, jméno):
        self.jméno = jméno
    
    def zvuk(self):
        pass

# Import
import sys

# Try-except s více argumenty
try:
    výsledek = 10 / 0
    matice = [[1, 2], [3, 4]]
except:
    print("Chyba při dělení")
finally:
    print("Konec bloku zkus")

# Return
def sečti(a, b):
    return a + b

# With statement
with open("soubor.txt") as f:
    obsah = f.read()

# Yield
def generátor():
    yield 1
    yield 2

# Delete
del x

# Raise
raise ValueError("Neplatná hodnota")
