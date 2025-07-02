from fastapi import APIRouter
from typing import List
from schemas.contenido import ContenidoOut,ContenidoResponse,ContenidoOut_serie
from services.contenidos_service import obtener_contenidos,crear_contenidos_pelicula,crear_contenidos_serie

router = APIRouter()

@router.get("/contenidos", response_model=List[ContenidoOut])
def listar_contenidos():
    return obtener_contenidos()

@router.post("/contenidosSerie", response_model=ContenidoResponse, status_code=201)
async def crear_serie(contenido: ContenidoOut_serie):
    return crear_contenidos_serie(contenido)

@router.post("/contenidosPelicula", response_model=ContenidoResponse, status_code=201)
async def crear_pelicula(contenido: ContenidoOut):
    return crear_contenidos_pelicula(contenido)
