import re  # Importar la librería de expresiones regulares
import requests
from collections import Counter
from functools import reduce
from typing import Union


# Clase Optional para manejar valores opcionales de forma segura
class Optional:
    def __init__(self, value:Union[list,None]) -> None:
        self._value = value

    def is_empty(self):
        return self._value is None

    def get(self):
        if self.is_empty():
            raise ValueError("No hay ningún valor")
        return self._value

    def map(self, func):
        if self.is_empty():
            return self
        return Optional(func(self._value))

# Obtener noticias desde la API de NewsAPI
def obtener_noticias(api_key, consulta_noticias, fecha_noticias):
    url = "https://newsapi.org/v2/everything"
    params = {
        'searchIn':'content',
        'from':fecha_noticias,
        'q': consulta_noticias,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)

    return Optional(response.json().get('articles', []))

# Función para limpiar y combinar título y descripción de cada noticia
def limpiar_y_combinar_noticias(noticias):
    if noticias:
        return list(map(lambda noticia: (noticia['title'] or '') + ' ' + (noticia['description'] or ''), noticias))
    return []

# Función para extraer palabras clave de las noticias
def extraer_palabras_clave(texto, excluir_palabras):
    palabras = re.findall(r'\b\w+\b', texto.lower())  # Extrae palabras ignorando mayúsculas y minúsculas
    palabras_frecuentes = [palabra for palabra in palabras if len(palabra) > 3 and palabra not in excluir_palabras]
    return Counter(palabras_frecuentes)

# Función principal que ejecuta el análisis de noticias y cuenta las palabras clave
def analizar_temas_en_noticias(api_key, consulta_noticias, fecha_noticias, excluir_palabras):
    # 1. Obtener noticias y usar map para procesarlas si están disponibles
    lista_noticias = obtener_noticias(api_key, consulta_noticias, fecha_noticias)
    
    # 2. Obtener el valor de noticias o una lista vacía si está vacío
    noticias = lista_noticias.get()

    # 3. Limpiar y combinar las noticias
    textos_noticias = limpiar_y_combinar_noticias(noticias)

    # 4. Extraer y contar las palabras clave
    contador_final = reduce(lambda acc, texto: acc + extraer_palabras_clave(texto, excluir_palabras), textos_noticias, Counter())

    return contador_final
    
# Main - Ejecutar análisis
if __name__ == "__main__":

    # Lista de palabras comunes a excluir
    excluir_palabras = {
        'jalisco', 'méxico', 'guadalajara', 'este', 'para', 'como', 'con', 'del', 'desde',
        'más', 'que', 'una', 'los', 'las', 'sus', 'por', 'y', 'en', 'el', 'la', 'es', 'de',
        'un', 'no', 'al', 'se', 'lo', 'a', 'sobre', 'han', 'son', 'una', 'entre', 'pero', 'ha',
        'from', 'estados', 'nacional', 'california', 'donde', 'dónde', 'baja', 'removed', '2024',
        'esta'
    }
    api_key = 'dfcde560d60e4f98b41098c0d2d60d77' 
    consulta_noticias = 'Jalisco' 
    fecha_noticias = '2024-09-12'

    conteo_palabras = analizar_temas_en_noticias(api_key, consulta_noticias, fecha_noticias, excluir_palabras)

    for palabra, conteo in conteo_palabras.most_common(10):  # Mostrar solo las 10 palabras más mencionadas
        print(f"{palabra}: {conteo} veces")

