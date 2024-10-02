import re
import requests
import random
import time
import json
from collections import Counter
from functools import reduce
from typing import Union, List, Dict

# Clase Optional para manejar valores opcionales de forma segura
class Optional:
    def __init__(self, value: Union[list, None]) -> None:
        self._value = value

    def is_empty(self) -> bool:
        return self._value is None

    def get(self) -> Union[list, None]:
        if self.is_empty():
            raise ValueError("No hay ningún valor")
        return self._value

    def map(self, func) -> 'Optional':
        if self.is_empty():
            return self
        return Optional(func(self._value))


# Obtener noticias desde la API de NewsAPI con posibilidad de generar errores
def obtener_noticias(url: str, params: Dict[str, str]) -> Optional:
    try:
        response = requests.get(url, params)
        data = response.json()
        return Optional(data.get('articles', []))
    except Exception as err:
        print(f"Error al obtener noticias: {err}")
        return Optional(None)

# Función para limpiar y combinar título y descripción de cada noticia
def limpiar_y_combinar_noticias(noticias: List[Dict[str, str]]) -> List[str]:
    if noticias:
        return list(map(lambda noticia: (noticia['title'] or '') + ' ' + (noticia['description'] or ''), noticias))
    return []

# Función para extraer menciones de municipios en las noticias
def contar_menciones_municipios(texto: str, municipios: List[str]) -> Counter:
    menciones = Counter()
    for municipio in municipios:
        if municipio.lower() in texto.lower():
            menciones[municipio] += texto.lower().count(municipio.lower())
    return menciones

# Función principal que ejecuta el análisis de noticias y cuenta las menciones de municipios
def analizar_noticias(url: str, params: Dict[str, str], municipios: List[str]) -> Counter:
    lista_noticias = obtener_noticias(url, params)
    textos_noticias = lista_noticias.map(limpiar_y_combinar_noticias).get()
    contador_municipios = reduce(lambda acc, texto: acc + contar_menciones_municipios(texto, municipios), textos_noticias, Counter())
    return contador_municipios

# Función para leer archivos JSON
def leer_json(archivo: str) -> Union[List, Dict, None]:
    try:
        archivo_optional = Optional(archivo)
        contenido = archivo_optional.map(whit_open(archivo)).get()
        return json.load(contenido)
    except Exception as e:
        print(f"Error al leer {archivo}: {e}")
        return None

def whit_open(archivo: str) -> str:
    with open(archivo, 'r', encoding='utf-8') as texto_salida:
        return texto_salida.read()


# Main - Ejecutar múltiples solicitudes simulando diferentes errores
if __name__ == "__main__":
    url = "https://newsapi.org/v2/everything"
    
    # Leer los municipios desde el archivo JSON
    municipios = leer_json('municipios.json')
    
    if municipios is None:
        print("Error al cargar los municipios.")
        exit()
    
    # Leer los parámetros desde el archivo JSON
    params_random = leer_json('params.json')
    
    if params_random is None:
        print("Error al cargar los parámetros.")
        exit()
    
    random.shuffle(params_random)
    
    for params in params_random:
        menciones_municipios = analizar_noticias(url, params, municipios)
        
        if menciones_municipios:
            for municipio, conteo in menciones_municipios.most_common():
                print(f"{municipio}: {conteo} veces")
        else:
            print("No se pudieron analizar noticias debido a errores.")
        
        time.sleep(random.uniform(1, 5))  # Retardo entre 1 y 5 segundos
