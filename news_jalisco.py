import re
import requests
import random
import time
import json
from collections import Counter
from functools import reduce
from typing import Union, List, Dict, Any

# Clase Optional para manejar valores opcionales de forma segura
class Optional:
    def __init__(self, value: Union[Any, None]) -> None:
        self._value = value

    def is_empty(self) -> bool:
        return self._value is None

    def get(self) -> Any:
        if self.is_empty():
            print("No hay ningún valor")
            return None
        return self._value

    def map(self, func) -> 'Optional':
        if self.is_empty():
            return self
        return Optional(func(self._value))
    


# Obtener noticias desde la API de NewsAPI con posibilidad de generar errores
def obtener_noticias(url: str, params: Dict[str, str]) -> Optional:
    try:
        response = requests.get(url, params)
        print(response.status_code)
        data = response.json()
        print(data)
        if response.status_code != 200:
            raise ValueError(f"Error en la API: {data.get('message', 'Respuesta no válida')}")

        return Optional(data.get('articles', []))
    
    except Exception as err:
        print(f"Error al obtener noticias: {err}")
        return Optional(None)

# Función para limpiar y combinar título y descripción de cada noticia
def limpiar_y_combinar_noticias(noticias: List[Dict[str, str]]) -> List[str]:
    if noticias:
        return list(map(lambda noticia: (noticia.get('title', '') or '') + ' ' + (noticia.get('description', '') or ''), noticias))
    return []

# Función para extraer menciones de municipios en las noticias
def contar_menciones_estados(texto: str, estados: List[str]) -> Counter:
    menciones = Counter()
    for estado in estados:
        if estado.lower() in texto.lower():
            menciones[estado] += texto.lower().count(estado.lower())
    return menciones

# Función principal que ejecuta el análisis de noticias y cuenta las menciones de estados
def analizar_noticias(url: str, params: Dict[str, str], estados: List[str]) -> Counter:
    lista_noticias = obtener_noticias(url, params)
    textos_noticias = lista_noticias.map(limpiar_y_combinar_noticias).get()
    
    if textos_noticias:
        contador_estados = reduce(lambda acc, texto: acc + contar_menciones_estados(texto, estados), textos_noticias, Counter())
    return contador_estados

# Función para leer archivos JSON
def leer_json(archivo: str) -> Union[List, Dict, None]:
    try:
        archivo_optional = Optional(archivo)
        contenido = archivo_optional.map(lambda archivo: with_open(archivo)).get()
        return json.loads(contenido)
    except Exception as e:
        print(f"Error al leer {archivo}: {e}")
        return None

def with_open(archivo: str) -> str:
    with open(archivo, 'r', encoding='utf-8') as texto_salida:
        return texto_salida.read()


# Main - Ejecutar múltiples solicitudes simulando diferentes errores
if __name__ == "__main__":
    url = "https://newsapi.org/v2/everything"
    
    # Leer los municipios desde el archivo JSON
    estados = leer_json('estados.json')
    
    if estados is None:
        print("Error al cargar los municipios.")
        exit()
    
    # Leer los parámetros desde el archivo JSON
    params_random = leer_json('params.json')
    
    if params_random is None:
        print("Error al cargar los parámetros.")
        exit()
    
    random.shuffle(params_random)
    
    for params in params_random:
        menciones_estados = analizar_noticias(url, params, estados)
        
        if menciones_estados:
            for estado, conteo in menciones_estados.most_common():
                print(f"{estado}: {conteo} veces")
        else:
            print("No se pudieron analizar noticias debido a errores.")
        
        time.sleep(random.uniform(1, 5))  # Retardo entre 1 y 5 segundos
