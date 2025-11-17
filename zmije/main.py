import io
import tokenize
import keyword

from zmije.internal.data import KEYWORD_MAP

NEJEDNOZNACNA_KLICOVA_SLOVA = {("a",)}

def prepis_tokeny(tokeny):
    vyrovnavaci_pamet = []
    vystup = []
    hloubka_zavorek = 0
    po_def = False
    v_def_zavorkach = False
    po_tecce = False

    for tok in tokeny:
        if tok.type == tokenize.NAME and tok.string == "def":
            po_def = True
            v_def_zavorkach = False
        
        if tok.type == tokenize.OP:
            if tok.string == "(":
                if po_def:
                    v_def_zavorkach = True
                hloubka_zavorek += 1
            elif tok.string == ")":
                hloubka_zavorek -= 1
                if hloubka_zavorek == 0 and po_def:
                    v_def_zavorkach = False
                    po_def = False
            elif tok.string == ".":
                po_tecce = True
            elif tok.string not in (",", " "):
                po_tecce = False
        
        if tok.type == tokenize.NAME:
            vyrovnavaci_pamet.append(tok)
            
            mel_nahradit = True
            
            if v_def_zavorkach:
                mel_nahradit = False
            
            if po_tecce:
                mel_nahradit = False
                po_tecce = False
            
            if mel_nahradit:
                for klicove_slovo in NEJEDNOZNACNA_KLICOVA_SLOVA:
                    if len(vyrovnavaci_pamet) >= len(klicove_slovo) and [t.string.lower() for t in vyrovnavaci_pamet[-len(klicove_slovo):]] == [k.lower() for k in klicove_slovo]:
                        mel_nahradit = False
                        break
            
            if mel_nahradit:
                for sekvence in sorted(KEYWORD_MAP.keys(), key=len, reverse=True):
                    if len(vyrovnavaci_pamet) >= len(sekvence):
                        okno = vyrovnavaci_pamet[-len(sekvence):]
                        if [t.string.lower() for t in okno] == [k.lower() for k in sekvence]:
                            nahrady = KEYWORD_MAP[sekvence]
                            novy = okno[0]._replace(string=nahrady)
                            vyrovnavaci_pamet = vyrovnavaci_pamet[:-len(sekvence)] + [novy]
                            break
            continue

        while vyrovnavaci_pamet:
            vystup.append(vyrovnavaci_pamet.pop(0))
        vystup.append(tok)

    while vyrovnavaci_pamet:
        vystup.append(vyrovnavaci_pamet.pop(0))
    
    return vystup

def nahrad_oddelovac_desetinnych(tokeny):
    vystup = []
    i = 0
    while i < len(tokeny):
        tok = tokeny[i]
        
        if tok.type == tokenize.NUMBER and i + 2 < len(tokeny):
            dalsi_tok = tokeny[i + 1]
            dalsi_dalsi_tok = tokeny[i + 2]
            
            if (dalsi_tok.type == tokenize.OP and dalsi_tok.string == "," and
                dalsi_dalsi_tok.type == tokenize.NUMBER):
                
                kombinovany_retezec = tok.string + "." + dalsi_dalsi_tok.string
                novy_tok = tok._replace(string=kombinovany_retezec)
                vystup.append(novy_tok)
                i += 3
                continue
        
        vystup.append(tok)
        i += 1
    
    return vystup

def nahrad_oddelovace_seznamu(tokeny):
    vystup = []
    for tok in tokeny:
        if tok.type == tokenize.OP and tok.string == ";":
            novy_tok = tok._replace(string=",")
            vystup.append(novy_tok)
        else:
            vystup.append(tok)
    
    return vystup

