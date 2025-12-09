from fastapi import APIRouter
from backend.app.database import get_db

router = APIRouter(prefix="/lists", tags=["Lists"])

@router.get("/")
def get_lists():    
    conn = get_db()
    lists = conn.execute("""
        SELECT
            l.list_id,
            l.name,
            l.board_id
        FROM list l
        ORDER BY l.name ASC;
    """).fetchall()

    return [dict(row) for row in lists]

@router.post("/")
def create_list(name: str, board_id: int):
    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO list (name, board_id)
        VALUES (?, ?);
    """, (name, board_id))
    conn.commit()

    new_list_id = cursor.lastrowid
    new_list = conn.execute("""
        SELECT
            l.list_id,
            l.name,
            l.board_id
        FROM list l
        WHERE l.list_id = ?;
    """, (new_list_id,)).fetchone()

    return dict(new_list)

@router.put("/{list_id}")
def update_list(list_id: int, name: str):
    conn = get_db()
    conn.execute("""
        UPDATE list
        SET name = ?
        WHERE list_id = ?;
    """, (name, list_id))
    conn.commit()

    updated_list = conn.execute("""
        SELECT
            l.list_id,
            l.name,
            l.board_id
        FROM list l
        WHERE l.list_id = ?;
    """, (list_id,)).fetchone()

    return dict(updated_list)

@router.delete("/{list_id}")
def delete_list(list_id: int):
    conn = get_db()
    conn.execute("""
        DELETE FROM list
        WHERE list_id = ?;
    """, (list_id,))
    conn.commit()

    return {"message": "List deleted successfully"}