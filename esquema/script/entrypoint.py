from asyncio import TaskGroup, run
from dataclasses import dataclass
from pathlib import Path
from time import time

from dataclass_wizard import JSONWizard
from dataclass_wizard.wizard_mixins import JSONFileWizard
from httpx import AsyncClient
from pelis.idiomas import (ARCHIVO_IDIOMAS, ARCHIVO_PAISES,
                           creacion_insert_idiomas, creacion_insert_paises,
                           idiomas_insert, paises_insert)
from pelis.peliculas import (agregar_genero_pelicula, agregar_imagen_pelicula,
                             agregar_lenguaje_pelicula, agregar_pelicula,
                             agregar_titulo_pelicula, generar_actores_pelicula,
                             generar_insert_involucrado_pelicula,
                             generos_pelicula, imagenes_pelicula,
                             informacion_pelicula, lenguajes_pelicula,
                             titulos_pelicula)
from pelis.typos import INFORMACION_ARTISTA_BASE, INFORMACION_ROL_BASE
from pelis.utils import AsignadorIndices

ARCHIVO_PELICULAS = Path("/output/08.01.b_pelicula_insert.sql")
ARCHIVO_IMAGENES_PELICULA = Path("/output/08.02.b_imagen_pelicula_insert.sql")
ARCHIVO_LENGUAJES_PELICULA = Path("/output/08.03.b_lenguajes_pelicula_insert.sql")
ARCHIVO_TITULOS_PELICULA = Path("/output/08.04.b_titulos_pelicula_insert.sql")
ARCHIVO_GENEROS_BASE = Path("/output/09.01.b_generos_base.sql")
ARCHIVO_GENEROS_PELICULA = Path("/output/09.02.b_genero_pelicula.sql")
ARCHIVO_ARTISTA_BASE = Path("/output/10.01.b_artista_base.sql")
ARCHIVO_ROL_BASE = Path("/output/10.02.b_rol_base.sql")
ARCHIVO_INVOLUCRADO_PELICULA = Path("/output/10.03.b_involucrado_pelicula.sql")
JSON_PELICULAS = Path("/datos/peliculas.json")

asignador_rol_base = AsignadorIndices[INFORMACION_ROL_BASE](
    formato_insert='insert into rol_artista(id_rol, descripcion) values ({}, "{}");\n',
    ruta_archivo=ARCHIVO_ROL_BASE,
)
asignador_artista = AsignadorIndices[INFORMACION_ARTISTA_BASE](
    formato_insert="""
insert into artista(id_artista, nombre, fecha_nacimiento, fecha_deceso)
values ({}, "{}", {}, {});\n""",
    ruta_archivo=ARCHIVO_ARTISTA_BASE,
)
asignador_genero = AsignadorIndices[tuple[str]](
    """insert into genero(id_genero, descripcion) values ({}, "{}");\n""",
    ARCHIVO_GENEROS_BASE,
)


@dataclass
class ArchivoPeliculas(JSONWizard, JSONFileWizard):
    peliculas: list[str]


async def inserts_wikipedia() -> float:
    start_time = time()
    async with TaskGroup() as tareas_http:
        for idioma in idiomas_insert():
            print(idioma)
            tareas_http.create_task(creacion_insert_idiomas(idioma, ARCHIVO_IDIOMAS))
        for pais in paises_insert():
            print(pais)
            tareas_http.create_task(creacion_insert_paises(pais, ARCHIVO_PAISES))
    elapsed_time = time() - start_time
    return elapsed_time


async def inserts_peliculas() -> float:
    peliculas_json = ArchivoPeliculas.from_json_file(str(JSON_PELICULAS))
    start_time = time()
    async with TaskGroup() as tareas_tablas_peliculas:
        async with AsyncClient() as cliente_http:
            for index, id_tmdb in enumerate(peliculas_json.peliculas):
                id_base_actual = index + 1
                datos_pelicula = await informacion_pelicula(id_tmdb, cliente_http)
                tareas_tablas_peliculas.create_task(
                    agregar_pelicula(id_base_actual, datos_pelicula, ARCHIVO_PELICULAS)
                )
                async for lenguaje_pelicula in lenguajes_pelicula(
                    id_tmdb, cliente_http
                ):
                    tareas_tablas_peliculas.create_task(
                        agregar_lenguaje_pelicula(
                            id_base_actual,
                            lenguaje_pelicula,
                            ARCHIVO_LENGUAJES_PELICULA,
                        )
                    )
                    print(lenguaje_pelicula)
                async for titulo in titulos_pelicula(id_tmdb, cliente_http):
                    tareas_tablas_peliculas.create_task(
                        agregar_titulo_pelicula(
                            id_base_actual, titulo, ARCHIVO_TITULOS_PELICULA
                        )
                    )
                    print(titulo)
                async for imagen_pelicula in imagenes_pelicula(id_tmdb, cliente_http):
                    tareas_tablas_peliculas.create_task(
                        agregar_imagen_pelicula(
                            id_base_actual, imagen_pelicula, ARCHIVO_IMAGENES_PELICULA
                        )
                    )
                    print(imagen_pelicula)
                async for genero_pelicula in generos_pelicula(
                    id_tmdb, cliente_http, asignador_genero
                ):
                    archivo_genero_pelicula = agregar_genero_pelicula(
                        id_base_actual, ARCHIVO_GENEROS_PELICULA, genero_pelicula[0]
                    )
                    tareas_tablas_peliculas.create_task(archivo_genero_pelicula)
                    print(genero_pelicula)
                async for artista in generar_actores_pelicula(
                    id_base_actual,
                    id_tmdb,
                    cliente_http,
                    asignador_rol_base,
                    asignador_artista,
                ):
                    tareas_tablas_peliculas.create_task(
                        generar_insert_involucrado_pelicula(
                            artista, ARCHIVO_INVOLUCRADO_PELICULA
                        )
                    )
                    print(artista)
                print(id_tmdb)
            async for genero_insert in asignador_genero.crear_insert():
                print(genero_insert)
            async for rol_insert in asignador_rol_base.crear_insert():
                print(rol_insert)
            async for artista_insert in asignador_artista.crear_insert():
                print(artista_insert)
        elapsed_time = time() - start_time
        return elapsed_time


async def main() -> None:
    start_time = time()
    async with TaskGroup() as tareas_inserts:
        i_peliculas = tareas_inserts.create_task(inserts_peliculas())
        i_inserts = tareas_inserts.create_task(inserts_wikipedia())
    elapsed_time = time() - start_time
    print(
        f"Tiempo de ejecucion de inserts de peliculas: {i_peliculas.result()} segundos"
    )
    print(f"Tiempo de ejecucion de inserts de wikipedia: {i_inserts.result()} segundos")
    print(f"Tiempo de ejecucion total: {elapsed_time} segundos")


folder_output = Path("/output/")
archivos_generados = list(folder_output.glob("*.b*.sql"))

if len(archivos_generados) != 0:
    print("Archivos generados con anteriodidad")
    exit(0)
else:
    print("Generando archivos base...")
    run(main())
    exit(0)
