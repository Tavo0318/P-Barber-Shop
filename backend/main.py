import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ==========================================
# CARGAR VARIABLES DEL ARCHIVO .env
# ==========================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

ADMIN_USUARIO = os.getenv("ADMIN_USUARIO")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


# ==========================================
# COMPROBAR VARIABLES NECESARIAS
# ==========================================

if not DATABASE_URL:
    raise RuntimeError(
        "No se encontró DATABASE_URL en el archivo .env"
    )

if not ADMIN_USUARIO:
    raise RuntimeError(
        "No se encontró ADMIN_USUARIO en el archivo .env"
    )

if not ADMIN_PASSWORD:
    raise RuntimeError(
        "No se encontró ADMIN_PASSWORD en el archivo .env"
    )

if not ADMIN_TOKEN:
    raise RuntimeError(
        "No se encontró ADMIN_TOKEN en el archivo .env"
    )


# ==========================================
# CREAR APLICACIÓN
# ==========================================

app = FastAPI(
    title="P-Barber Shop API",
    description="API para gestionar las citas de P-Barber Shop",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

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
# MODELO DEL LOGIN
# ==========================================

class Login(BaseModel):
    usuario: str
    contraseña: str


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


# ==========================================
# LOGIN DEL ADMINISTRADOR
# ==========================================

@app.post("/admin/login")
def admin_login(datos: Login):

    if (
        datos.usuario != ADMIN_USUARIO
        or datos.contraseña != ADMIN_PASSWORD
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    return {
        "mensaje": "Inicio de sesión correcto",
        "token": ADMIN_TOKEN
    }


# ==========================================
# COMPROBAR TOKEN DEL ADMINISTRADOR
# ==========================================

def comprobar_admin(authorization: str | None):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="No autorizado"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Formato de autorización incorrecto"
        )

    token = authorization.replace("Bearer ", "", 1)

    if token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )


# ==========================================
# VER TODAS LAS CITAS
# ==========================================

@app.get("/admin/citas")
def obtener_citas(
    fecha: str | None = None,
    authorization: str | None = Header(default=None)
):

    comprobar_admin(authorization)

    try:

        with psycopg.connect(DATABASE_URL) as conexion:

            with conexion.cursor() as cursor:

                if fecha:

                    cursor.execute(
                        """
                        SELECT
                            id,
                            nombre,
                            telefono,
                            servicio,
                            fecha,
                            hora
                        FROM citas
                        WHERE fecha = %s
                        ORDER BY hora
                        """,
                        (fecha,)
                    )

                else:

                    cursor.execute(
                        """
                        SELECT
                            id,
                            nombre,
                            telefono,
                            servicio,
                            fecha,
                            hora
                        FROM citas
                        ORDER BY fecha, hora
                        """
                    )

                citas = cursor.fetchall()

        resultado = []

        for cita in citas:

            resultado.append(
                {
                    "id": cita[0],
                    "nombre": cita[1],
                    "telefono": cita[2],
                    "servicio": cita[3],
                    "fecha": str(cita[4]),
                    "hora": str(cita[5])
                }
            )

        return {
            "total": len(resultado),
            "citas": resultado
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar las citas: {error}"
        )


# ==========================================
# CANCELAR / ELIMINAR UNA CITA
# ==========================================

@app.delete("/admin/citas/{cita_id}")
def eliminar_cita(
    cita_id: int,
    authorization: str | None = Header(default=None)
):

    comprobar_admin(authorization)

    try:

        with psycopg.connect(DATABASE_URL) as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    DELETE FROM citas
                    WHERE id = %s
                    RETURNING id
                    """,
                    (cita_id,)
                )

                cita_eliminada = cursor.fetchone()

                if not cita_eliminada:
                    raise HTTPException(
                        status_code=404,
                        detail="La cita no existe"
                    )

                conexion.commit()

        return {
            "mensaje": "Cita cancelada correctamente",
            "id": cita_id
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Error al cancelar la cita: {error}"
        )