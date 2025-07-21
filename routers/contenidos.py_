from fastapi import APIRouter,Depends
from typing import List
from schemas.contenido import ContenidoOut,ContenidoResponse,ContenidoOut_serie
from services.contenidos_service import obtener_contenidos,crear_contenidos_pelicula,crear_contenidos_serie
from auth.deps import rol_requerido

router = APIRouter()

@router.get("/contenidos", response_model=List[ContenidoOut])
def listar_contenidos(_ =Depends(rol_requerido("admin"))):
    return obtener_contenidos()

@router.post("/contenidosSerie", response_model=ContenidoResponse, status_code=201)
async def crear_serie(contenido: ContenidoOut_serie,_ =Depends(rol_requerido("admin"))):
    return crear_contenidos_serie(contenido)

@router.post("/contenidosPelicula", response_model=ContenidoResponse, status_code=201)
async def crear_pelicula(contenido: ContenidoOut,_ =Depends(rol_requerido("admin"))):
    return crear_contenidos_pelicula(contenido)
