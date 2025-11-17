# Zmije

For english, see [README_EN.md](README_EN.md).

## Manifest

Myšlenka ryze českého programovacího jazyka není žádným novodobým nápadem. Na žádost knížete Rostislava, byli na Velkou Moravu okolo roku 86é přizváni zvěrozvěsti **Konstantin** a **Metoděj**, kteří byli prvními mysliteli v oblasti slovanských informačních technologií. Právě na jejich počest jsou pojmenovány základní stavební kameny moderního programování - **konstanty** a **metody**.

Češi jakožto národ ale na tyto myšlenky postupně pozapomněl a raději se za dob národního obrození věnovali velkým písmenům. I přes snahy mocností jako byla Drittes Reich nebo Sovětský svaz, přežil šeský jazyk do dnešních dní. Bohužel ale s velkými ztrátami v oblasti technické terminologie. Tento projekt si klade za cíl tyto ztráty napravit a vytvořit plnohodnotný programovací jazyk, který bude využívat bohatou českou slovní zásobu a její pravidla.

## Příklad

Klasický program ahoj světe v jazyce Zmije vypadá následovně:

```zmije
vytiskni(„Ahoj světe!“)
```

Pro další příklady a podrobnosti o syntaxi se jukněte do souboru [example.zm](example.zm).

## Důležitá pravidla

### Přímá řeč

Pokud chceme jakýkoliv text vypsat či uložit, musíme použít správné úvozovky. V češtině se používají „dolní“ a „horní“ uvozovky, které se liší od anglických "rovných" uvozovek. Například:

```zmije
textík = „Ahoj světe“
```

### Desetinná čísla

```zmije
ludolfovo_číslo = 3,14
```

V češtině se jako oddělovač desetinných míst používá čárka místo tečky. Například:

```zmije
ludolfovo_číslo = 3,14
```

### Oddělovač prvků v seznamech a n-ticích

Pro oddělení prvků v seznamech a n-ticích se používá středník místo čárky. Například:

```zmije
seznam = [1; 2; 3; 4; 5]
```

### Ostatní překlady

Mnoho klíčových slov a vestavěných funkcí bylo přeloženo do češtiny. Kompletní seznam překladů naleznete v souboru [internal/data.py](internal/data.py).