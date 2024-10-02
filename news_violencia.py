#!/usr/bin/env python3
import requests
import random
import time
import json
from collections import Counter
from functools import reduce
from typing import Union, List, Dict, Any

# Este programa realiza un análisis de noticias que mencionen la violencia, 
# obtenidas desde la API de NewsAPI para contar cuántas veces se mencionan
# los diferentes estados de México. 

# 1.- Obtención de datos: Realiza múltiples solicitudes a la API de noticias
# utilizando diferentes parámetros, los cuales se cargan aleatoriamente desde
# un archivo params.json el cual contiene parametros correctos y erroneos.

# 2.- Procesamiento de noticias: Extrae el contenido de las noticias, los 
# limpia, y luego cuenta cuántas veces se mencionan los nombres de los estados,
# los cuales están definidos en un archivo estados.json.

# 3.- Conteo de menciones: Utiliza una función que recorre los textos de las 
# noticias para contar cuántas veces aparece cada estado y guarda los 
# resultados en un contador.

# 4.- Simulación de retrasos: Entre cada solicitud a la API, el programa 
# introduce un retardo aleatorio para simular el tiempo de espera.

# 5.- El objetivo final es mostrar cuántas veces es mencionado cada estado en 
# las noticias violentas.

class Optional:
    #Clase Optional para manejar valores opcionales de forma segura.

    def __init__(self, value: Union[Any, None]) -> None:
        self._value = value

    def is_empty(self) -> bool:
        return self._value is None

    # Método seguro
    def get(self) -> Any:
        if self.is_empty():
            return None
        return self._value

    # Función de alto orden
    def map(self, func) -> 'Optional':
        if self.is_empty():
            return self
        return Optional(func(self._value))


def obtener_noticias(url: str, params: Dict[str, str]) -> Optional:
    # Obtiene noticias desde la API de NewsAPI. 
    # Utiliza la mónada para saber si se pudieron obtener o no
    # las noticias de la api.
    # Args:
       # url (str): URL de la API.
       # params (Dict[str, str]): Parámetros de la solicitud.
    # Returns: Optional: Lista de artículos o None si ocurre un error.
    try:
        response = requests.get(url, params)
        data = response.json()
        if response.status_code != 200:
            raise ValueError(f"Error en la API: {data.get('message', 'Respuesta no válida')}")
        articulos = Optional(data.get('articles', []))
        return articulos

    except Exception as err:
        print(f"Error al obtener noticias: {err}")
        return Optional(None)


def limpiar_y_combinar_noticias(noticias: List[Dict[str, str]]) -> List[str]:
    # Limpia y combina el contenido de las noticias.
    # Args:
        # noticias (List[Dict[str, str]]): Lista de noticias.
    # Returns:
        # List[str]: Lista de contenidos de noticias.
        
    if noticias:
        return list(map(lambda noticia: noticia.get('content', '') or '', noticias))
    return []


def contar_menciones_estados(texto: str, estados: List[str]) -> Counter:
    # Cuenta las menciones de estados en el texto.
    # Args:
        # texto (str): Texto en el que buscar menciones.
        # estados (List[str]): Lista de estados a buscar.
    # Returns:
        # Counter: Contador de menciones de cada estado.

    menciones = Counter()
    for estado in estados:
        if estado.lower() in texto.lower():
            menciones[estado] += texto.lower().count(estado.lower())
    return menciones


def analizar_noticias(url: str, params: Dict[str, str], estados: List[str]) -> Counter:
    # Analiza las noticias y cuenta menciones de estados.
    # Args:
        # url (str): URL de la API (https://newsapi.org/v2/everything). 
        # params (Dict[str, str]): Parámetros para la API.
        # estados (List[str]): Lista de estados del país para buscar 
        # coincidencia en las noticias.
    # Returns:
        # Counter: Número de menciones de los estados del país.

    lista_noticias = obtener_noticias(url, params)
    # La lista de noticias es de tipo Optional y sirve para poder usar 
    # la mónada y maneje los posibles errores en la consulta de News API
    textos_noticias = lista_noticias.map(limpiar_y_combinar_noticias).get()
    
    contador_estados = Counter()

    if textos_noticias:
        contador_estados = reduce(
            lambda acc, texto: acc + contar_menciones_estados(texto, estados),
            textos_noticias,
            Counter()
        )
        
    return contador_estados


def leer_json(archivo: str) -> Union[List, Dict, None]:
    # Lee un archivo JSON.
    # Args:
        # archivo (str): Ruta al archivo JSON.
    # Returns:
        # Union[List, Dict, None]: Contenido del archivo JSON o None si ocurre 
        # un error.

        # La lista es para los estados, el diccionario para los parametros y 
        # None se usa cuando no existe el archivo o hay algún error en la 
        # lectura.
    
    try:
        archivo_optional = Optional(archivo)
        contenido = archivo_optional.map(lambda archivo: with_open(archivo)).get()
        return json.loads(contenido)
    except Exception as e:
        print(f"Error al leer {archivo}: {e}")
        return None


def with_open(archivo: str) -> str:
    # Abre un archivo y lee su contenido.
    # Args:
        # archivo (str): Ruta al archivo.
    # Returns:
        # str: Contenido del archivo.

    with open(archivo, 'r', encoding='utf-8') as texto_salida:
        return texto_salida.read()

# entry point
if __name__ == "__main__":
    url = "https://newsapi.org/v2/everything"

    # Leer los estados desde el archivo JSON
    estados = leer_json('estados.json')
    
    if estados is None:
        print("Error al cargar los estados.")
        exit()
    
    # Leer los parámetros desde el archivo JSON
    params_random = leer_json('params.json')
    
    if params_random is None:
        print("Error al cargar los parámetros.")
        exit()
    
    # Aplica un random a los parametros para que en cada ejecución
    # tengan diferente orden
    random.shuffle(params_random)
    
    # Realiza el número de consultas que se contienen en el JSON params
    for index, params in enumerate(params_random, start=1):
        # Muestra que número de consulta se está ejecutando
        print(f"Consultando la API... ({index})")
        # Retardo entre 1 y 5 segundos
        time.sleep(random.uniform(1, 5))  
        menciones_estados = analizar_noticias(url, params, estados)
    
        if menciones_estados:
            for estado, conteo in menciones_estados.most_common():
                print(f"{estado}: {conteo} veces")