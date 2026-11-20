import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from sistema import registrar_log, organizar_archivos
from archivos import importar_json
from validacion import filtrar_validos

load_dotenv()
cadena_conexion = os.getenv("MONGO_URI")


def conectar_mongo():
    try:
        cliente_mongo = MongoClient(cadena_conexion)
        cliente_mongo.admin.command("ping")
        base_de_datos = cliente_mongo["taller3"]
        coleccion_signos = base_de_datos["signos_vitales"]
        print("Conexión exitosa a MongoDB")
        registrar_log("Conexión exitosa a MongoDB")
        return coleccion_signos
    except Exception as error:
        print("No se pudo conectar a MongoDB:", error)
        registrar_log("Error al conectar a MongoDB")
        return None


def insertar_registros(coleccion_signos, lista_registros):
    registros_validos = filtrar_validos(lista_registros)
    if len(registros_validos) == 0:
        print("No hay registros válidos para insertar")
        return
    for registro in registros_validos:
        registro["fc_numero"] = int(registro["fc"].replace("ppm", ""))
        registro["spo2_numero"] = int(registro["spo2"].replace("%", ""))
    coleccion_signos.delete_many({})
    coleccion_signos.insert_many(registros_validos)
    registrar_log(f"Se insertaron {len(registros_validos)} registros en MongoDB")


def calcular_promedio_fc(coleccion_signos):
    resultado = list(coleccion_signos.aggregate([
        {"$group": {"_id": None, "promedio_fc": {"$avg": "$fc_numero"}}}
    ]))
    promedio_fc = round(resultado[0]["promedio_fc"], 2)
    return promedio_fc


def buscar_spo2_bajo(coleccion_signos):
    filtro = {"spo2_numero": {"$lt": 94}}
    campos_a_mostrar = {"_id": 0}
    registros_spo2_bajo = list(coleccion_signos.find(filtro, campos_a_mostrar))
    return registros_spo2_bajo


def buscar_por_id(coleccion_signos, id_buscado):
    registro_encontrado = coleccion_signos.find_one({"id": id_buscado}, {"_id": 0})
    return registro_encontrado


def exportar_resultados(promedio_fc, registros_spo2_bajo):
    resultados = {
        "promedio_fc": promedio_fc,
        "spo2_menor_94": registros_spo2_bajo
    }
    with open("resultados_mongo.json", "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, ensure_ascii=False, indent=4)
    registrar_log("Resultados exportados a resultados_mongo.json")


if __name__ == "__main__":
    coleccion_signos = conectar_mongo()
    if coleccion_signos is not None:
        lista_registros = importar_json()
        insertar_registros(coleccion_signos, lista_registros)
        promedio_fc = calcular_promedio_fc(coleccion_signos)
        registros_spo2_bajo = buscar_spo2_bajo(coleccion_signos)
        exportar_resultados(promedio_fc, registros_spo2_bajo)
        organizar_archivos()
        print("Promedio de frecuencia cardiaca:", promedio_fc)
        print("Registros con SpO2 menor a 94:", len(registros_spo2_bajo))
        print("Búsqueda de ID-001:", buscar_por_id(coleccion_signos, "ID-001"))