from zmije.main import transpile
import sys

def main():
    
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

    source_file = None
    output_file = None

    args = sys.argv[1:]
    i = 0

    while i < len(args):
        arg = args[i]
        if arg == "-o" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            source_file = arg
            i += 1

    if not source_file:
        print("Chabička se vloudila: Chybí soubor se zdrojovým kódem.")
        sys.exit(1)

    with open(source_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    transpiled_code = transpile(source_code)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transpiled_code)
    
        print(f"Přetlumočený kód byl uložen do {output_file}.")

    else:
        print(transpiled_code)

    


if __name__ == "__main__":
    main()