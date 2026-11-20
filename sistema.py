import os
from pathlib import Path
from datetime import datetime

CARPETAS = {
    ".txt": Path("data/txt"),
    ".csv": Path("data/csv"),
    ".json": Path("data/json")
}
LOG = Path("log.txt")
NO_MOVER = ["log.txt", "requirements.txt"]

def registrar_log(mensaje):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{fecha}] {mensaje}\n")

def crear_carpetas():
    for carpeta in CARPETAS.values():
        carpeta.mkdir(parents=True, exist_ok=True)
    registrar_log("Estructura de carpetas creada")

def organizar_archivos():
    for nombre in os.listdir("."):
        extension = Path(nombre).suffix
        if extension in CARPETAS and nombre not in NO_MOVER:
            destino = CARPETAS[extension] / nombre
            Path(nombre).replace(destino)
            registrar_log(f"Archivo movido: {nombre} -> {destino}")

if __name__ == "__main__":
    crear_carpetas()
    Path("prueba.txt").write_text("hola", encoding="utf-8")
    organizar_archivos()
    print("Listo, revisa la carpeta data/ y el archivo log.txt")