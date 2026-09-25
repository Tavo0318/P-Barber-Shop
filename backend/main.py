import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Cargar variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Comprobar que exista la conexión
if not DATABASE_URL:
    raise RuntimeError(
        "No se encontró DATABASE_URL en el archivo .env"
    )


# Crear aplicación
app = FastAPI(
    title="P-Barber Shop API",
    description="API para gestionar las citas de P-Barber Shop",
    version="1.0.0"
)


# Permitir que nuestra página web se comunique con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# MODELO DE UNA CITA
# ==========================================

class Cita(BaseModel):
    nombre: str
    telefono: str
    servicio: str
    fecha: str
    hora: str


# ==========================================
# RUTA DE PRUEBA
# ==========================================

@app.get("/")
def inicio():
    return {
        "mensaje": "P-Barber Shop API funcionando 💈"
    }


# ==========================================
# CREAR UNA CITA
# ==========================================

@app.post("/citas")
def crear_cita(cita: Cita):

    try:

        with psycopg.connect(DATABASE_URL) as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO citas
                    (
                        nombre,
                        telefono,
                        servicio,
                        fecha,
                        hora
                    )
                    VALUES
                    (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        cita.nombre,
                        cita.telefono,
                        cita.servicio,
                        cita.fecha,
                        cita.hora
                    )
                )

                cita_id = cursor.fetchone()[0]

                conexion.commit()


        return {
            "mensaje": "Cita registrada correctamente",
            "id": cita_id,
            "cita": cita
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar la cita: {error}"
        )