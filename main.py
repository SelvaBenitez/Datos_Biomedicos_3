from generador import generar_registros, ordenar_por_fc
from validacion import validar_registro, filtrar_validos
from archivos import guardar_txt, guardar_csv, exportar_json, importar_json
from sistema import crear_carpetas, organizar_archivos, registrar_log
from mongodb import conectar_mongo, insertar_registros, calcular_promedio_fc
from mongodb import buscar_spo2_bajo, buscar_por_id, exportar_resultados


def mostrar_menu():
    print("\nSISTEMA DE SIGNOS VITALES")
    print("1. Generar registros aleatorios")
    print("2. Ingresar un registro manualmente")
    print("3. Validar datos")
    print("4. Exportar archivos (TXT, CSV, JSON)")
    print("5. Importar archivo JSON")
    print("6. Subir a MongoDB y hacer consultas")
    print("7. Buscar registro por ID en MongoDB")
    print("0. Salir")


crear_carpetas()
lista_registros = []

while True:
    mostrar_menu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        lista_registros = ordenar_por_fc(generar_registros(50))
        print(f"Se generaron {len(lista_registros)} registros ordenados por FC")
        registrar_log("Se generaron registros aleatorios")

    elif opcion == "2":
        id_paciente = input("ID (ejemplo ID-051): ").upper()
        edad = input("Edad: ")
        frecuencia = input("Frecuencia cardiaca (ejemplo 90): ")
        saturacion = input("SpO2 (ejemplo 95): ")
        nuevo_registro = {
            "id": id_paciente,
            "fr": edad + " Años",
            "fc": frecuencia.zfill(3) + "ppm",
            "spo2": saturacion + "%"
        }
        if validar_registro(nuevo_registro):
            lista_registros.append(nuevo_registro)
            lista_registros = ordenar_por_fc(lista_registros)
            print("Registro agregado correctamente")
            registrar_log(f"Registro ingresado manualmente: {nuevo_registro['id']}")
        else:
            print("No se pudo registrar el usuario. Por favor, verificar la digitación de la información.")

    elif opcion == "3":
        registros_validos = filtrar_validos(lista_registros)
        print(f"{len(registros_validos)} de {len(lista_registros)} registros son válidos")
        registrar_log("Se validaron los registros")

    elif opcion == "4":
        if len(lista_registros) == 0:
            print("Primero debes generar o importar registros")
        else:
            guardar_txt(lista_registros)
            guardar_csv(lista_registros)
            exportar_json(lista_registros)
            organizar_archivos()
            print("Archivos guardados en la carpeta data/")

    elif opcion == "5":
        lista_registros = importar_json()
        print(f"Se importaron {len(lista_registros)} registros")

    elif opcion == "6":
        if len(lista_registros) == 0:
            print("Primero genera o importa registros")
        else:
            coleccion_signos = conectar_mongo()
            if coleccion_signos is not None:
                insertar_registros(coleccion_signos, lista_registros)
                promedio_fc = calcular_promedio_fc(coleccion_signos)
                registros_spo2_bajo = buscar_spo2_bajo(coleccion_signos)
                exportar_resultados(promedio_fc, registros_spo2_bajo)
                organizar_archivos()
                print(f"Promedio de frecuencia cardiaca: {promedio_fc} ppm")
                print(f"Registros con SpO2 menor a 94: {len(registros_spo2_bajo)}")
                for registro in registros_spo2_bajo:
                    print(f"  {registro['id']} - SpO2: {registro['spo2']}")

    elif opcion == "7":
        coleccion_signos = conectar_mongo()
        if coleccion_signos is not None:
            id_buscado = input("Escribe el ID a buscar (ejemplo ID-005): ").upper()
            registro_encontrado = buscar_por_id(coleccion_signos, id_buscado)
            if registro_encontrado is not None:
                print("Registro encontrado:")
                print(f"  ID: {registro_encontrado['id']}")
                print(f"  Edad: {registro_encontrado['fr']}")
                print(f"  Frecuencia cardiaca: {registro_encontrado['fc']}")
                print(f"  SpO2: {registro_encontrado['spo2']}")
                registrar_log(f"Consulta en MongoDB por ID: {id_buscado}")
            else:
                print(f"No se encontró ningún registro con el ID {id_buscado}")

    elif opcion == "0":
        print("Saliendo del programa.")
        registrar_log("Programa finalizado")
        break

    else:
        print("No es una opción válida, intenta de nuevo")