from typing import Tuple, TypedDict, TypeVar

ID_PELICULA_TMDB = str
ID_PELICULA_BASE = int
ID_LENGUAJE_BASE = str
ID_IDIOMA_BASE = str
ID_GENERO_BASE = int
ID_ROL_ARTISTA_BASE = int
ID_ARTISTA_BASE = int

INFORMACION_PELICULA = Tuple[str, str, int]
INFORMACION_GENERO = Tuple[ID_GENERO_BASE, str]
INFORMACION_URL_IMAGEN = Tuple[str, str]
INFORMACION_TITULO_PELICULA = Tuple[ID_IDIOMA_BASE, str]
INFORMACION_ROL_BASE = Tuple[str]
INFORMACION_ARTISTA_BASE = Tuple[str, str, str]
INFORMACION_INVOLUCRADO_PELICULA = Tuple[
    ID_ARTISTA_BASE, ID_ROL_ARTISTA_BASE, ID_PELICULA_BASE
]

ValorIndexableSQL = TypeVar("ValorIndexableSQL", bound=Tuple)


class DiccionarioGeneroApi(TypedDict):
    id: int
    name: str
