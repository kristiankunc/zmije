# Příklad kódu s českými klíčovými slovy

x = 0
výraz = True
počet = None
cena = 19.99   
průměr = 3.14   
zpráva = "Ahoj světe"
pokyn = "Zadej číslo"

# podmínka
if      x > 0:
    print("x je kladné číslo")
elif x < 0:
    print("x je záporné číslo")
else:
    print("x je nula")

# smyčka for
for i in [1.2   , 3]:
    print("číslo v seznamu:", i)

# smyčka while
while x < 5:
    print("x =", x)
    x = x + 1

# definice třídy
class Zvire:
    def __init__(self, jméno):
        self.jméno = jméno
    
    def zvuk(self):
        pass

# import
import sys

# try-except
try:
    výsledek = 10 / 0
except:
    print("Chyba při dělení")
finally:
    print("Konec bloku zkus")

# return
def sečti(a, b):
    return a + b

# with statement
with open("soubor.txt") as f:
    obsah = f.read()

# yield
def generátor():
    yield 1
    yield 2

# delete
del x

# raise
raise ValueError("Neplatná hodnota")
