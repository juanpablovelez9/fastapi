# routers/user_routes.py (o routers/admin_routes.py si prefieres)

from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

# Importa tu servicio para crear usuarios
from services.usuarios_service import crear_usuario
# Importa tu esquema de usuario para el formulario (UserCreate)
from schemas.user import UserCreate 

# Si quieres que solo los admins puedan crear usuarios, importa tu dependencia de rol:
#from auth.auth_utils import rol_requerido # Asumiendo que tienes esta dependencia

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- Endpoint para mostrar el formulario de creación de usuario ---
@router.get("/admin/usuarios", response_class=HTMLResponse)
async def crear_usuario_form(
    request: Request,
    # Puedes proteger esta ruta si solo los admins deben acceder al formulario
   # _ = Depends(rol_requerido("admin")) 
):
    return templates.TemplateResponse("admin/usuarios.html", {
        "request": request,
        "title": "Crear Nuevo Usuario",
        "error": None,
        "success": None
    })

# --- Endpoint para procesar el envío del formulario ---
@router.post("/admin/usuarios", response_class=HTMLResponse)
async def crear_usuario_submit(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    contrasena: str = Form(...),
    rol:str=Form(...),
    # Protección de la ruta, si aplica
    #_ = Depends(rol_requerido("admin"))
):
    try:
        # Crea una instancia de UserCreate con los datos del formulario
        nuevo_usuario_data = UserCreate(
            nombre=nombre,
            email=email,
            contrasena=contrasena,
            rol=rol
        )
        
        # Llama a tu función de servicio para crear el usuario en la DB
        usuario_creado = crear_usuario(nuevo_usuario_data)
        
        # Redirigir o mostrar mensaje de éxito
        # Opción 1: Redirigir a la lista de usuarios con un mensaje de éxito
        response = RedirectResponse(url="/admin/usuarios?success=Usuario+creado+exitosamente", status_code=status.HTTP_302_FOUND)
        return response

        # Opción 2: Mantenerse en la misma página y mostrar un mensaje de éxito
        # return templates.TemplateResponse("admin/crear_usuario.html", {
        #     "request": request,
        #     "title": "Crear Nuevo Usuario",
        #     "error": None,
        #     "success": f"Usuario '{usuario_creado.nombre}' creado con ID: {usuario_creado.id}"
        # })

    except HTTPException as e:
        # Si tu servicio lanza HTTPException (ej. para email duplicado)
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "title": "Crear Nuevo Usuario",
            "error": e.detail,
            "nombre": nombre,
            "email": email
        })
    except Exception as e:
        # Para cualquier otro error inesperado
        print(f"Error al crear usuario: {e}") # Imprime el error para depuración
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "title": "Crear Nuevo Usuario",
            "error": "Ocurrió un error inesperado al crear el usuario.",
            "nombre": nombre,
            "email": email,
            "rol":rol,
        })