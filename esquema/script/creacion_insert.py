from asyncio import TaskGroup, run
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from time import time
from typing import Iterator

import aiofiles
from dataclass_wizard import JSONWizard
from dataclass_wizard.wizard_mixins import JSONFileWizard
from httpx import get
from lxml import etree
from lxml.cssselect import CSSSelector

ARCHIVO_IDIOMAS = Path("/output/6_idiomas_g.sql")
ARCHIVO_PAISES = Path("/output/7_paises_g.sql")


class IndicesValores(IntEnum):
    NOMBRE_ISO = 0
    ALFA_2 = 1
    ALFA_3 = 2


@dataclass
class ArchivoPeliculas(JSONWizard, JSONFileWizard):
    peliculas: list[str]


def paises_insert() -> Iterator[tuple[str, str, str]]:
    respuesta_server = get(
        "https://api.wikimedia.org/core/v1/wikipedia/es/page/ISO_3166-1/html"
    )
    datos_html = respuesta_server.text
    pagina_datos = etree.fromstring(datos_html)
    selector_filas_datos = CSSSelector("table#mwBxc > tbody#mwBxg > tr:nth-child(n+2)")
    selector_columnas_alfa_1_2 = CSSSelector("td:nth-child(3), td:nth-child(4)")
    selector_columna_nombre_comun = CSSSelector("td:nth-child(1) > a")
    filas_datos = selector_filas_datos(pagina_datos)
    for fila_actual in filas_datos:
        valores_pais_actual: list[str] = []
        elemento_nombre_comun = selector_columna_nombre_comun(fila_actual)[0]
        valores_pais_actual.append(elemento_nombre_comun.text)
        for columna_actual in selector_columnas_alfa_1_2(fila_actual):
            valores_pais_actual.append(columna_actual.text)
        valor_retornado = (
            valores_pais_actual[0],
            valores_pais_actual[1],
            valores_pais_actual[2],
        )
        yield valor_retornado
        valores_pais_actual = []


def idiomas_insert() -> Iterator[tuple[str, str]]:
    datos_html: str
    respuesta_server = get(
        "https://api.wikimedia.org/core/v1/wikipedia/es/page/ISO_639-1/html"
    )
    datos_html = respuesta_server.text
    pagina_datos = etree.fromstring(datos_html)
    selector_filas_datos = CSSSelector("table#mwUw > tbody#mwVA > tr")
    selector_columna_iso = CSSSelector("td:nth-child(1) > b")
    selector_columna_descripcion = CSSSelector("td:nth-child(2) > a")
    for fila in selector_filas_datos(pagina_datos):
        valor_iso = selector_columna_iso(fila)[0].text
        valor_descripcion = selector_columna_descripcion(fila)[0].text
        valor_retornado = (valor_iso, valor_descripcion)
        yield valor_retornado


async def creacion_insert_paises(
    datos_pais: tuple[str, str, str], archivo_salida: Path
) -> Path:
    async with aiofiles.open(archivo_salida, mode="a") as archivo:
        await archivo.write(
            f"insert into pais(id_pais,codigo_alfa_3, descripcion) values ('{datos_pais[1]}', '{datos_pais[2]}', '{datos_pais[0]}');\n"
        )
        print(f"Agregado {datos_pais} -> {archivo_salida}")
    return archivo_salida


async def creacion_insert_idiomas(
    datos_idioma: tuple[str, str], archivo_salida: Path
) -> Path:
    async with aiofiles.open(archivo_salida, mode="a") as archivo:
        await archivo.write(
            f"insert into lenguaje(id_lenguaje, nombre) values ('{datos_idioma[0]}', '{datos_idioma[1]}');\n"
        )
        print(f"Agregado idioma {datos_idioma} -> {archivo_salida}")
    return archivo_salida


async def inserts_wikipedia() -> None:
    start_time = time()
    async with TaskGroup() as tareas_http:
        for idioma in idiomas_insert():
            tareas_http.create_task(creacion_insert_idiomas(idioma, ARCHIVO_IDIOMAS))
        for pais in paises_insert():
            tareas_http.create_task(creacion_insert_paises(pais, ARCHIVO_PAISES))
    elapsed_time = time() - start_time
    print(
        f"Tiempo de ejecución para creacion de inserts de wikipedia: {elapsed_time:.4f} segundos"
    )


async def main() -> None:
    async with aiofiles.open(ARCHIVO_PAISES, mode="a") as paises_sql:
        await paises_sql.write("SET NAMES 'utf8mb4';\n")
    async with aiofiles.open(ARCHIVO_IDIOMAS, mode="a") as idiomas_sql:
        await idiomas_sql.write("SET NAMES 'utf8mb4';\n")
    await inserts_wikipedia()


if __name__ == "__main__":
    run(main())
