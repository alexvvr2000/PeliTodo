from pathlib import Path
from random import sample
from typing import AsyncIterator

import aiofiles
from async_lru import alru_cache
from httpx import AsyncClient
from pelis.requests_tmdb import (
    dict_imagenes_pelicula,
    dict_involucrados_pelicula,
    dict_pelicula,
    dict_perfil_artista,
    dict_traducciones_pelicula,
)
from pelis.typos import (
    ID_GENERO_BASE,
    ID_LENGUAJE_BASE,
    ID_PELICULA_BASE,
    ID_PELICULA_TMDB,
    INFORMACION_INVOLUCRADO_PELICULA,
    INFORMACION_PELICULA,
    INFORMACION_TITULO_PELICULA,
    INFORMACION_URL_IMAGEN,
)
from pelis.utils import AsignadorIndices


async def informacion_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> INFORMACION_PELICULA:
    json_datos = await dict_pelicula(id_pelicula, cliente_http)
    return (
        json_datos["release_date"],
        json_datos["origin_country"][0],
        json_datos["runtime"],
    )


async def agregar_pelicula(
    id_pelicula_base: int, datos: INFORMACION_PELICULA, ruta_archivo: Path
) -> tuple[int, Path]:
    async with aiofiles.open(ruta_archivo, "a") as sql:
        await sql.write(
            f"""insert into pelicula(id_pelicula, fecha_estreno, id_pais, duracion)
values({id_pelicula_base}, "{datos[0]}", "{datos[1]}", {datos[2]});\n"""
        )
    return (id_pelicula_base, ruta_archivo)


async def lenguajes_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> AsyncIterator[ID_LENGUAJE_BASE]:
    json_datos = await dict_traducciones_pelicula(id_pelicula, cliente_http)
    for traduccion in json_datos["translations"]:
        yield traduccion["iso_639_1"]


async def agregar_lenguaje_pelicula(
    id_pelicula: ID_PELICULA_BASE,
    id_lenguaje: ID_LENGUAJE_BASE,
    ruta_archivo: Path,
) -> tuple[ID_PELICULA_BASE, ID_LENGUAJE_BASE, Path]:
    async with aiofiles.open(ruta_archivo, "a") as sql:
        await sql.write(
            f"""insert ignore into lenguaje_pelicula(id_pelicula, id_lenguaje)
values({id_pelicula},"{id_lenguaje}");\n"""
        )
    return (id_pelicula, id_lenguaje, ruta_archivo)


async def imagenes_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> AsyncIterator[INFORMACION_URL_IMAGEN]:
    json_datos = await dict_imagenes_pelicula(id_pelicula, cliente_http)
    for imagen in sample(json_datos["backdrops"], 3):
        yield ("backdrop", imagen["file_path"])
    for imagen in sample(json_datos["posters"], 3):
        yield ("poster", imagen["file_path"])
    for imagen in sample(json_datos["logos"], 3):
        yield ("logo", imagen["file_path"])


async def agregar_imagen_pelicula(
    id_pelicula: ID_PELICULA_BASE,
    datos_imagen: INFORMACION_URL_IMAGEN,
    ruta_archivo: Path,
) -> tuple[int, Path]:
    async with aiofiles.open(ruta_archivo, "a") as sql:
        await sql.write(
            f"""insert into imagen_pelicula(id_pelicula, url_imagen, descripcion)
values({id_pelicula}, "{datos_imagen[1]}", "{datos_imagen[0]}");\n"""
        )
    return (id_pelicula, ruta_archivo)


async def titulos_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> AsyncIterator[tuple[str, str]]:
    @alru_cache
    async def titulo_original(titulo_traduccion: str) -> str:
        if titulo_traduccion == "":
            valor_titulo_original = await dict_pelicula(id_pelicula, cliente_http)
            return valor_titulo_original["title"]
        return titulo_traduccion

    json_datos = await dict_traducciones_pelicula(id_pelicula, cliente_http)
    for titulo_api in sample(json_datos["translations"], 5):
        yield (
            titulo_api["iso_3166_1"],
            await titulo_original(titulo_api["data"]["title"]),
        )


