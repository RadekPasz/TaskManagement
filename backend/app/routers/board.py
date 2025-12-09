from fastapi import APIRouter
from backend.app.database import get_db

router = APIRouter(prefix="/boards", tags=["Boards"])

@router.get("/")
def get_boards():
    conn = get_db()
    boards = conn.execute("""
        SELECT
            b.board_id,
            b.name
        FROM board b
        ORDER BY b.name ASC;
    """).fetchall()

    return [dict(row) for row in boards]

@router.get("/{board_id}")
def get_board(board_id: int):
    conn = get_db()
    board = conn.execute("""
        SELECT
            b.board_id,
            b.name
        FROM board b
        WHERE b.board_id = ?;
    """, (board_id,)).fetchone()

    if board is None:
        return {"error": "Board not found"}

    return dict(board)

@router.get("/{board_id}/lists")
def get_board_lists(board_id: int):   
    conn = get_db()
    lists = conn.execute("""
        SELECT
            l.list_id,
            l.name,
            l.board_id
        FROM list l
        WHERE l.board_id = ?
        ORDER BY l.name ASC;
    """, (board_id,)).fetchall()

    return [dict(row) for row in lists]

@router.post("/")
def create_board(name: str):
    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO board (name)
        VALUES (?);
    """, (name,))
    conn.commit()

    new_board_id = cursor.lastrowid
    new_board = conn.execute("""
        SELECT
            b.board_id,
            b.name
        FROM board b
        WHERE b.board_id = ?;
    """, (new_board_id,)).fetchone()

    return dict(new_board)

@router.delete("/{board_id}")
def delete_board(board_id: int):
    conn = get_db()
    conn.execute("""
        DELETE FROM board
        WHERE board_id = ?;
    """, (board_id,))
    conn.commit()

    return {"message": "Board deleted successfully"}

@router.put("/{board_id}")
def update_board(board_id: int, name: str):
    conn = get_db()
    conn.execute("""
        UPDATE board
        SET name = ?
        WHERE board_id = ?;
    """, (name, board_id))
    conn.commit()

    updated_board = conn.execute("""
        SELECT
            b.board_id,
            b.name
        FROM board b
        WHERE b.board_id = ?;
    """, (board_id,)).fetchone()

    return dict(updated_board)