import random

def generar_registros(n=50):
    registros = []
    for i in range(1, n + 1):
        registros.append({
            "id": f"ID-{i:03d}",
            "fr": f"{random.randint(18, 90)} Años",
            "fc": f"{random.randint(50, 130):03d}ppm",
            "spo2": f"{random.randint(85, 100)}%"
        })
    return registros

def ordenar_por_fc(registros):
    return sorted(registros, key=lambda r: int(r["fc"][:3]))

if __name__ == "__main__":
    datos = ordenar_por_fc(generar_registros())
    for r in datos:
        print(r)