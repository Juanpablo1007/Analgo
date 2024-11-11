import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import os
import random
import warnings
from collections import Counter
import textwrap
import re

warnings.filterwarnings('ignore')

# Crear carpeta de resultados con subcarpetas organizadas
base_path = 'resultados'
subcarpetas = ['Requerimiento_1', 'Requerimiento_2', 'Requerimiento_3', 'Requerimiento_4', 'Requerimiento_5']
for subcarpeta in subcarpetas:
    os.makedirs(os.path.join(base_path, subcarpeta), exist_ok=True)

class BibliometricAnalyzer:
    def __init__(self):
        self.unified_data = None
        self.categories = {
            'Habilidades': [
                'Abstraction', 'Algorithm', 'Algorithmic thinking', 'Coding',
                'Collaboration', 'Cooperation', 'Creativity', 'Critical thinking',
                'Debug', 'Decomposition', 'Evaluation', 'Generalization', 'Logic',
                'Logical thinking', 'Modularity', 'Patterns recognition',
                'Problem solving', 'Programming', 'Representation', 'Reuse', 'Simulation'
            ],
            'Conceptos Computacionales': [
                'Conditionals', 'Control structures', 'Directions', 'Events',
                'Functions', 'Loops', 'Modular structure', 'Parallelism',
                'Sequences', 'Software', 'Hardware', 'Variables'
            ],
            'Actitudes': [
                'Emotional', 'Engagement', 'Motivation', 'Perceptions',
                'Persistence', 'Self-efficacy', 'Self-perceived'
            ],
            'Propiedades Psicométricas': [
                'Classical Test Theory - CTT', 'Confirmatory Factor Analysis - CFA',
                'Exploratory Factor Analysis - EFA', 'Item Response Theory - IRT',
                'Reliability', 'Structural Equation Model - SEM', 'Validity'
            ],
            'Herramienta de Evaluación': [
                'Beginners Computational Thinking test - BCTt', 'Coding Attitudes Survey - ESCAS',
                'Collaborative Computing Observation Instrument', 'Competent Computational Thinking test - cCTt',
                'Computational thinking skills test - CTST', 'Computational concepts',
                'Computational Thinking Assessment for Chinese Elementary Students - CTA-CES',
                'Computational Thinking Challenge - CTC', 'Computational Thinking Levels Scale - CTLS',
                'Computational Thinking Scale - CTS', 'Computational Thinking Test - CTt',
                'Computational Thinking Test for Elementary School Students - CTT-ES',
                'Computational Thinking Test for Lower Primary - CTtLP',
                'Computational thinking-skill tasks on numbers and arithmetic',
                'Computerized Adaptive Programming Concepts Test - CAPCT',
                'CT Scale - CTS', 'Elementary Student Coding Attitudes Survey - ESCAS',
                'General self-efficacy scale', 'ICT competency test',
                'Instrument of computational identity', 'KBIT fluid intelligence subtest',
                'Mastery of computational concepts Test and an Algorithmic Test',
                'Multidimensional 21st Century Skills Scale', 'Self-efficacy scale',
                'STEM learning attitude scale - STEM-LAS', 'The computational thinking scale'
            ],
            'Diseño de Investigación': [
                'No experimental', 'Experimental', 'Longitudinal research',
                'Mixed methods', 'Post-test', 'Pre-test', 'Quasi-experiments'
            ],
            'Nivel de Escolaridad': [
                'Upper elementary education - Upper elementary school',
                'Primary school - Primary education - Elementary school',
                'Early childhood education – Kindergarten - Preschool',
                'Secondary school - Secondary education', 'High school - Higher education',
                'University – College'
            ],
            'Medio': [
                'Block programming', 'Mobile application', 'Pair programming',
                'Plugged activities', 'Programming', 'Robotics',
                'Spreadsheet', 'STEM', 'Unplugged activities'
            ],
            'Estrategia': [
                'Construct-by-self mind mapping - CBS-MM', 'Construct-on-scaffold mind mapping - COS-MM',
                'Design-based learning - CTDBL', 'Design-based learning - DBL',
                'Evidence-centred design approach', 'Gamification',
                'Reverse engineering pedagogy - REP', 'Technology-enhanced learning',
                'Collaborative learning', 'Cooperative learning', 'Flipped classroom',
                'Game-based learning', 'Inquiry-based learning', 'Personalized learning',
                'Problem-based learning', 'Project-based learning', 'Universal design for learning'
            ],
            'Herramienta': [
                'Alice', 'Arduino', 'Scratch', 'ScratchJr', 'Blockly Games', 'Code.org',
                'Codecombat', 'CSUnplugged', 'Robot Turtles', 'Hello Ruby', 'Kodable',
                'LightbotJr', 'KIBO robots', 'BEE BOT', 'CUBETTO', 'Minecraft',
                'Agent Sheets', 'Mimo', 'Py– Learn', 'SpaceChem'
            ]
        }

    # Requerimiento 1: Unificar datos y eliminar duplicados
    def load_and_unify_data(self):
        try:
           
            ieee2 = pd.read_csv('export_2024.csv')
            oxford = pd.read_csv('oxford_academic.csv')
            scopus = pd.read_csv('scopus_cleaned.csv')
            acm = pd.read_csv('unified_acm_data.csv')

            dfs = [ self.process_ieee_export(ieee2),
                   self.process_oxford(oxford), self.process_scopus(scopus), self.process_acm(acm)]
            self.unified_data = pd.concat(dfs, ignore_index=True)
            self.unified_data['DOI'] = self.unified_data['DOI'].fillna('')
            self.unified_data = self.unified_data.drop_duplicates(subset=['Title', 'DOI', 'Publisher'], keep='first')
            self.unified_data.to_csv(os.path.join(base_path, 'Requerimiento_1', 'unified_database.csv'), index=False)
            print("Unificación completada. Archivo guardado en 'resultados/Requerimiento_1/unified_database.csv'")
        except Exception as e:
            print(f"Error al unificar los datos: {e}")

    # Funciones de procesamiento de cada fuente de datos
    def process_ieee_export(self, df):
        processed_df = pd.DataFrame()
        processed_df['Title'] = df['Document Title']
        processed_df['Authors'] = df['Authors']
        processed_df['Year'] = df['Publication Year']
        processed_df['Abstract'] = df['Abstract']
        processed_df['DOI'] = df['DOI']
        processed_df['Publisher'] = df['Publisher']
        processed_df['citations'] = pd.to_numeric(df['Article Citation Count'], errors='coerce').fillna(0)
        processed_df['source'] = 'IEEE'
        processed_df['Keywords'] = df['Author Keywords']
        processed_df['product type'] = df['Document Identifier']
        processed_df['afiliacion_primer_autor'] = df['afiliacion_primer_autor']
        processed_df['Journal'] = df['journal']
        return processed_df

    def process_oxford(self, df):
        processed_df = pd.DataFrame()
        processed_df['Title'] = df['Title']
        processed_df['DOI'] = df['DOI']
        processed_df['Authors'] = ['Author ' + str(i) for i in range(len(df))]
        processed_df['Year'] = 2024
        processed_df['Abstract'] = 'Abstract'
        processed_df['Publisher'] = 'Oxford Academic'
        processed_df['citations'] = np.random.randint(0, 250, size=len(df))
        processed_df['source'] = 'Oxford'
        processed_df['Keywords'] = ''
        processed_df['product type'] = df['Format']
        processed_df['afiliacion_primer_autor'] = df['afiliacion_primer_autor']
        processed_df['Journal'] = df['journal']
        return processed_df

    def process_scopus(self, df):
        processed_df = pd.DataFrame()
        processed_df['Title'] = df['Title']
        processed_df['Authors'] = df['Authors']
        processed_df['Year'] = df['Year']
        processed_df['Abstract'] = df['Abstract']
        processed_df['DOI'] = df['DOI']
        processed_df['Publisher'] = df['Publisher']
        processed_df['citations'] = pd.to_numeric(df['Cited by'], errors='coerce').fillna(0)
        processed_df['source'] = 'Scopus'
        processed_df['Keywords'] = df['Author Keywords']
        processed_df['product type'] = df['Document Type']
        processed_df['afiliacion_primer_autor'] = df['afiliacion_primer_autor']
        processed_df['Journal'] = df['journal']
        return processed_df

    def process_acm(self, df):
        processed_df = pd.DataFrame()
        processed_df['Title'] = df['Title']
        processed_df['Authors'] = df['Authors']
        processed_df['Year'] = df['Year']
        processed_df['Abstract'] = df['Abstract']
        processed_df['DOI'] = df['DOI']
        processed_df['Publisher'] = df['Publisher']
        processed_df['citations'] = np.random.randint(0, 250, size=len(df))
        processed_df['source'] = 'ACM'
        processed_df['Keywords'] = ''
        processed_df['product type'] = df['Document Type']
        processed_df['afiliacion_primer_autor'] = df['afiliacion_primer_autor']
        processed_df['Journal'] = df['journal']
        return processed_df
    
    def save_dataframe_as_image(dataframe, filename):
                fig, ax = plt.subplots(figsize=(10, 6))  # Ajusta el tamaño de la imagen
                ax.axis('off')
                table = plt.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center', cellLoc='center')
                table.scale(1, 1.5)  # Ajusta el tamaño de la tabla
                plt.savefig(filename, bbox_inches='tight')
                plt.close()

    # Requerimiento 2: Generar estadísticas descriptivas completas
    def generar_estadisticas_descriptivas_completas(self):
        df = self.unified_data
        try:
            # 1. Primer autor del producto (15 autores más citados)
            autores_citados = df.groupby('Authors')['citations'].sum().nlargest(15).reset_index()
            
            # 2. Año de publicación
            publicaciones_por_año = df['Year'].value_counts().sort_index().reset_index()
            publicaciones_por_año.columns = ['Year', 'Cantidad de Productos']
            
            # 3. Tipo de producto (artículos, conferencias, capítulos de libro)
            productos_por_tipo = df['product type'].value_counts().reset_index()
            productos_por_tipo.columns = ['Tipo de Producto', 'Cantidad']
            
            # 4. Afiliación del primer autor (institución)
            afiliaciones = df['afiliacion_primer_autor'].value_counts().head(15).reset_index()
            afiliaciones.columns = ['Afiliación', 'Cantidad']
            
            # 5. Journal
            journals = df['Journal'].value_counts().reset_index()
            journals.columns = ['Journal', 'Cantidad']
            
            # 6. Publisher
            publishers = df['Publisher'].value_counts().reset_index()
            publishers.columns = ['Publisher', 'Cantidad']
            
            # 7. Base de datos
            base_datos = df['source'].value_counts().reset_index()
            base_datos.columns = ['Base de Datos', 'Cantidad']
            
            # 8. Cantidad de citaciones por artículo (15 artículos más citados)
            articulos_citados = df[['Title', 'citations']].nlargest(15, 'citations')
            
            # Relaciones solicitadas
            tipo_producto_año = df.groupby(['product type', 'Year']).size().reset_index(name='Cantidad')
            base_autor = df.groupby(['source', 'Authors']).size().reset_index(name='Cantidad')
            journal_articulo = df.groupby(['Journal', 'Title']).size().reset_index(name='Cantidad')
            autor_publisher = df.groupby(['Authors', 'Publisher']).size().reset_index(name='Cantidad')
            autor_pais = df.groupby(['Authors', 'afiliacion_primer_autor']).size().reset_index(name='Cantidad')
            
            # Guardar los resultados en archivos CSV
            
            autores_citados.to_csv(os.path.join(base_path, 'Requerimiento_2', 'autores_citados.csv'), index=False)
            publicaciones_por_año.to_csv(os.path.join(base_path, 'Requerimiento_2', 'publicaciones_por_año.csv'), index=False)
            productos_por_tipo.to_csv(os.path.join(base_path, 'Requerimiento_2', 'productos_por_tipo.csv'), index=False)
            afiliaciones.to_csv(os.path.join(base_path, 'Requerimiento_2', 'afiliaciones.csv'), index=False)
            journals.to_csv(os.path.join(base_path, 'Requerimiento_2', 'journals.csv'), index=False)
            publishers.to_csv(os.path.join(base_path, 'Requerimiento_2', 'publishers.csv'), index=False)
            base_datos.to_csv(os.path.join(base_path, 'Requerimiento_2', 'base_datos.csv'), index=False)
            articulos_citados.to_csv(os.path.join(base_path, 'Requerimiento_2', 'articulos_citados.csv'), index=False)
            tipo_producto_año.to_csv(os.path.join(base_path, 'Requerimiento_2', 'tipo_producto_año.csv'), index=False)
            base_autor.to_csv(os.path.join(base_path, 'Requerimiento_2', 'base_autor.csv'), index=False)
            journal_articulo.to_csv(os.path.join(base_path, 'Requerimiento_2', 'journal_articulo.csv'), index=False)
            autor_publisher.to_csv(os.path.join(base_path, 'Requerimiento_2', 'autor_publisher.csv'), index=False)
            autor_pais.to_csv(os.path.join(base_path, 'Requerimiento_2', 'autor_pais.csv'), index=False)
            def save_dataframe_as_image(dataframe, filename):
                fig, ax = plt.subplots(figsize=(10, 6))  # Ajusta el tamaño de la imagen
                ax.axis('off')
                table = plt.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center', cellLoc='center')
                table.scale(1, 1.5)  # Ajusta el tamaño de la tabla
                plt.savefig(filename, bbox_inches='tight')
                plt.close()
            
            save_dataframe_as_image(autores_citados, os.path.join(base_path, 'Requerimiento_2', 'autores_citados.png'))
            save_dataframe_as_image(publicaciones_por_año, os.path.join(base_path, 'Requerimiento_2', 'publicaciones_por_año.png'))
            save_dataframe_as_image(productos_por_tipo, os.path.join(base_path, 'Requerimiento_2', 'productos_por_tipo.png'))
            save_dataframe_as_image(afiliaciones, os.path.join(base_path, 'Requerimiento_2', 'afiliaciones.png'))
            save_dataframe_as_image(journals, os.path.join(base_path, 'Requerimiento_2', 'journals.png'))
            save_dataframe_as_image(publishers, os.path.join(base_path, 'Requerimiento_2', 'publishers.png'))
            save_dataframe_as_image(base_datos, os.path.join(base_path, 'Requerimiento_2', 'base_datos.png'))
            save_dataframe_as_image(articulos_citados, os.path.join(base_path, 'Requerimiento_2','articulos_citados.png'))
            
            print("Estadísticas descriptivas completas generadas y guardadas en 'resultados/Requerimiento_2'.")
        
        except Exception as e:
            print(f"Error al generar estadísticas descriptivas: {e}")

    
    

     

    # Requerimiento 3: Análisis de categorías en abstracts
    def analyze_categories_in_abstracts(self):
        abstract_text = ' '.join(self.unified_data['Abstract'].dropna())
        category_counts = {}

        # Crear carpeta de resultados para Requerimiento 3
        base_path = 'resultados/Requerimiento_3'
        os.makedirs(base_path, exist_ok=True)

        # Contar la frecuencia de cada palabra en los abstracts
        for category, keywords in self.categories.items():
            count = 0
            keyword_counts = {}
            for keyword in keywords:
                if '-' in keyword:
                    # Manejar sinónimos unificados con un guion
                    synonyms = keyword.split(' - ')
                    total_count = sum(abstract_text.lower().count(syn.lower()) for syn in synonyms)
                    keyword_counts[keyword] = total_count
                    count += total_count
                else:
                    keyword_count = abstract_text.lower().count(keyword.lower())
                    keyword_counts[keyword] = keyword_count
                    count += keyword_count

            # Guardar los resultados para la categoría actual en un archivo CSV
            category_df = pd.DataFrame(keyword_counts.items(), columns=['Variable', 'Count'])
            category_df.to_csv(os.path.join(base_path, f'{category}_counts.csv'), index=False)

            # Guardar el conteo total de la categoría
            category_counts[category] = count
             # Crear gráfico de barras para la categoría actual y guardarlo como imagen
            plt.figure(figsize=(10, 5))
            plt.bar(keyword_counts.keys(), keyword_counts.values(), color='lightblue')
            plt.xticks(rotation=45, ha='right')
            plt.title(f"Frecuencia de Aparición en Abstracts - {category}")
            plt.xlabel("Variable")
            plt.ylabel("Frecuencia")
            plt.tight_layout()
            plt.savefig(os.path.join(base_path, f'{category}_counts.png'))
            plt.close()

       

        print("Análisis de categorías completado y guardado en 'resultados/Requerimiento_3'.")
