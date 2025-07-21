# routers/admin_routes.py (o donde manejes las rutas de administración)

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Optional

# Importa tu servicio para obtener usuarios
from services.usuarios_service import obtener_usuarios
# Importa tu esquema UserResponse
from schemas.user import UserResponse 
# Importa tu dependencia de rol si quieres proteger la ruta
#from auth.auth_utils import rol_requerido # Asumiendo que tienes esta dependencia

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin/listarusuarios", response_class=HTMLResponse)
async def listar_usuarios(
    request: Request,
    # Protege esta ruta: solo administradores pueden ver la lista de usuarios
   # _ = Depends(rol_requerido("admin")), 
    skip: int = 0, # Parámetros para paginación si los quieres usar
    limit: int = 100
):
    try:
        # Obtiene la lista de usuarios usando tu función de servicio
        usuarios: List[UserResponse] = obtener_usuarios(skip=skip, limit=limit)
        
        # Puedes añadir un mensaje de éxito si vienes de crear/editar un usuario
        success_message = request.query_params.get("success")

        return templates.TemplateResponse("admin/listarusuarios.html", {
            "request": request,
            "title": "Lista de Usuarios",
            "usuarios": usuarios, # Aquí pasamos la lista de usuarios a la plantilla
            "success": success_message,
            "error": None
        })
    except Exception as e:
        print(f"Error al listar usuarios: {e}")
        return templates.TemplateResponse("admin/listar_usuarios.html", {
            "request": request,
            "title": "Lista de Usuarios",
            "usuarios": [], # Pasa una lista vacía en caso de error
            "error": "No se pudo cargar la lista de usuarios en este momento.",
            "success": None
        })