import pandas as pd

# Diccionario de equivalencias mejorado
columnas_equivalentes = {
    "Document Title": "Titulo",
    "Title": "Titulo",
    "Publication Title": "Titulo",
    "Authors": "Autores",
    "Author Affiliations": "Afiliaciones",
    "Year": "Año",
    "Publication Year": "Año",
    "Source title": "Fuente",
    "Publication Title": "Fuente",
    "Journal": "Fuente",
    "Conference": "Fuente",
    "Volume": "Volumen",
    "Issue": "Número",
    "Pages": "Páginas",
    "Start Page": "Página inicial",
    "End Page": "Página final",
    "Abstract":"Abstract",
    "DOI": "DOI",
    "ISBNs": "ISBN",
    "ISSN": "ISSN",
    "Document Type": "Tipo de Documento",
    "Source": "Fuente",
    "Funding Information": "Financiamiento",
    "PDF Link": "Enlace PDF",
    "Author Keywords": "Palabras clave",
    "IEEE Terms": "Términos",
    "Mesh_Terms": "Términos",
    "Article Citation Count": "Citas",
    "Patent Citation Count": "Citas de Patentes",
    "Reference Count": "Cantidad de Referencias",
    "License": "Licencia",
    "Online Date": "Fecha en Línea",
    "Issue Date": "Fecha de Publicación",
    "Meeting Date": "Fecha de Conferencia",
    "Publisher": "Editorial",
    "Document Identifier": "ID Documento"
}

def cargar_csv(archivo):
    """Carga un archivo CSV y maneja errores."""
    try:
        return pd.read_csv(archivo)
    except Exception as e:
        print(f"Error al cargar {archivo}: {e}")
        return pd.DataFrame()

def normalizar_columnas(df):
    """Renombra columnas usando el diccionario de equivalencias."""
    df = df.rename(columns=lambda x: columnas_equivalentes.get(x, x))
    # Elimina columnas duplicadas (mantiene la primera aparición)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def eliminar_duplicados_por_isbn_o_doi(df):
    """Elimina las filas duplicadas basándose en la columna 'ISBN' o 'DOI'."""
    if 'ISBN' in df.columns:
        df = df.drop_duplicates(subset=['ISBN'], keep='first')
    elif 'DOI' in df.columns:
        df = df.drop_duplicates(subset=['DOI'], keep='first')
    return df

def obtener_menos_columnas(archivos):
    """Encuentra el archivo con menos columnas después de la normalización."""
    dataframes = [normalizar_columnas(eliminar_duplicados_por_isbn_o_doi(cargar_csv(archivo))) for archivo in archivos]
    return min(dataframes, key=lambda df: df.shape[1])

def unificar_archivos_csv(archivos):
    """Unifica los CSV usando las columnas del archivo más pequeño."""
    # Identificar las columnas relevantes
    df_menos_columnas = obtener_menos_columnas(archivos)
    columnas_relevantes = df_menos_columnas.columns

    # Filtra y normaliza las columnas relevantes
    dataframes = [
        normalizar_columnas(eliminar_duplicados_por_isbn_o_doi(cargar_csv(archivo))).reindex(columns=columnas_relevantes, fill_value="")
        for archivo in archivos
    ]

    # Concatenar los DataFrames (ya sin duplicados por ISBN o DOI)
    df_unificado = pd.concat(dataframes, ignore_index=True)

    return df_unificado

def main():
    archivos = [
        "export_sanitized.csv", 
        "export2024.10.15-18.47.42.csv", 
        "unified_acm_data.csv",
        "resultados\scopus.csv"
    ]

    df_unificado = unificar_archivos_csv(archivos)
    df_unificado.to_csv("unified_articles.csv", index=False)
    print("Archivo unificado guardado como 'unified_articles.csv'.")

if __name__ == "__main__":
    main()