def validuj_promenne_velkymi_pismeny(kod):
    python_klicova_slova = set(keyword.kwlist)
    
    ceska_klicova_slova = set()
    for klic in KEYWORD_MAP.keys():
        if isinstance(klic, tuple):
            ceska_klicova_slova.add(klic[0])
        else:
            ceska_klicova_slova.add(klic)
    
    vstavene_nazvy = set(dir(__builtins__) if isinstance(__builtins__, dict) else dir(__builtins__))
    
    kod_normalizovany = kod.replace('„', '"').replace('‟', '"')
    kod_normalizovany = kod_normalizovany.strip()
    
    try:
        tokeny = list(tokenize.generate_tokens(io.StringIO(kod_normalizovany).readline))
    except tokenize.TokenError as e:
        raise ValueError(f"Neplatný kód: {e}")
    
    i = 0
    while i < len(tokeny) - 1:
        tok = tokeny[i]
        dalsi_tok = tokeny[i + 1]
        
        if (tok.type == tokenize.NUMBER and dalsi_tok.type == tokenize.NAME and
            dalsi_tok.string.lower() not in ceska_klicova_slova and
            dalsi_tok.string not in python_klicova_slova):
            raise ValueError(
                f"Neplatný kód: nelze mít číselný literál bezprostředně následovaný jiným názvem proměnné "
                f"na řádku {dalsi_tok.start[0]}, sloupci {dalsi_tok.start[1]}"
            )
        
        i += 1
    
    i = 0
    while i < len(tokeny):
        tok = tokeny[i]
        
        if (tok.type == tokenize.NAME and 
            i + 1 < len(tokeny) and 
            tokeny[i + 1].type == tokenize.OP and 
            tokeny[i + 1].string == "="):
            
            je_atribut = False
            if i > 0 and tokeny[i - 1].type == tokenize.OP and tokeny[i - 1].string == ".":
                je_atribut = True
            
            if je_atribut:
                i += 1
                continue
            
            nazev_promenne = tok.string
            if (nazev_promenne not in python_klicova_slova and
                nazev_promenne not in ceska_klicova_slova and
                nazev_promenne not in vstavene_nazvy and
                nazev_promenne and
                not nazev_promenne[0].isupper()):
                raise ValueError(
                    f"Proměnná '{nazev_promenne}' musí začínat velkým písmenem na řádku {tok.start[0]}, sloupci {tok.start[1]}"
                )
        
        i += 1

def validuj_zadna_anglicka_klicova_slova(kod):
    anglicka_klicova_slova = set(value for value in KEYWORD_MAP.values())
    
    kod_normalizovany = kod.replace('„', '"').replace('‟', '"')
    tokeny = list(tokenize.generate_tokens(io.StringIO(kod_normalizovany).readline))
    
    for tok in tokeny:
        if tok.type == tokenize.NAME and tok.string in anglicka_klicova_slova:
            raise ValueError(
                f"Nalezeno anglické klíčové slovo '{tok.string}' na řádku {tok.start[0]}, sloupci {tok.start[1]}. "
                f"Toto klíčové slovo má český překlad. Použijte českou verzi. "
                f"Zdrojový kód by měl být psán vždy v češtině vole."
            )

def transpiluj(kod):
    try:
        validuj_promenne_velkymi_pismeny(kod)
        
        validuj_zadna_anglicka_klicova_slova(kod)
        
        kod_normalizovany = kod.replace('„', '"').replace('‟', '"')
        
        tokeny = list(tokenize.generate_tokens(io.StringIO(kod_normalizovany).readline))
        
        prepisane = prepis_tokeny(tokeny)
        prepisane = nahrad_oddelovac_desetinnych(prepisane)
        prepisane = nahrad_oddelovace_seznamu(prepisane)
        
        vysledek = tokenize.untokenize(prepisane)
        
        try:
            compile(vysledek, '<transpiluj>', 'exec')
        except SyntaxError as e:
            print(f"Varování: Transpiliovaný kód může obsahovat chyby v syntaxi: {e}")
            print(f"Řádek {e.lineno}: {e.text}")
        
        return vysledek
    
    except ValueError as e:
        raise
    except tokenize.TokenError as e:
        print(f"Chyba: Selhalo tokenizování kódu: {e}")
        raise
    except Exception as e:
        print(f"Chyba při tlumočení: {e}")
        raise

if __name__ == "__main__":
    with open("example.zm", "r", encoding="utf-8") as f:
        zdrojovy_kod = f.read()

    transpiliovany_kod = transpiluj(zdrojovy_kod)
    with open("example.py", "w", encoding="utf-8") as f:
        f.write(transpiliovany_kod)
