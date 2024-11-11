from pathlib import Path


def get_docker_secret(secreto: str, default: str = "") -> str:
    ubicacion: Path = Path(f"/run/secrets/{secreto}")
    if not ubicacion.exists():
        return default
    valor_secreto: str = ""
    with open(ubicacion, "r") as archivo_secreto:
        valor_secreto = archivo_secreto.read().rstrip("\n")
    return valor_secreto
