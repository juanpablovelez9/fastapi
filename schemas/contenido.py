from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date

class TipoContenido(str, Enum):
    pelicula = 'pelicula'
    serie = 'serie'

class ContenidoOut(BaseModel):
    titulo: str
    descripcion: Optional[str]
    fecha_lanzamiento: Optional[str]
    tipo_contenido: str
    duracion: Optional[int] = None

class ContenidoOut_serie(BaseModel):
    titulo: str
    descripcion: Optional[str]
    fecha_lanzamiento: Optional[str]
    tipo_contenido: str
    cantidad_temporadas: Optional[int] = None    

# Para devolver info del contenido
class ContenidoResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str    
    fecha_lanzamiento: date
    tipo_contenido:str