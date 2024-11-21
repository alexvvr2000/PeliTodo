from json import loads
from typing import Any

from async_lru import alru_cache
from httpx import AsyncClient
from pelis.typos import ID_PELICULA_TMDB
from pelis.utils import get_docker_secret

URL_TMDB = "https://api.themoviedb.org/3"
CLAVE_TMDB = get_docker_secret(secreto="tmdb")


@alru_cache
async def dict_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> dict[str, Any]:
    datos_pelicula = await cliente_http.get(
        url=f"{URL_TMDB}/movie/{id_pelicula}", params={"api_key": CLAVE_TMDB}
    )
    json_datos = loads(datos_pelicula.text)
    return json_datos


@alru_cache
async def dict_traducciones_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> dict[str, Any]:
    datos_pelicula = await cliente_http.get(
        url=f"{URL_TMDB}/movie/{id_pelicula}/translations",
        params={"api_key": CLAVE_TMDB},
    )
    json_datos = loads(datos_pelicula.text)
    return json_datos


@alru_cache
async def dict_imagenes_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> dict[str, Any]:
    datos_pelicula = await cliente_http.get(
        url=f"{URL_TMDB}/movie/{id_pelicula}/images",
        params={"api_key": CLAVE_TMDB},
    )
    json_datos = loads(datos_pelicula.text)
    return json_datos


@alru_cache
async def dict_involucrados_pelicula(
    id_pelicula: ID_PELICULA_TMDB, cliente_http: AsyncClient
) -> dict[str, Any]:
    datos_pelicula = await cliente_http.get(
        url=f"{URL_TMDB}/movie/{id_pelicula}/credits",
        params={"api_key": CLAVE_TMDB},
    )
    json_datos = loads(datos_pelicula.text)
    return json_datos


@alru_cache
async def dict_perfil_artista(
    id_artista_tmdb: int, cliente_http: AsyncClient
) -> dict[str, Any]:
    datos_pelicula = await cliente_http.get(
        url=f"{URL_TMDB}/person/{id_artista_tmdb}",
        params={"api_key": CLAVE_TMDB},
    )
    json_datos = loads(datos_pelicula.text)
    return json_datos
