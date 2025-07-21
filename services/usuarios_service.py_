from database.connection import ConnectionFactory
from schemas.user import UserResponse, UserCreate


def obtener_usuarios(skip: int = 0, limit: int = 100):
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
                    SELECT id, nombre, email
                    FROM usuarios
                    ORDER BY id
                    OFFSET ? ROWS
                    FETCH NEXT ? ROWS ONLY
                    """,
        (skip, limit),
    )
    rows = cursor.fetchall()
    return [
        UserResponse(
            id=row[0],
            nombre=row[1],
            email=row[2],
        )
        for row in rows
    ]


def crear_usuario(usuario: UserCreate) -> UserResponse:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nombre, email, contrasena)
        OUTPUT INSERTED.id, INSERTED.nombre, INSERTED.email
        VALUES (?, ?, ?)
    """, (usuario.nombre, usuario.email, usuario.contrasena))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()

    return UserResponse(
        id=row.id,
        nombre=row.nombre,
        email=row.email
    )

def obtener_usuario_por_id(usuario_id: int) -> UserResponse | None:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, nombre, email
        FROM usuarios
        WHERE id = ?
        """,
        (usuario_id,)
    )
    row = cursor.fetchone()
    conn.close()
 
    if row:
        return UserResponse(id=row[0], nombre=row[1], email=row[2])
    return None


def eliminar_usuario_por_id(usuario_id: int) -> str:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()    
    cursor.close()
    conn.close()
    
    return "Usuario eliminado correctamente"


def obtener_usuario_por_Email(usuario_email: str) -> UserResponse | None:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, nombre, email
        FROM usuarios
        WHERE email = ?
        """,
        (usuario_email,)
    )
    row = cursor.fetchone()
    conn.close()
 
    if row:
        return UserResponse(id=row[0], nombre=row[1], email=row[2])
    return None

def autenticar_usuario(email: str, password: str):
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, nombre, email, rol
    FROM usuarios
    WHERE email = ? AND contrasena = ?
    """

    cursor.execute(query, (email, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        print("Encuentro usuario")
        print(row.id)
        return {
            "id": row.id,
            "username": row.nombre,
            "email": row.email,
            "rol": row.rol
        }
    
    return None