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