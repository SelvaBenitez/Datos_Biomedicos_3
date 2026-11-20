import csv
import json
from pathlib import Path
from sistema import registrar_log, crear_carpetas, organizar_archivos
from generador import generar_registros, ordenar_por_fc
from validacion import filtrar_validos

CAMPOS = ["id", "fr", "fc", "spo2"]

def guardar_txt(registros, nombre="registros.txt"):
    try:
        with open(nombre, "w", encoding="utf-8") as f:
            for r in registros:
                f.write(f"{r['id']} | {r['fr']} | {r['fc']} | {r['spo2']}\n")
        registrar_log(f"Datos guardados en {nombre}")
    except OSError as e:
        print(f"Error al guardar TXT: {e}")
        registrar_log(f"ERROR al guardar {nombre}: {e}")

def guardar_csv(registros, nombre="registros.csv"):
    try:
        with open(nombre, "w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(registros)
        registrar_log(f"Datos guardados en {nombre}")
    except OSError as e:
        print(f"Error al guardar CSV: {e}")
        registrar_log(f"ERROR al guardar {nombre}: {e}")

def exportar_json(registros, nombre="registros.json"):
    try:
        with open(nombre, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=4)
        registrar_log(f"Datos exportados a {nombre}")
    except OSError as e:
        print(f"Error al exportar JSON: {e}")
        registrar_log(f"ERROR al exportar {nombre}: {e}")

def importar_json(ruta="data/json/registros.json"):
    ruta = Path(ruta)
    if not ruta.exists():
        print(f"No existe el archivo: {ruta}")
        registrar_log(f"ERROR: no se encontró {ruta}")
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            registros = json.load(f)
        registrar_log(f"Datos importados desde {ruta}")
        return registros
    except json.JSONDecodeError:
        print("El archivo JSON está dañado")
        registrar_log(f"ERROR: JSON inválido en {ruta}")
        return []

if __name__ == "__main__":
    crear_carpetas()
    datos = filtrar_validos(ordenar_por_fc(generar_registros()))
    guardar_txt(datos)
    guardar_csv(datos)
    exportar_json(datos)
    organizar_archivos()
    importados = importar_json()
    print(f"Se importaron {len(importados)} registros")