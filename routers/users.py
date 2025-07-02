from fastapi import APIRouter
from typing import List
from schemas.user import UserCreate, UserResponse
from services.usuarios_service import obtener_usuarios, crear_usuario,obtener_usuario_por_id,obtener_usuario_por_Email

router = APIRouter()

@router.get("/usuarios", response_model=List[UserResponse])
async def listar_usuarios(skip: int = 0, limit: int = 100):
    return obtener_usuarios(skip=skip, limit=limit)

@router.post("/usuarios", response_model=UserResponse, status_code=201)
async def crear(usuario: UserCreate):
    return crear_usuario(usuario)

@router.get("/Consulto_Usuario_ID/{usuario_id}", response_model=UserResponse)
async def consultar_usuario(usuario_id: int):
    usuario = obtener_usuario_por_id(usuario_id)
    return usuario

@router.get("/Consulto_Usuario_email/{usuario_email}", response_model=UserResponse)
async def consultar_usuario(usuario_email: str):
    usuario = obtener_usuario_por_Email(usuario_email)
    return usuario