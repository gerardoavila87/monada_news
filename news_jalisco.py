import requests
import json
from collections import Counter
from functools import reduce
import re  # Importar la librería de expresiones regulares
from collections import defaultdict

# Lista de palabras comunes a excluir ("stop words")
STOP_WORDS = {
    'jalisco', 'méxico', 'guadalajara', 'este', 'para', 'como', 'con', 'del', 'desde',
    'más', 'que', 'una', 'los', 'las', 'sus', 'por', 'y', 'en', 'el', 'la', 'es', 'de',
    'un', 'no', 'al', 'se', 'lo', 'a', 'sobre', 'han', 'son', 'una', 'entre', 'pero', 'ha',
    'from', 'estados', 'nacional', 'california', 'donde', 'dónde', 'baja'
}

# Obtener noticias desde la API de NewsAPI
def obtener_noticias(api_key, query):
    url = "https://newsapi.org/v2/everything"
    params = {
        'searchIn':'content',
        'from':'2024-09-01',
        'q': query,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    return response.json().get('articles', [])

# Función para limpiar y combinar título y descripción de cada noticia
def limpiar_y_combinar_noticias(noticias):
    return map(lambda noticia: (noticia['title'] or '') + ' ' + (noticia['description'] or ''), noticias)

# Función para extraer palabras clave de las noticias
def extraer_palabras_clave(texto):
    palabras = re.findall(r'\b\w+\b', texto.lower())  # Extrae palabras ignorando mayúsculas y minúsculas
    palabras_frecuentes = [palabra for palabra in palabras if len(palabra) > 3 and palabra not in STOP_WORDS]
    return Counter(palabras_frecuentes)

# Función principal que ejecuta el análisis de noticias y cuenta las palabras clave
def analizar_temas_en_noticias(api_key, query):
    # 1. Obtener noticias
    noticias = obtener_noticias(api_key, query)

    # 2. Limpiar y combinar las noticias
    textos_noticias = limpiar_y_combinar_noticias(noticias)

    # 3. Extraer y contar las palabras clave
    contador_final = reduce(lambda acc, texto: acc + extraer_palabras_clave(texto), textos_noticias, Counter())

    # 4. Devolver el conteo final
    return contador_final

# Mostrar resultados ordenados de mayor a menor
def mostrar_resultados(conteo_palabras):
    for palabra, conteo in conteo_palabras.most_common(10):  # Mostrar solo las 10 palabras más mencionadas
        print(f"{palabra}: {conteo} veces")

# Main - Ejecutar análisis
if __name__ == "__main__":
    api_key = 'dfcde560d60e4f98b41098c0d2d60d77'  # API key
    query = 'Jalisco'  # Consultar específicamente Jalisco

    conteo_palabras = analizar_temas_en_noticias(api_key, query)
    mostrar_resultados(conteo_palabras)
