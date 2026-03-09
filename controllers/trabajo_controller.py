import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_PATH = os.path.join(BASE_DIR, "storage", "trabajos")


def guardar_archivo(ruta_original, nombre_cliente):
    """
    Copia el archivo al storage interno y lo renombra automáticamente.
    """

    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nombre_original = os.path.basename(ruta_original)
    extension = os.path.splitext(nombre_original)[1]

    nuevo_nombre = f"{fecha}_{nombre_cliente}{extension}"

    ruta_destino = os.path.join(STORAGE_PATH, nuevo_nombre)

    shutil.copy2(ruta_original, ruta_destino)

    return ruta_destino