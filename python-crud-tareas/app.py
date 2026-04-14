from db import get_connection

ESTADOS_VALIDOS = {"pendiente", "en_progreso", "hecha"}

def crear_tarea():
    titulo = input("Título: ").strip()
    if not titulo:
        print("⚠️ El título no puede estar vacío.")
        return
    descripcion = input("Descripción: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)",
        (titulo, descripcion)
    )
    conn.commit()
    conn.close()
    print("✅ Tarea creada.")

def listar_tareas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, estado, descripcion, created_at FROM tareas ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No hay tareas registradas.")
        return

    print("\n--- TAREAS ---")
    for r in rows:
        id_, titulo, estado, desc, created = r
        print(f"[{id_}] {titulo} | {estado} | {created:%Y-%m-%d %H:%M}")
        if desc:
            print(f"    - {desc}")

def actualizar_estado():
    tarea_id = input("ID de la tarea: ").strip()
    if not tarea_id.isdigit():
        print("⚠️ ID inválido.")
        return

    nuevo_estado = input("Nuevo estado (pendiente/en_progreso/hecha): ").strip().lower()
    if nuevo_estado not in ESTADOS_VALIDOS:
        print("⚠️ Estado inválido.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tareas SET estado=%s WHERE id=%s", (nuevo_estado, int(tarea_id)))
    if cur.rowcount == 0:
        print("⚠️ No existe una tarea con ese ID.")
    else:
        print("✅ Estado actualizado.")
    conn.commit()
    conn.close()

def editar_tarea():
    tarea_id = input("ID de la tarea: ").strip()
    if not tarea_id.isdigit():
        print("⚠️ ID inválido.")
        return

    nuevo_titulo = input("Nuevo título (enter para dejar igual): ").strip()
    nueva_desc = input("Nueva descripción (enter para dejar igual): ").strip()

    conn = get_connection()
    cur = conn.cursor()

    # Traer valores actuales
    cur.execute("SELECT titulo, descripcion FROM tareas WHERE id=%s", (int(tarea_id),))
    row = cur.fetchone()
    if not row:
        print("⚠️ No existe una tarea con ese ID.")
        conn.close()
        return

    titulo_actual, desc_actual = row
    titulo_final = nuevo_titulo if nuevo_titulo else titulo_actual
    desc_final = nueva_desc if nueva_desc else desc_actual

    cur.execute(
        "UPDATE tareas SET titulo=%s, descripcion=%s WHERE id=%s",
        (titulo_final, desc_final, int(tarea_id))
    )
    conn.commit()
    conn.close()
    print("✅ Tarea editada.")

def eliminar_tarea():
    tarea_id = input("ID de la tarea a eliminar: ").strip()
    if not tarea_id.isdigit():
        print("⚠️ ID inválido.")
        return

    confirmar = input("¿Seguro? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Cancelado.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas WHERE id=%s", (int(tarea_id),))
    if cur.rowcount == 0:
        print("⚠️ No existe una tarea con ese ID.")
    else:
        print("🗑️ Tarea eliminada.")
    conn.commit()
    conn.close()

def menu():
    while True:
        print("\n=== Gestor de Tareas (Python + PostgreSQL) ===")
        print("1) Crear tarea")
        print("2) Listar tareas")
        print("3) Editar tarea")
        print("4) Actualizar estado")
        print("5) Eliminar tarea")
        print("6) Salir")
        op = input("Opción: ").strip()

        if op == "1":
            crear_tarea()
        elif op == "2":
            listar_tareas()
        elif op == "3":
            editar_tarea()
        elif op == "4":
            actualizar_estado()
        elif op == "5":
            eliminar_tarea()
        elif op == "6":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
