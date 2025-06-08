# ner-extractie

![Python version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License: Unlicense](https://img.shields.io/badge/license-Unlicense-lightgrey)

**Beschrijving (Nederlands)**

Dit project bevat een Python-script (`ner_extract_terms_spacy.py`) voor het automatisch extraheren van betekenisvolle termen uit Nederlandstalige tekstbestanden, zoals beschrijvingen van erfgoedobjecten. Het script gebruikt:

* SpaCy voor taalanalyse (Nederlands model)
* Regex voor herkenning van jaartallen en eeuwen
* Handmatige thesaurusverrijking (domeintermen)
* Optionele filtering en normalisatie

Het resultaat is een extra kolom met termen die geschikt zijn voor analyse, matching of verdere verrijking.

**Installatie**

1. Zorg dat Python 3.10 of hoger is geïnstalleerd.
2. Installeer de vereiste pakketten:

```bash
pip install -r requirements.txt
```

Of handmatig:

```bash
pip install spacy pandas openpyxl tqdm
python -m spacy download nl_core_news_md
```

**Gebruik**

U kunt het script draaien via de terminal met interactieve prompts, of met commando-opties zoals hieronder:

```bash
python ner_extract_terms_spacy.py --file mijndata.csv --kolom 3 --output ner_terms \
  --entiteiten --kleine_letters --sorteer --csv
```
**Let op (Windows gebruikers)**

- Voer de volledige opdracht **op één regel** uit, zonder `\`.
- Gebruik geen extra argumenten zoals `--profile`, tenzij ondersteund door het script.
- Voorbeeld (werkt altijd):

```bash
python ner_extract_terms_spacy.py --file mijndata.csv --kolom 3 --output ner_terms --entiteiten --kleine_letters --sorteer --csv

**Argumenten**

* `--file` pad naar CSV of Excel-bestand
* `--kolom` index van kolom met tekst (beginnend bij 0)
* `--output` naam voor nieuwe kolom met output
* `--entiteiten` voegt SpaCy entiteiten toe (LOC, ORG, GPE, etc.)
* `--kleine_letters` zet alles om naar kleine letters
* `--sorteer` sorteert resultaat alfabetisch
* `--csv` slaat output op als CSV (standaard: Excel bij .xlsx input)

De resultaten worden opgeslagen in een nieuw bestand in dezelfde map. Bestandsnamen worden automatisch voorzien van volgnummer bij dubbele naam.

Gefilterde rijen (waarbij alles werd verwijderd) worden gelogd in een apart .txt-bestand.

**Voorbeeldbestand**

U kunt starten met `example.csv`, een voorbeeldbestand dat drie eenvoudige beschrijvingen bevat.

**Screenshot terminaloutput**

```
Kolommen in uw bestand:
[0] rijksmonument
[1] nummer
[2] omschrijving

Kies het nummer van de kolom die u wilt analyseren:
(typ alleen het cijfer en druk op Enter): 2
Hoe moet de nieuwe kolom met resultaten heten? [druk op Enter]: ner_terms
Wilt u ook entiteiten meenemen? [Enter=ja]:
Wilt u omzetten naar kleine letters? [Enter=ja]:
Wilt u sorteren? [Enter=ja]:
Verwerken gestart...
Rijen: 3
Duur: 0.5 s
Logbestand: verwerkingslog_...txt
```

**Bekende beperkingen**

* Alleen getest met Nederlandstalige teksten
* Werkt het best met goed gestructureerde zinnen
* Geen automatische semantische disambiguatie

**Toekomstige uitbreidingen (TODO)**

* Koppeling met een externe thesaurus via SPARQL/API
* Ondersteuning voor synoniemenlijsten
* Output als RDF of JSON-LD
* Meerdere kolommen tegelijk verwerken

**Licentie**

Iedereen mag dit script gebruiken, kopiëren, wijzigen en verspreiden. Geen rechten voorbehouden.

> UNLICENSE (2025) Joop Vanderheiden / jolietjakeblues

---

**Description (English)**

![Python version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License: Unlicense](https://img.shields.io/badge/license-Unlicense-lightgrey)

This repository contains `ner_extract_terms_spacy.py`, a script to extract meaningful terms from Dutch text (e.g. heritage descriptions) using:

* SpaCy (Dutch model)
* Regex for centuries and date ranges
* Manual thesaurus enrichment
* Filtering of short/unwanted tokens

**Installation**

Make sure you have Python 3.10+ installed. Then install the dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install spacy pandas openpyxl tqdm
python -m spacy download nl_core_news_md
```

**Usage**
Run interactively or with CLI options like:

```bash
python ner_extract_terms_spacy.py --file mydata.csv --kolom 3 --output ner_terms \
  --entiteiten --kleine_letters --sorteer --csv
```

**Options**

* `--file` path to input file (.csv or .xlsx)
* `--kolom` column index (starting at 0)
* `--output` output column name
* `--entiteiten` include SpaCy named entities
* `--kleine_letters` normalize to lowercase
* `--sorteer` sort terms alphabetically
* `--csv` force CSV output (default: Excel for .xlsx input)

Filtered-out rows are logged separately. Output is saved with a unique filename.

**Sample data**
See `example.csv` for a 3-row test file.

**Terminal screenshot**

```
Processing started...
Extracting from column: omschrijving
Output column: ner_terms
Saved as: example_output.csv
Filtered rows logged.
```

**Known limitations**

* Designed for Dutch-language texts only
* Relies on well-formed input sentences
* No semantic disambiguation

**Future ideas (TODO)**

* SPARQL/API integration with external thesauri
* Synonym support
* Export as RDF or JSON-LD
* Multi-column processing

**License**

This code is released into the public domain.

> UNLICENSE (2025) Joop Vanderheiden / jolietjakeblues
