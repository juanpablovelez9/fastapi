from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Literal
from enum import Enum

class TipoContenido(str, Enum):
    pelicula = 'pelicula'
    serie = 'serie'
    todos = 'todos'

class ContenidoOut(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    fecha_lanzamiento: date
    tipo_contenido: TipoContenido
    imagen_url: Optional[str]
    trailer_url: Optional[str]

# --- Modelo Base para la Creación de Contenido (Campos Comunes) ---
class ContenidoBaseCreate(BaseModel):
    """Modelo base con campos comunes para crear contenido (película o serie)."""
    titulo: str 
    descripcion: Optional[str] 
    fecha_lanzamiento: date
    imagen_url: Optional[str] 
    trailer_url: Optional[str] 

    # --- Modelo para Crear una Película ---
class ContenidoCreatePelicula(ContenidoBaseCreate):
    """Modelo de entrada para crear una nueva película."""
    # 'Literal' fuerza que el valor de tipo_contenido sea exactamente 'pelicula' para este modelo
    tipo_contenido: Literal[TipoContenido.pelicula] = TipoContenido.pelicula
    duracion_minutos: int 

# --- Modelo para Crear una Serie ---
class ContenidoCreateSerie(ContenidoBaseCreate):
    """Modelo de entrada para crear una nueva serie."""
    # 'Literal' fuerza que el valor de tipo_contenido sea exactamente 'serie' para este modelo
    tipo_contenido: Literal[TipoContenido.serie] = TipoContenido.serie
    cantidad_temporadas: int 
# --- Modelos de Respuesta (para cuando la DB devuelve datos) ---
# Estos son útiles si quieres retornar los datos creados con un ID, por ejemplo.
class ContenidoBaseResponse(ContenidoBaseCreate):
    id: int 

class PeliculaResponse(ContenidoBaseResponse):
    tipo_contenido: TipoContenido = TipoContenido.pelicula
    duracion_minutos: int

class SerieResponse(ContenidoBaseResponse):
    tipo_contenido: TipoContenido = TipoContenido.serie
    cantidad_temporadas: int
# --- Modelo de Salida General (para listar contenidos) ---

    
