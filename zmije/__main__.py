from zmije.main import transpiluj
import sys

def hlavni():
    
    if len(sys.argv) == 2 and sys.argv[1] == "--pomoc":
        print("""
Užití: zmije [command] [options]
Příkazy:
    (žádný příkaz)    Spustí tlumočník pro převod kódu
    Argumenty:
        SOUBOR        Cesta k souboru se zdrojovým kódem
    Možnosti:
        -o <soubor>   Uloží výstup do zadaného souboru
              
    --pomoc            Zobrazí tuto nápovědu""")
        
        sys.exit(1)

    SouborZdroje = None
    SouborVystupu = None

    argumenty = sys.argv[1:]
    i = 0

    while i < len(argumenty):
        arg = argumenty[i]
        if arg == "-o" and i + 1 < len(argumenty):
            SouborVystupu = argumenty[i + 1]
            i += 2
        else:
            SouborZdroje = arg
            i += 1

    if not SouborZdroje:
        print("Chabička se vloudila: Chybí soubor se zdrojovým kódem.")
        sys.exit(1)

    with open(SouborZdroje, "r", encoding="utf-8") as f:
        KodZdroje = f.read()

    PrepisujtecKod = transpiluj(KodZdroje)

    if SouborVystupu:
        with open(SouborVystupu, "w", encoding="utf-8") as f:
            f.write(PrepisujtecKod)
    
        print(f"Přetlumočený kód byl uložen do {SouborVystupu}.")

    else:
        print(PrepisujtecKod)



if __name__ == "__main__":
    hlavni()