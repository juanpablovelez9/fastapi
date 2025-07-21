from database.connection import ConnectionFactory
from schemas.contenido import ContenidoOut
from typing import Union
from datetime import date # Importa date para fecha_lanzamiento si no lo tienes


def obtener_contenidos():
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, fecha_lanzamiento, tipo_contenido,imagen_url,trailer_url FROM contenidos"
    )
    rows = cursor.fetchall()
    return [
        ContenidoOut(
            id=row[0],
            titulo=row[1],
            descripcion=row[2],
            fecha_lanzamiento=str(row[3]) if row[3] else None,
            tipo_contenido=row[4],
            imagen_url=row[5],
            trailer_url=row[6],
        )
        for row in rows
    ]



# Suponiendo que tus modelos Pydantic son algo así:
# Si no usas Pydantic, adapta esto a cómo defines tus estructuras de datos.

class ContenidoBase:
    titulo: str
    descripcion: str
    fecha_lanzamiento: date # O str, si lo manejas como string en la DB
    tipo_contenido: str
    imagen_url: str
    trailer_url: str

class ContenidoOut_Pelicula(ContenidoBase):
    duracion_minutos: int

class ContenidoOut_Serie(ContenidoBase):
    cantidad_temporadas: int

# Puedes usar un Union para la entrada de la función si manejas ambos tipos en una misma ruta
ContenidoIn = Union[ContenidoOut_Pelicula, ContenidoOut_Serie]

class ContenidoResponse:
    id: int
    titulo: str
    descripcion: str
    fecha_lanzamiento:  str
    tipo_contenido: str
    imagen_url: str
    trailer_url: str

# services/contenidos_service.py

# --- Importaciones Esenciales ---
# IMPORTA TODAS LAS CLASES PYDANTIC Y ENUMS DESDE TU ARCHIVO DE ESQUEMAS
from schemas.contenido import (
    ContenidoCreatePelicula,  # Modelo de entrada para crear película
    ContenidoCreateSerie,     # Modelo de entrada para crear serie
    PeliculaResponse,         # Modelo de respuesta para película creada
    SerieResponse,            # Modelo de respuesta para serie creada
    TipoContenido             # Enum para los tipos de contenido
)

# Importa tu ConnectionFactory (asegúrate de que la ruta sea correcta)
from database.connection import ConnectionFactory

from typing import Union
# No necesitas importar 'date' aquí si Pydantic ya maneja los tipos de fecha desde la DB.

# --- Definición de Uniones de Tipos (Tipo Sugerido) ---
# Esto permite que la función acepte tanto ContenidoCreatePelicula como ContenidoCreateSerie
ContenidoCreate = Union[ContenidoCreatePelicula, ContenidoCreateSerie]

# Esto permite que la función retorne tanto PeliculaResponse como SerieResponse
ContenidoResponseFull = Union[PeliculaResponse, SerieResponse]


def crear_contenido(contenido: ContenidoCreate) -> ContenidoResponseFull:
    """
    Crea un nuevo contenido (película o serie) en la base de datos.

    Args:
        contenido (ContenidoCreate): Objeto Pydantic con los datos del contenido.
                                     Puede ser ContenidoCreatePelicula o ContenidoCreateSerie.

    Returns:
        ContenidoResponseFull: Objeto Pydantic con los datos del contenido recién creado,
                               incluyendo su ID y campos específicos.

    Raises:
        Exception: Si ocurre un error durante la inserción en la base de datos.
    """
    conn = None
    cursor = None

    try:
        conn = ConnectionFactory.create_connection()
        cursor = conn.cursor()

        # 1. Insertar en la tabla 'contenidos'
        # Nota: 'contenido.tipo_contenido' es un Enum, usa '.value' para obtener su string.
        cursor.execute("""
            INSERT INTO contenidos (titulo, descripcion, fecha_lanzamiento, tipo_contenido, imagen_url, trailer_url)
            OUTPUT INSERTED.id, INSERTED.titulo, INSERTED.descripcion, INSERTED.fecha_lanzamiento, INSERTED.tipo_contenido, INSERTED.imagen_url, INSERTED.trailer_url
            VALUES (?, ?, ?, ?, ?, ?)
        """, (contenido.titulo, contenido.descripcion, contenido.fecha_lanzamiento, contenido.tipo_contenido.value,
              contenido.imagen_url, contenido.trailer_url))

        # Obtener los datos del contenido insertado, incluido el ID
        inserted_row = cursor.fetchone()
        if not inserted_row:
            raise Exception("No se pudo obtener el ID del contenido recién insertado.")

        contenido_id = inserted_row.id # Ya tienes el ID aquí

        # 2. Insertar en tablas específicas (peliculas o series) según el tipo
        # Usa 'is' para comparar miembros de Enum, es más robusto.
        if contenido.tipo_contenido is TipoContenido.pelicula:
            # Pydantic ya validó que 'duracion_minutos' existe y es el tipo correcto
            cursor.execute("""
                INSERT INTO peliculas (contenido_id, duracion_minutos)
                VALUES (?, ?)
            """, (contenido_id, contenido.duracion_minutos))

            # Crea el objeto de respuesta PeliculaResponse con todos los datos
            response_model = PeliculaResponse(
                id=inserted_row.id,
                titulo=inserted_row.titulo,
                descripcion=inserted_row.descripcion,
                fecha_lanzamiento=inserted_row.fecha_lanzamiento,
                tipo_contenido=TipoContenido(inserted_row.tipo_contenido), # Convierte a Enum
                imagen_url=inserted_row.imagen_url,
                trailer_url=inserted_row.trailer_url,
                duracion_minutos=contenido.duracion_minutos # Toma este valor del objeto de entrada
            )

        elif contenido.tipo_contenido is TipoContenido.serie:
            # Pydantic ya validó que 'cantidad_temporadas' existe y es el tipo correcto
            cursor.execute("""
                INSERT INTO series (contenido_id, cantidad_temporadas)
                VALUES (?, ?)
            """, (contenido_id, contenido.cantidad_temporadas))

            # Crea el objeto de respuesta SerieResponse con todos los datos
            response_model = SerieResponse(
                id=inserted_row.id,
                titulo=inserted_row.titulo,
                descripcion=inserted_row.descripcion,
                fecha_lanzamiento=inserted_row.fecha_lanzamiento,
                tipo_contenido=TipoContenido(inserted_row.tipo_contenido), # Convierte a Enum
                imagen_url=inserted_row.imagen_url,
                trailer_url=inserted_row.trailer_url,
                cantidad_temporadas=contenido.cantidad_temporadas # Toma este valor del objeto de entrada
            )

        else:
            # Esto se ejecuta si el tipo de contenido no es 'pelicula' ni 'serie'
            conn.rollback()
            raise ValueError(f"Tipo de contenido no soportado: {contenido.tipo_contenido.value if hasattr(contenido.tipo_contenido, 'value') else contenido.tipo_contenido}")

        # 3. Confirmar la transacción
        conn.commit()

        # 4. Retornar la respuesta con los datos del contenido creado
        return response_model

    except Exception as e:
        if conn:
            conn.rollback() # Solo intenta rollback si la conexión existe
        print(f"Error al crear contenido: {e}")
        raise e # Re-lanza la excepción para que el router web la capture y la muestre.

    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()