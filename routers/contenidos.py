from fastapi import APIRouter, Request, Depends # <-- Agregado Depends
from typing import List, Optional # <-- Agregado Optional
from schemas.contenido import ContenidoOut, TipoContenido # <-- Agregado TipoContenido
from services.contenidos_service import obtener_contenidos
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse # <-- Agregado RedirectResponse


# Suponiendo que tu función de autenticación está aquí o en un archivo auth.auth_utils
# Asegúrate de que la ruta de importación sea correcta según tu estructura de proyecto


router = APIRouter()
templates = Jinja2Templates(directory="templates")



@router.get("/contenido", response_class=HTMLResponse)
async def mostrar_contenidos(
    request: Request,
    tipo: Optional[TipoContenido] = TipoContenido.todos # Aquí está el cambio clave para el filtro
):


    # Llama a tu servicio para obtener los contenidos, pasándole el tipo de filtro
    # Asume que obtener_contenidos ahora puede recibir un parámetro 'tipo_filtro'
    contenidos: List[ContenidoOut] = obtener_contenidos(tipo_filtro=tipo)


    # Nota: La indentación en esta línea es importante. Debe estar al mismo nivel que 'contenidos = ...'
    return templates.TemplateResponse("contenido.html", {
        "request": request,
        "contenidos": contenidos,
        "tipo_seleccionado": tipo.value # Pasa el valor string del Enum a la plantilla
        # Si tienes 'username' o 'user_id' en tu plantilla, no los estás pasando aquí.
        # Por ejemplo, podrías hacer:
        # "username": request.state.user_payload.get("username", "Usuario")
    })
