# Thesaurus-verrijking en NER extractie script
# =============================================
# Ondersteunt zowel interactieve terminalinput als command line-opties via argparse.
# Gebruikt SpaCy om namenwoorden en optioneel entiteiten te extraheren uit een opgegeven kolom.
# Onderdrukt korte tokens (<3 tekens), herkent samengestelde jaartallen en eeuwen via regex.
# Domeintermen kunnen handmatig worden aangevuld.
# Logging van verwerkingsproces en gefilterde regels inbegrepen.

import spacy
import pandas as pd
import os
import re
import argparse
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import logging
import time
import subprocess

# Setup SpaCy model
try:
    import importlib.util
    model_name = "nl_core_news_md" if importlib.util.find_spec("nl_core_news_md") else "nl_core_news_sm"
except Exception:
    model_name = "nl_core_news_sm"

try:
    nlp = spacy.load(model_name)
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
    nlp = spacy.load(model_name)

log_filename = f"verwerkingslog_{int(time.time())}.txt"
filterlog_filename = f"gefilterd_{int(time.time())}.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

SAMENSTELLINGEN = [
    ("begin", "jaartelling"),
    ("eerste", "wereldoorlog"),
    ("tweede", "kamer"),
    ("koninklijk", "huis"),
    ("oude", "rijksdaggebouw"),
]

DOMEINTERMEN = {"wierde", "terp", "waterput", "kerkheuvel", "urnenveld", "huisterp", "dorpswierde", "borg"}

def herstel_samenstellingen(nomenlijst):
    woorden = nomenlijst.split("|")
    i = 0
    resultaat = []
    while i < len(woorden):
        if i < len(woorden) - 1 and (woorden[i], woorden[i + 1]) in SAMENSTELLINGEN:
            resultaat.append(f"{woorden[i]} {woorden[i + 1]}")
            i += 2
        else:
            resultaat.append(woorden[i])
            i += 1
    return "|".join(resultaat)

def unieke_bestandsnaam(pad):
    if not os.path.exists(pad): return pad
    base, ext = os.path.splitext(pad)
    for i in range(1, 1000):
        nieuw = f"{base}-{i}{ext}"
        if not os.path.exists(nieuw): return nieuw
    return pad

def vind_romeinse_eeuwen_en_jaartallen(tekst):
    tekst = tekst.lower()
    losse_eeuwen = re.findall(r"\b\d{1,2}e eeuw\b", tekst)
    samengestelde_eeuwen = re.findall(r"\b\d{1,2}e\s*[-–]\s*\d{1,2}e eeuw\b", tekst)
    jaartallen = re.findall(r"\b\d{3,4}(?:\s*[-–]\s*\d{3,4})?\b", tekst)
    return losse_eeuwen + samengestelde_eeuwen + jaartallen

def select_input_file():
    root = tk.Tk(); root.withdraw()
    return filedialog.askopenfilename(title="Selecteer bestand", filetypes=[("CSV/Excel", "*.csv *.tsv *.xlsx")])

