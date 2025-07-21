from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.contenidos_service import obtener_contenidos


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/contenidos", response_class=HTMLResponse)
async def mostrar_contenidos(request: Request, tipo: str = Query(default="todos")):
    contenidos = obtener_contenidos()
    tipo = tipo.lower()
    if tipo != "todos":
        contenidos = [c for c in contenidos if c.tipo_contenido.lower() == tipo]

    return templates.TemplateResponse("contenidos.html", {
        "request": request,
        "contenidos": contenidos,
        "tipo_seleccionado": tipo
    })

