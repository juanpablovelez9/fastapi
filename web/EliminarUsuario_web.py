# routers/admin_routes.py (o donde tengas tus rutas de administración)

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
# Asegúrate de importar la función de eliminación de tu servicio
from services.usuarios_service import eliminar_usuario_por_id 
# Importa la dependencia de rol si solo los admins pueden eliminar
#from auth.auth_utils import rol_requerido 

router = APIRouter()

# --- Endpoint para eliminar un usuario ---
# Usamos POST porque es una acción que modifica el estado del servidor
@router.post("/admin/eliminarusuario/{user_id}", status_code=status.HTTP_302_FOUND)
async def eliminar_usuario(
    user_id: int, # El ID del usuario a eliminar vendrá de la URL
    request: Request,
    # Protege esta ruta: solo administradores pueden eliminar usuarios
   # _ = Depends(rol_requerido("admin")) 
):
    try:
        # Llama a tu función de servicio para eliminar el usuario
        mensaje = eliminar_usuario_por_id(user_id)
        
        # Redirige de vuelta a la lista de usuarios con un mensaje de éxito
        response = RedirectResponse(
            url=f"/admin/listarusuarios?success={mensaje}", 
            status_code=status.HTTP_302_FOUND # Redirección exitosa
        )
        return response
    except HTTPException as e:
        # Si tu servicio lanza una HTTPException (ej. usuario no encontrado)
        # Redirige con un mensaje de error
        response = RedirectResponse(
            url=f"/admin/listarusuarios?error={e.detail}", 
            status_code=status.HTTP_302_FOUND
        )
        return response
    except Exception as e:
        # Para cualquier otro error inesperado
        print(f"Error al eliminar usuario con ID {user_id}: {e}") # Para depuración
        response = RedirectResponse(
            url="/admin/listarusuarios?error=Error+inesperado+al+eliminar+el+usuario.", 
            status_code=status.HTTP_302_FOUND
        )
        return response