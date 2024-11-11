from dataclasses import dataclass
from pathlib import Path

from dataclass_wizard import JSONWizard
from dataclass_wizard.wizard_mixins import JSONFileWizard


@dataclass
class ArchivoPeliculas(JSONWizard, JSONFileWizard):
    peliculas: list[str]


def get_docker_secret(secreto: str, default: str = "") -> str:
    ubicacion = Path(f"/run/secrets/{secreto}")
    if not ubicacion.exists():
        return default
    valor_secreto: str = ""
    with open(ubicacion, "r") as archivo_secreto:
        valor_secreto = archivo_secreto.read().rstrip("\n")
    return valor_secreto


PATH_ARCHIVO_DATOS = Path("/datos/peliculas.json")
peliculas_introducidas = ArchivoPeliculas.from_json_file(str(PATH_ARCHIVO_DATOS))
