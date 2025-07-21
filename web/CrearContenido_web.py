# web/crear_contenido_web.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from datetime import date # Asegúrate de que esta importación esté presente

# --- Importaciones de tus modelos y servicios ---
from schemas.contenido import (
    ContenidoCreatePelicula,
    ContenidoCreateSerie,
    TipoContenido
)
from services.contenidos_service import crear_contenido

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- 1. Ruta GET para mostrar el formulario HTML ---
@router.get("/Crear_contenido", response_class=HTMLResponse)
async def mostrar_formulario_crear_contenido(request: Request, success: str = None, error: str = None):
    """Muestra el formulario HTML para crear un nuevo contenido (película o serie)."""
    return templates.TemplateResponse("crear_contenido.html", {
        "request": request,
        "success": success,
        "error": error
    })

# --- 2. Ruta POST para procesar el formulario HTML ---
@router.post("/Crear_contenido", response_class=RedirectResponse, status_code=303)
async def procesar_formulario_crear_contenido(request: Request):
    """
    Procesa los datos enviados desde el formulario HTML para crear
    una película o una serie en la base de datos.
    """
    form_data = await request.form()

    # Extracción de datos comunes
    titulo = form_data.get("titulo")
    descripcion = form_data.get("descripcion")
    fecha_lanzamiento_str = form_data.get("fecha_lanzamiento")
    tipo_contenido_str = form_data.get("tipo_contenido")
    imagen_url = form_data.get("imagen_url")
    trailer_url = form_data.get("trailer_url")

    # Obtiene la URL base de la ruta del formulario.
    # ¡Aquí NO pasamos los parámetros 'success' o 'error'!
    base_form_url = router.url_path_for("mostrar_formulario_crear_contenido")

    try:
        # Conversión de tipos de datos (¡fecha_lanzamiento debe ser un objeto date!)
        fecha_lanzamiento = date.fromisoformat(fecha_lanzamiento_str)
        tipo_contenido = TipoContenido(tipo_contenido_str)

        # Lógica condicional basada en el tipo de contenido
        if tipo_contenido == TipoContenido.pelicula:
            duracion_minutos = int(form_data.get("duracion_minutos"))
            contenido_a_crear = ContenidoCreatePelicula(
                titulo=titulo,
                descripcion=descripcion,
                fecha_lanzamiento=fecha_lanzamiento,
                tipo_contenido=tipo_contenido,
                imagen_url=imagen_url,
                trailer_url=trailer_url,
                duracion_minutos=duracion_minutos
            )
        elif tipo_contenido == TipoContenido.serie:
            cantidad_temporadas = int(form_data.get("cantidad_temporadas"))
            contenido_a_crear = ContenidoCreateSerie(
                titulo=titulo,
                descripcion=descripcion,
                fecha_lanzamiento=fecha_lanzamiento,
                tipo_contenido=tipo_contenido,
                imagen_url=imagen_url,
                trailer_url=trailer_url,
                cantidad_temporadas=cantidad_temporadas
            )
        else:
            raise ValueError("Tipo de contenido no válido.")

        # Llama a tu función de servicio
        crear_contenido(contenido_a_crear)

        # Redirige con mensaje de éxito, construyendo el query parameter manualmente
        return RedirectResponse(
            url=f"{base_form_url}?success=Contenido creado exitosamente.", # <--- ¡CAMBIO CLAVE AQUÍ!
            status_code=303
        )

    except ValidationError as e:
        error_messages = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
        print(f"Error de validación Pydantic: {error_messages}")
        # Redirige con mensaje de error
        return RedirectResponse(
            url=f"{base_form_url}?error=Error de validación: {error_messages}", # <--- ¡CAMBIO CLAVE AQUÍ!
            status_code=303
        )
    except (ValueError, TypeError) as e:
        print(f"Error de conversión de datos del formulario: {e}")
        # Redirige con mensaje de error
        return RedirectResponse(
            url=f"{base_form_url}?error=Error en los datos del formulario: {e}", # <--- ¡CAMBIO CLAVE AQUÍ!
            status_code=303
        )
    except Exception as e:
        print(f"Error inesperado al crear contenido: {e}")
        # Redirige con mensaje de error
        return RedirectResponse(
            url=f"{base_form_url}?error=Error al crear contenido: {e}", # <--- ¡CAMBIO CLAVE AQUÍ!
            status_code=303
        )