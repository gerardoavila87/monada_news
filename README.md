# Análisis de Noticias violentas por Estados de México

Este programa realiza un análisis de noticias que mencionen la violencia, obtenidas desde la API de **NewsAPI** para contar cuántas veces se mencionan los diferentes estados de México. 

## Funcionalidad

El programa sigue estos pasos principales:

1. **Obtención de noticias**: Realiza múltiples solicitudes a la API de noticias utilizando diferentes parámetros, los cuales se cargan aleatoriamente desde un archivo params.json el cual contiene parametros correctos y erroneos.
   
2. **Procesamiento de artículos**: Extrae el contenido de las noticias, los limpia, y luego cuenta cuántas veces se mencionan los nombres de los estados, los cuales están definidos en un archivo estados.json.

3. **Conteo de menciones**: Conteo de menciones: Utiliza una función que recorre los textos de las noticias para contar cuántas veces aparece cada estado y guarda los resultados en un contador.

4. **Simulación de retrasos**: Entre cada solicitud a la API, se introduce un retardo aleatorio para simular tiempos de espera.

## Requisitos

Este proyecto requiere **Python 3.x** y las siguientes bibliotecas:

- `requests`
- `json`
- `random`
- `time`
- `functools`
- `collections`

Puedes instalar la biblioteca `requests` usando el siguiente comando:

```bash
pip install requests
```

## Archivos

El programa utiliza los siguientes archivos JSON:

- **`estados.json`**: Contiene una lista de los nombres de los estados de México.
- **`params.json`**: Contiene los parámetros de búsqueda para la API de NewsAPI.

### `estados.json`
```json
[
    "AGUASCALIENTES",
    "BAJA CALIFORNIA",
    "BAJA CALIFORNIA SUR",
    ...
]
```

### `params.json`
```json
[
    {
        "searchIn": "content",
        "api_key": "YOUR_API_KEY",
        "q": "violencia",
        "from": "2024-09-01"
    },
    ...
]
```