async def agregar_titulo_pelicula(
    id_pelicula: ID_PELICULA_BASE,
    datos_lenguajes: INFORMACION_TITULO_PELICULA,
    ruta_archivo: Path,
) -> tuple[int, Path]:
    async with aiofiles.open(ruta_archivo, "a") as sql:
        await sql.write(
            f"""insert into titulo_pelicula(id_pelicula, id_pais, titulo_alternativo)
values({id_pelicula}, "{datos_lenguajes[0]}", "{datos_lenguajes[1]}");\n"""
        )
    return (id_pelicula, ruta_archivo)


async def generos_pelicula(
    id_pelicula_tmdb: ID_PELICULA_TMDB,
    cliente_http: AsyncClient,
    asignador_generos: AsignadorIndices,
) -> AsyncIterator[tuple[ID_GENERO_BASE, str]]:
    json_datos = await dict_pelicula(id_pelicula_tmdb, cliente_http)
    lista_generos_pelicula: list[str] = [
        genero["name"] for genero in json_datos["genres"]
    ]
    for genero_pelicula in lista_generos_pelicula:
        indice_actual = await asignador_generos.crear_indice((genero_pelicula,))
        yield (indice_actual, genero_pelicula)


async def agregar_genero_pelicula(
    id_pelicula: ID_PELICULA_BASE,
    ruta_archivo: Path,
    id_genero: ID_GENERO_BASE,
) -> tuple[ID_GENERO_BASE, Path]:
    async with aiofiles.open(ruta_archivo, "a") as sql:
        await sql.write(
            f"""insert into genero_pelicula(id_pelicula, id_genero)
                values({id_pelicula}, {id_genero});\n"""
        )
    return (id_pelicula, ruta_archivo)


async def agregar_artista_base(
    id_artista_tmdb: int, cliente_http: AsyncClient, asignador_artista: AsignadorIndices
) -> int:
    informacion_artista = await dict_perfil_artista(id_artista_tmdb, cliente_http)
    datos_artista: tuple[str, str, str] = (
        informacion_artista["name"],
        (
            f'"{informacion_artista["birthday"]}"'
            if informacion_artista["birthday"] is not None
            else "NULL"
        ),
        (
            f'"{informacion_artista["deathday"]}"'
            if informacion_artista["deathday"] is not None
            else "NULL"
        ),
    )
    id_agregado = await asignador_artista.crear_indice(datos_artista)
    return id_agregado


async def generar_actores_pelicula(
    id_base: ID_PELICULA_BASE,
    id_tmdb: ID_PELICULA_TMDB,
    cliente_http: AsyncClient,
    asignador_rol_base: AsignadorIndices,
    asignador_artista: AsignadorIndices,
) -> AsyncIterator[INFORMACION_INVOLUCRADO_PELICULA]:
    json_datos = await dict_involucrados_pelicula(id_tmdb, cliente_http)
    rol_actor = await asignador_rol_base.crear_indice(("Actor",))
    for artista_cast in sample(json_datos["cast"], 5):
        id_artista_tmdb: int = artista_cast["id"]
        id_artista_agregado = await agregar_artista_base(
            id_artista_tmdb, cliente_http, asignador_artista
        )
        yield (id_artista_agregado, rol_actor, id_base)


async def generar_insert_involucrado_pelicula(
    datos_artista: INFORMACION_INVOLUCRADO_PELICULA, archivo_output: Path
) -> tuple[INFORMACION_INVOLUCRADO_PELICULA, Path]:
    async with aiofiles.open(archivo_output, "a") as sql:
        await sql.write(
            f"""insert into involucrado_pelicula(id_artista, id_rol, id_pelicula)
values ({datos_artista[0]}, {datos_artista[1]}, {datos_artista[2]});\n"""
        )
    return (datos_artista, archivo_output)
