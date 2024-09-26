import requests
import json
from collections import Counter
from functools import reduce
import re  # Importar la librería de expresiones regulares

# Obtener noticias desde la API de NewsAPI
def obtener_noticias(api_key, query):
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    return response.json().get('articles', [])

# Cargar el archivo JSON con los municipios
def cargar_municipios(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para limpiar y combinar título y descripción de cada noticia
def limpiar_y_combinar_noticias(noticias):
    return map(lambda noticia: (noticia['title'] or '') + ' ' + (noticia['description'] or ''), noticias)

# Función para contar la aparición de municipios en las noticias utilizando expresiones regulares
def contar_municipios_en_texto(texto, municipios_por_estado):
    contador = Counter()
    for estado, municipios in municipios_por_estado.items():
        for municipio in municipios:
            # Usamos una expresión regular para encontrar coincidencias exactas de palabras
            patron = r'\b' + re.escape(municipio) + r'\b'
            if re.search(patron, texto, re.IGNORECASE):
                contador[(estado, municipio)] += 1
    return contador

# Función principal que ejecuta el análisis de noticias y cuenta los municipios
def analizar_municipios_en_noticias(api_key, query, municipios_file):
    # 1. Obtener noticias
    noticias = obtener_noticias(api_key, query)
    
    # 2. Cargar municipios desde archivo JSON
    municipios_por_estado = cargar_municipios(municipios_file)

    # 3. Limpiar y combinar las noticias
    textos_noticias = limpiar_y_combinar_noticias(noticias)
    
    # 4. Contar ocurrencias de municipios en todas las noticias
    contador_final = reduce(lambda acc, texto: acc + contar_municipios_en_texto(texto, municipios_por_estado), textos_noticias, Counter())
    
    # 5. Devolver el conteo final
    return contador_final

# Mostrar resultados ordenados de mayor a menor
def mostrar_resultados(conteo_municipios):
    for (estado, municipio), conteo in conteo_municipios.most_common():
        print(f"{estado} - {municipio}: {conteo} veces")

# Main - Ejecutar análisis
if __name__ == "__main__":
    api_key = 'dfcde560d60e4f98b41098c0d2d60d77'  # API key
    query = 'violencia, México'
    municipios_file = 'municipios_mexico.json'  # Archivo JSON con todos los municipios de México

    conteo_municipios = analizar_municipios_en_noticias(api_key, query, municipios_file)
    mostrar_resultados(conteo_municipios)