def main():
    parser = argparse.ArgumentParser(description="NER extractie en thesaurusverrijking")
    parser.add_argument('--file', help='Pad naar invoerbestand (anders opent dialoog)')
    parser.add_argument('--kolom', type=int, help='Index van te analyseren kolom')
    parser.add_argument('--output', default='ner_resultaat', help='Naam van outputkolom')
    parser.add_argument('--entiteiten', action='store_true', help='Voeg SpaCy entiteiten toe')
    parser.add_argument('--kleine_letters', action='store_true', help='Zet tekst om naar kleine letters')
    parser.add_argument('--sorteer', action='store_true', help='Sorteer resultaten alfabetisch')
    parser.add_argument('--csv', action='store_true', help='Forceer output naar CSV (anders: Excel indien .xlsx)')
    args = parser.parse_args()

    input_file = args.file or select_input_file()
    if not input_file:
        print("Geen bestand geselecteerd."); return
    ext = os.path.splitext(input_file)[1].lower()
    sep = ','

    if ext in [".csv", ".tsv"]:
        sep = input("Wat is het scheidingsteken tussen de kolommen? (bijv. ',' of ';' of '|' of '\t')\nLaat leeg voor ',': ").strip() or ','
        df = pd.read_csv(input_file, encoding="utf-8", sep=sep, on_bad_lines='skip')
    elif ext == ".xlsx":
        df = pd.read_excel(input_file, engine="openpyxl")
    else:
        print("Bestandstype niet ondersteund."); return

    print("\nKolommen in uw bestand:")
    for i, col in enumerate(df.columns): print(f"[{i}] {col}")
    print(df.head(2).to_string(index=False))

    if args.kolom is not None:
        column_name = df.columns[args.kolom]
    else:
        try:
            col_index = int(input("\nKies het nummer van de kolom die u wilt analyseren:\n(typ alleen het cijfer en druk op Enter): ").strip())
            column_name = df.columns[col_index]
        except:
            print("Ongeldige kolomkeuze. Script wordt gestopt."); return

    output_column = args.output
    include_entities = args.entiteiten or input("Wilt u ook entiteiten zoals plaatsnamen en objecten meenemen? (ja/nee) [Enter=ja]: ").strip().lower() != "nee"
    lowercase = args.kleine_letters or input("Wilt u de termen omzetten naar kleine letters? (ja/nee) [Enter=ja]: ").strip().lower() != "nee"
    sort_output = args.sorteer or input("Wilt u de termen alfabetisch sorteren? (ja/nee) [Enter=ja]: ").strip().lower() != "nee"

    start_time = time.time()
    print("\nVerwerken gestart...")

    texts = df[column_name].astype(str)
    if lowercase:
        texts = texts.str.lower()
    texts = texts.str.replace(r'["“”.,;:!?]', '', regex=True).str.strip().str.replace(r'\s+', ' ', regex=True).tolist()

    results = []
    gefilterde_regels = []
    for doc, raw_text in zip(tqdm(nlp.pipe(texts, batch_size=50), total=len(texts)), texts):
        try:
            terms = [t.text.lower().strip() for t in doc if t.pos_ in {"NOUN", "PROPN"}]
            if include_entities:
                terms += [e.text.lower().strip() for e in doc.ents if e.label_ in {"LOC", "GPE", "ORG", "MISC"}]
            terms += vind_romeinse_eeuwen_en_jaartallen(raw_text)
            for term in DOMEINTERMEN:
                if term in raw_text.lower():
                    terms.append(term)
            terms = [t for t in terms if len(t.strip()) > 2 and not re.fullmatch(r"\d{1,2}|\w{1,2}", t)]
            terms = list(dict.fromkeys(terms))
            if sort_output:
                terms = sorted(terms)
            resultaat = herstel_samenstellingen("|".join(terms))
            if not resultaat:
                gefilterde_regels.append(raw_text)
            results.append(resultaat)
        except Exception as e:
            logging.error(f"Fout bij tekst: {raw_text[:30]}... - {e}")
            results.append("")

    df[output_column] = results

    output_ext = ".csv" if args.csv or ext in [".csv", ".tsv"] else ".xlsx"
    output_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = unieke_bestandsnaam(os.path.join(os.path.dirname(input_file), f"{output_name}_output{output_ext}"))

    try:
        if output_ext == ".xlsx":
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, encoding="utf-8", index=False, sep=sep or ',')
        print(f"\nBestand opgeslagen als: {output_file}")
    except Exception as e:
        print(f"Fout bij opslaan: {e}")
        logging.error(f"Opslaan mislukt: {e}")

    if gefilterde_regels:
        with open(filterlog_filename, "w", encoding="utf-8") as flog:
            for lijn in gefilterde_regels:
                flog.write(lijn + "\n")
        print(f"\nGefilterde regels opgeslagen in: {filterlog_filename}")

    print(f"\n--- Verwerking voltooid ---\nRijen: {len(df)}\nDuur: {round(time.time() - start_time, 1)} s\nLog: {log_filename}")

if __name__ == "__main__":
    main()