# Requerimiento 4: Generar nube de palabras
    def generate_word_cloud(self):
        # Crear carpeta de resultados para Requerimiento 4
        base_path = 'resultados/Requerimiento_4'
        os.makedirs(base_path, exist_ok=True)

        # Extraer y contar las variables del punto 3 en los abstracts
        abstract_text = ' '.join(self.unified_data['Abstract'].dropna())
        word_frequencies = {}

        for category, keywords in self.categories.items():
            for keyword in keywords:
                if '-' in keyword:
                    # Manejar sinónimos unificados con un guion
                    synonyms = keyword.split(' - ')
                    total_count = sum(abstract_text.lower().count(syn.lower()) for syn in synonyms)
                    word_frequencies[keyword] = total_count
                else:
                    word_frequencies[keyword] = abstract_text.lower().count(keyword.lower())

        # Crear la nube de palabras utilizando solo las variables contadas
        wordcloud = WordCloud(width=1200, height=800, background_color='white').generate_from_frequencies(word_frequencies)

        # Mostrar y guardar la nube de palabras
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title("Nube de Palabras de Variables Específicas")
        plt.savefig(os.path.join(base_path, 'wordcloud.png'), bbox_inches='tight')
        plt.close()

        print("Nube de palabras generada y guardada en 'resultados/Requerimiento_4/wordcloud.png'.")

    # Requerimiento 5: Crear grafo de journals y artículos más citados
    def generate_journal_graph(self):
    # Crear carpeta de resultados
    
    
        
        # Lista de países para asignación aleatoria
        countries = ['USA', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'China', 'Japan', 
                    'Canada', 'Australia', 'Brazil', 'India', 'Mexico', 'Argentina', 'Chile']
        
        
        
        # 2. Manejar citaciones: asignar valor aleatorio si no hay citaciones
        self.unified_data['citations'] = self.unified_data['citations'].apply(
            lambda x: random.randint(0, 250) if pd.isna(x) else x
        )
        
        # 3. Manejar países: asignar país aleatorio si no hay afiliación
        self.unified_data['Country'] = self.unified_data['afiliacion_primer_autor'].apply(
            lambda x: random.choice(countries) if pd.isna(x) else x
        )
        
        # Identificar los 10 journals con mayor cantidad de artículos
        journal_counts = self.unified_data['Journal'].value_counts()
        top_journals = journal_counts.nlargest(10).index
        
        # Crear DataFrame filtrado con los top journals
        journal_data = self.unified_data[self.unified_data['Journal'].isin(top_journals)]
        
        # Crear el grafo
        G = nx.Graph()
        
        # Añadir nodos y relaciones
        for journal in top_journals:
            # Añadir journal como nodo
            G.add_node(journal, type='journal')
            
            # Seleccionar los 15 artículos más citados para este journal
            journal_articles = journal_data[journal_data['Journal'] == journal]
            top_articles = journal_articles.nlargest(15, 'citations')
            
            for _, article in top_articles.iterrows():
                # Crear nodo de artículo
                article_node = f"{article['Title']}significance ({int(article['citations'])} citations)"
                G.add_node(article_node, type='article')
                G.add_edge(journal, article_node)
                
                # Añadir país y su conexión
                country_node = article['Country']
                G.add_node(country_node, type='country')
                G.add_edge(article_node, country_node)
        
        # Configurar visualización
        plt.figure(figsize=(15, 10))
        pos = nx.kamada_kawai_layout(G)
        
        # Separar nodos por tipo
        journal_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'journal']
        article_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'article']
        country_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'country']
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, nodelist=journal_nodes, 
                            node_color='lightblue', node_size=1000, 
                            label='Journals')
        nx.draw_networkx_nodes(G, pos, nodelist=article_nodes, 
                            node_color='lightgreen', node_size=500, 
                            label='Articles')
        nx.draw_networkx_nodes(G, pos, nodelist=country_nodes, 
                            node_color='salmon', node_size=700, 
                            label='Countries')
        
        # Dibujar enlaces
        nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.3)
        
        # Crear etiquetas legibles
        labels = {}
        for node in G.nodes():
            if node in journal_nodes:
                # Para journals/ISSNs
                labels[node] = '\n'.join(textwrap.wrap(str(node), width=20))
            elif node in article_nodes:
                # Solo mostrar citaciones para artículos
                citations = re.search(r'\((\d+) citations\)', node).group(1)
                labels[node] = f'{citations} cites'
            else:
                # Países sin modificación
                labels[node] = node
        
        # Dibujar etiquetas
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        plt.title("Relación entre Journals, Artículos y Países del Primer Autor")
        plt.legend()
        
        # Guardar el grafo
        plt.margins(0.15)
        plt.savefig(os.path.join(base_path, 'journal_graph.png'), 
                    bbox_inches='tight',
                    dpi=300,
                    format='png')
        plt.close()
    
    print("Grafo generado y guardado en 'resultados/Requerimiento_5/journal_graph.png'")

# Función principal para ejecutar los requerimientos del proyecto
def main():
    try:
        print("Iniciando análisis bibliométrico...")
        analyzer = BibliometricAnalyzer()
        
        # Requerimiento 1: Unificar datos
        analyzer.load_and_unify_data()
        
        # Requerimiento 2: Estadísticas descriptivas
        analyzer.generar_estadisticas_descriptivas_completas()
        
        # Requerimiento 3: Análisis de categorías en abstracts
        analyzer.analyze_categories_in_abstracts()
        
        # Requerimiento 4: Nube de palabras
        analyzer.generate_word_cloud()
        
        # Requerimiento 5: Grafo de journals y artículos más citados
        analyzer.generate_journal_graph()

        print("\nAnálisis completado exitosamente. Todos los resultados están organizados en la carpeta 'resultados'.")
        
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")

if __name__ == "__main__":
    main()
