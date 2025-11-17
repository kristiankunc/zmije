# Zmije

For english, see [README_EN.md](README_EN.md).

## Manifest

Myšlenka ryze českého programovacího jazyka není žádným novodobým nápadem. Na žádost knížete Rostislava byli na Velkou Moravu okolo roku 860 přizváni zvěrozvěsti **Konstantin** a **Metoděj**, kteří byli prvními mysliteli v oblasti slovanských informačních technologií. Právě na jejich počest jsou pojmenovány základní stavební kameny moderního programování - **konstanty** a **metody**.

Češi jakožto národ ale na tyto myšlenky postupně zapomněli a raději se za dob národního obrození věnovali velkým písmenům. I přes snahy mocností jako byly Třetí říše nebo Sovětský svaz se český jazyk přežil do dnešních dní. Bohužel ale s velkými ztrátami v oblasti technické terminologie. Tento projekt si klade za cíl tyto ztráty napravit a vytvořit plnohodnotný programovací jazyk, který bude využívat bohatou českou slovní zásobu a její pravidla.

## Příklad

Klasický program ahoj světe v jazyce Zmije vypadá následovně:

```zmije
vytiskni(„Ahoj světe!“)
```

Pro další příklady a podrobnosti o syntaxi se jukněte do souboru [example.zm](example.zm).

## Důležitá pravidla

### Velká písmena

Všechny vlastní jména (názvy proměnných) musí začínat velkým písmenem. Například:

```zmije
Správná_proměnná = 42
```

### Přímá řeč

Pokud chceme jakýkoliv text vypsat či uložit, musíme použít správné úvozovky. V češtině se používají „dolní“ a „horní“ uvozovky, které se liší od anglických "rovných" uvozovek. Například:

```zmije
Textík = „Ahoj světe“
```

### Desetinná čísla

V češtině se jako oddělovač desetinných míst používá čárka místo tečky. Například:

```zmije
Ludolfovo_číslo = 3,14
```

### Oddělovač prvků v seznamech a n-ticích

Pro oddělení prvků v seznamech a n-ticích se používá středník místo čárky. Například:

```zmije
Seznam = [1; 2; 3; 4; 5]
```

### Ostatní překlady

Mnoho klíčových slov a vestavěných funkcí bylo přeloženo do češtiny. Kompletní seznam překladů naleznete v souboru [internal/data.py](internal/data.py).