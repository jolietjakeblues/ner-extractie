# ner-extractie

**Beschrijving (Nederlands)**

Dit project bevat een Python-script (`ner_extract_terms_spacy.py`) voor het automatisch extraheren van betekenisvolle termen uit Nederlandstalige tekstbestanden, zoals beschrijvingen van erfgoedobjecten. Het script gebruikt:

* SpaCy voor taalanalyse (Nederlands model)
* Regex voor herkenning van jaartallen en eeuwen
* Handmatige thesaurusverrijking (domeintermen)
* Optionele filtering en normalisatie

Het resultaat is een extra kolom met termen die geschikt zijn voor analyse, matching of verdere verrijking.

**Gebruik**

U kunt het script draaien via de terminal met interactieve prompts, of met commando-opties zoals hieronder:

```bash
python ner_extract_terms_spacy.py --file mijndata.csv --kolom 3 --output ner_terms \
  --entiteiten --kleine_letters --sorteer --csv
```

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

**Licentie**

Iedereen mag dit script gebruiken, kopiëren, wijzigen en verspreiden. Geen rechten voorbehouden.

> UNLICENSE (2025) Joop Vanderheiden / jolietjakeblues

---

**Description (English)**

This repository contains `ner_extract_terms_spacy.py`, a script to extract meaningful terms from Dutch text (e.g. heritage descriptions) using:

* SpaCy (Dutch model)
* Regex for centuries and date ranges
* Manual thesaurus enrichment
* Filtering of short/unwanted tokens

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

**License**

This code is released into the public domain.

> UNLICENSE (2025) Joop Vanderheiden / jolietjakeblues
