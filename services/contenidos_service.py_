from database.connection import ConnectionFactory
from schemas.contenido import ContenidoOut,ContenidoResponse,ContenidoOut_serie

def obtener_contenidos():
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, fecha_lanzamiento, tipo_contenido FROM contenidos"
    )
    rows = cursor.fetchall()
    return [
        ContenidoOut(
            id=row[0],
            titulo=row[1],
            descripcion=row[2],
            fecha_lanzamiento=str(row[3]) if row[3] else None,
            tipo_contenido=row[4],
        )
        for row in rows
    ]

def crear_contenidos_pelicula(contenido: ContenidoOut) -> ContenidoResponse:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO contenidos (titulo,descripcion,fecha_lanzamiento,tipo_contenido)
            OUTPUT INSERTED.id,INSERTED.titulo, INSERTED.descripcion, INSERTED.fecha_lanzamiento,INSERTED.tipo_contenido
            VALUES (?, ?, ?,?)
        """, (contenido.titulo, contenido.descripcion, contenido.fecha_lanzamiento, contenido.tipo_contenido))
        
        row = cursor.fetchone()
        contenido_id = row.id

        # Insertar en peliculas si es tipo 'pelicula'
        if contenido.tipo_contenido.lower() == 'pelicula':
            cursor.execute("""
                INSERT INTO peliculas (contenido_id, duracion_minutos)
                VALUES (?, ?)
            """, (contenido_id, contenido.duracion))

        conn.commit()

        return ContenidoResponse(
            id=row.id,
            titulo=row.titulo,
            descripcion=row.descripcion,
            fecha_lanzamiento=row.fecha_lanzamiento,
            tipo_contenido=row.tipo_contenido
        )

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def crear_contenidos_serie(contenido: ContenidoOut_serie) -> ContenidoResponse:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO contenidos (titulo,descripcion,fecha_lanzamiento,tipo_contenido)
            OUTPUT INSERTED.id,INSERTED.titulo, INSERTED.descripcion, INSERTED.fecha_lanzamiento,INSERTED.tipo_contenido
            VALUES (?, ?, ?,?)
        """, (contenido.titulo, contenido.descripcion, contenido.fecha_lanzamiento, contenido.tipo_contenido))
        
        row = cursor.fetchone()
        contenido_id = row.id

        # Insertar en peliculas si es tipo 'pelicula'
        if contenido.tipo_contenido.lower() == 'serie':
            cursor.execute("""
                INSERT INTO series (contenido_id, cantidad_temporadas)
                VALUES (?, ?)
            """, (contenido_id, contenido.cantidad_temporadas))

        conn.commit()

        return ContenidoResponse(
            id=row.id,
            titulo=row.titulo,
            descripcion=row.descripcion,
            fecha_lanzamiento=row.fecha_lanzamiento,
            tipo_contenido=row.tipo_contenido
        )

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()        
    