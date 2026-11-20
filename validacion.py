import re

PATRONES = {
    "id": r"ID-\d{3}",
    "fr": r"\d{1,3} Años",
    "fc": r"\d{3}ppm",
    "spo2": r"\d{1,3}%"
}

def validar_registro(registro):
    for campo, patron in PATRONES.items():
        valor = str(registro.get(campo, ""))
        if not re.fullmatch(patron, valor):
            print(f"Registro inválido: {campo} = '{valor}'")
            return False
    return True

def filtrar_validos(registros):
    return [r for r in registros if validar_registro(r)]

if __name__ == "__main__":
    bueno = {"id": "ID-001", "fr": "18 Años", "fc": "090ppm", "spo2": "95%"}
    malo = {"id": "ID1", "fr": "18", "fc": "90", "spo2": "95"}
    print(validar_registro(bueno))
    print(validar_registro(malo))