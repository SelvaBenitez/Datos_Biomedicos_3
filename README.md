# Sistema de Gestión de Signos Vitales

Taller 3 – Informática 1 (Unidades 3 y 4)
Universidad de Antioquia – Facultad de Ingeniería

**Selva Natalia Benítez Peláez**

## Descripción

Programa en Python que genera, valida, ordena y almacena registros biomédicos.
Guarda los datos en archivos TXT, CSV y JSON, organiza las carpetas de forma automática,
registra cada acción en un log y se conecta a MongoDB Atlas para hacer consultas.

Cada registro tiene estos campos:

| Campo | Significado | Formato |
|-------|-------------|---------|
| `id` | Identificación | `ID-001` |
| `fr` | Edad | `18 Años` |
| `fc` | Frecuencia cardiaca | `090ppm` |
| `spo2` | Saturación periférica de oxígeno | `95%` |


## Estructura del proyecto

```
Final-taller3/
├── data/
│   ├── txt/          # registros.txt
│   ├── csv/          # registros.csv
│   └── json/         # registros.json y resultados_mongo.json
├── generador.py      # Genera y ordena los registros
├── validacion.py     # Valida los campos con expresiones regulares
├── archivos.py       # Guarda en TXT/CSV y exporta/importa JSON
├── sistema.py        # Crea carpetas, mueve archivos y escribe el log
├── mongodb.py        # Conexión y consultas en MongoDB Atlas
├── main.py           # Menú principal
├── log.txt           # Registro de acciones
├── requirements.txt  # Librerías instaladas. (usar pip install -r requirements.txt para ejecutar)
└── README.md
```

## Descripción de cada módulo

### 1. `generador.py` – Procesamiento y ordenamiento
- Genera 50 registros aleatorios con el formato pedido.
- Ordena los registros por frecuencia cardiaca de menor a mayor con `sorted()`.

### 2. `archivos.py` – Gestión de archivos
- Guarda los datos ordenados en `.txt` y `.csv`.
- Exporta e importa los datos en `.json`.
- Usa `try/except` para manejar errores y verifica que las rutas existan con `Path.exists()`.

### 3. `sistema.py` – Herramientas del sistema
- Crea las carpetas `data/txt`, `data/csv` y `data/json` con `pathlib`.
- Mueve cada archivo a su carpeta según su extensión con `os.listdir()` y `Path.replace()`.
- Escribe en `log.txt` cada acción del programa con la fecha y la hora.

### 4. `validacion.py` – Expresiones regulares
Verifica que cada campo cumpla su patrón con `re.fullmatch()`:

| Campo | Patrón | Ejemplo válido |
|-------|--------|----------------|
| `id` | `ID-\d{3}` | `ID-001` |
| `fr` | `\d{1,3} Años` | `18 Años` |
| `fc` | `\d{3}ppm` | `090ppm` |
| `spo2` | `\d{1,3}%` | `95%` |

### 5. `mongodb.py` 
- Se conecta a **MongoDB Atlas** con `pymongo`.
- Usa la colección `signos_vitales`.
- Inserta solo los registros validados.
- Consultas:
  - **Promedio de frecuencia cardiaca**, con `aggregate` y `$avg`.
  - **Documentos con SpO2 menor a 94**, con `find` y `$lt`.
  - **Búsqueda por ID**, con `find_one`.
- Exporta los resultados a `resultados_mongo.json`.

Para poder calcular con números, al insertar se agregan los campos `fc_numero` y `spo2_numero`
(por ejemplo, `"090ppm"` se guarda también como `90`).

### 6. `main.py` – Integración del sistema
Menú con las opciones:
1. Generar registros aleatorios
2. Ingresar un registro manualmente (con validación)
3. Validar datos
4. Exportar archivos (TXT, CSV, JSON)
5. Importar archivo JSON
6. Subir a MongoDB y hacer consultas
7. Buscar registro por ID en MongoDB
0. Salir

## Instalación y uso

1. Clonar el repositorio:
   ```
   git clone https://github.com/SelvaBenitez/Datos_Biomedicos_3.git
   cd Datos_Biomedicos_3
   ```

2. Crear y activar el entorno virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instalar las librerías:
   ```
   pip install -r requirements.txt
   ```

4. Crear un archivo `.env` en la carpeta principal con la cadena de conexión de MongoDB Atlas:
   ```
   MONGO_URI=mongodb+srv://usuario:contraseña@cluster0.xxxxx.mongodb.net/
   ```
   > El archivo `.env` no lo subo al repositorio porque contiene la contraseña.

5. Ejecutar el programa:
   ```
   python main.py
   ```

## Tecnologías utilizadas
- Python 3
- Librerías estándar: `random`, `re`, `os`, `pathlib`, `csv`, `json`, `datetime`
- `pymongo` – conexión con MongoDB
- `python-dotenv` – lectura del archivo `.env`
- MongoDB Atlas
- Git y GitHub