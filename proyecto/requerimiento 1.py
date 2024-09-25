import rispy
import pandas as pd
from collections import Counter
import re

# Definir las rutas de los archivos RIS
archivos_ris = [
    'IEEE Xplore Citation RIS Download 2024.8.12.9.26.10.ris',
    'ScienceDirect_citations_1723472751920.ris',
    'scopus.ris',
    'tandf_citations.ris'
]

entradas = []
for archivo in archivos_ris:
    with open(archivo, 'r', encoding='utf-8') as f:
        entradas_cargadas = rispy.load(f)
        for entrada in entradas_cargadas:
            entrada['base_de_datos'] = archivo  # Agregar el archivo RIS como fuente
        entradas.extend(entradas_cargadas)

# Crear DataFrame con los datos
df = pd.DataFrame(entradas)

# Eliminar duplicados usando 'doi' como identificador único
df.drop_duplicates(subset=['doi'], inplace=True)

df.to_csv('datos_unificados.csv', index=False)
print("Datos unificados y guardados en 'datos_unificados.csv'.")

#----------------------------------------------------------------
# Estadísticas por primer autor 
df['primer_autor'] = df['authors'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'Desconocido')
estadisticas_primer_autor = df['primer_autor'].value_counts()
estadisticas_primer_autor.to_csv('estadisticas_primer_autor.csv')

# Estadísticas por año
estadisticas_anio = df['year'].value_counts()
estadisticas_anio.to_csv('estadisticas_anio.csv')

# Estadísticas por tipo de producto
estadisticas_tipo_producto = df['type_of_reference'].value_counts()
estadisticas_tipo_producto.to_csv('estadisticas_tipo_producto.csv')

# Estadísticas por journal (si aplica)
if 'journal_name' in df.columns:
    estadisticas_journal = df['journal_name'].value_counts()
    estadisticas_journal.to_csv('estadisticas_journal.csv')

# Estadísticas por editor
if 'publisher' in df.columns:
    estadisticas_editor = df['publisher'].value_counts()
    estadisticas_editor.to_csv('estadisticas_editor.csv')

# Estadísticas por base de datos (nombre del archivo RIS)
estadisticas_base_datos = df['base_de_datos'].value_counts()
estadisticas_base_datos.to_csv('estadisticas_base_datos.csv')

# Estadísticas por citaciones (si existen citaciones)
if 'citations' in df.columns:
    estadisticas_citaciones = df['citations'].value_counts()
    estadisticas_citaciones.to_csv('estadisticas_citaciones.csv')

print("Estadísticas generadas y guardadas en archivos CSV.")

#----------------------------------------------------------------
# Sinónimos (usamos un diccionario donde las claves son las palabras clave y los valores son las unificaciones)
sinonimos = {
    'Abstraction': 'Abstracción',
    'Algorithm': 'Algoritmo',
    'Algorithmic thinking': 'Pensamiento Algorítmico',
    'Coding': 'Codificación',
    'Collaboration': 'Colaboración',
    'Cooperation': 'Colaboración',
    'Creativity': 'Creatividad',
    'Critical thinking': 'Pensamiento Crítico',
    'Debug': 'Depuración',
    'Decomposition': 'Descomposición',
    'Evaluation': 'Evaluación',
    'Generalization': 'Generalización',
    'Logic': 'Lógica',
    'Logical thinking': 'Lógica',
    'Modularity': 'Modularidad',
    'Patterns recognition': 'Reconocimiento de Patrones',
    'Problem solving': 'Resolución de Problemas',
    'Programming': 'Programación',
    'Representation': 'Representación',
    'Reuse': 'Reutilización',
    'Simulation': 'Simulación'
}

# Consolidar todas las descripciones/resúmenes en una sola cadena de texto
todos_resumenes = ' '.join(df['abstract'].dropna())

todos_resumenes = todos_resumenes.lower()

# Contar la frecuencia de aparición de cada variable
frecuencia_palabras = Counter()

for palabra, palabra_unificada in sinonimos.items():
    conteo_palabra = len(re.findall(palabra.lower(), todos_resumenes))
    frecuencia_palabras[palabra_unificada] += conteo_palabra

# Guardar los resultados en un archivo CSV
frecuencia_palabras_df = pd.DataFrame(list(frecuencia_palabras.items()), columns=['Variable', 'Frecuencia'])
frecuencia_palabras_df.to_csv('frecuencia_palabras.csv', index=False)
print("Frecuencia de aparición de palabras clave generada y guardada en 'frecuencia_palabras.csv'.")
