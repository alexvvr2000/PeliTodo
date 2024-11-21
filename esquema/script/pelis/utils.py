from asyncio import Lock
from pathlib import Path
from typing import Any, AsyncIterator, Generic

import aiofiles
from pelis.typos import ValorIndexableSQL


class AsignadorIndices(Generic[ValorIndexableSQL]):
    def __init__(self, formato_insert: str, ruta_archivo: Path) -> None:
        self._valores: dict[ValorIndexableSQL, int] = {}
        self._formato_insert = formato_insert
        self._ruta_salida_txt = ruta_archivo
        self._lock_valores = Lock()
        self._ultimo_indice_agregado = 0

    async def crear_indice(self, valor_nuevo: ValorIndexableSQL) -> int:
        async with self._lock_valores:
            self._ultimo_indice_agregado += 1
            if valor_nuevo in self._valores.keys():
                return self._valores[valor_nuevo]
            self._valores[valor_nuevo] = self._ultimo_indice_agregado
            return self._ultimo_indice_agregado

    async def crear_insert(self) -> AsyncIterator[tuple[ValorIndexableSQL, int, Path]]:
        for valor, indice in self._valores.items():
            async with aiofiles.open(self._ruta_salida_txt, "a") as sql:
                nuevo_insert = f"{self._formato_insert.format(indice, *valor)}"
                await sql.write(nuevo_insert)
                yield (valor, indice, self._ruta_salida_txt)


async def async_enumerate(
    async_iterable: AsyncIterator[Any], start: int = 0
) -> AsyncIterator[tuple[int, Any]]:
    index = start
    async for valor_iterable in async_iterable:
        yield index, valor_iterable
        index += 1


def get_docker_secret(secreto: str, default: str = "") -> str:
    ubicacion: Path = Path(f"/run/secrets/{secreto}")
    if not ubicacion.exists():
        return default
    valor_secreto: str = ""
    with open(ubicacion, "r") as archivo_secreto:
        valor_secreto = archivo_secreto.read().rstrip("\n")
    return valor_secreto
