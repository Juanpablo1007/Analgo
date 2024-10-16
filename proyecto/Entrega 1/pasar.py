import bibtexparser
import pandas as pd

# Leer el archivo unificado .bib
with open("unified_acm.bib", encoding='utf-8') as bibtex_file:
    bib_data = bibtexparser.load(bibtex_file)

# Extraer los campos relevantes
records = []
for entry in bib_data.entries:
    title = entry.get('title', '')
    author = entry.get('author', '')
    year = entry.get('year', '')
    isbn = entry.get('isbn', '')
    publisher = entry.get('publisher', '')
    address = entry.get('address', '')
    url = entry.get('url', '')
    doi = entry.get('doi', '')
    abstract = entry.get('abstract', '')

    records.append({
        "Authors": author,
        "Title": title,
        "Year": year,
        "ISBN": isbn,
        "Publisher": publisher,
        "Address": address,
        "URL": url,
        "DOI": doi,
        "Abstract": abstract
    })

# Crear un DataFrame
df = pd.DataFrame(records)

# Guardar como archivo CSV
df.to_csv("unified_acm_data.csv", index=False)
print("Archivo CSV generado exitosamente: unified_acm_data.csv")
