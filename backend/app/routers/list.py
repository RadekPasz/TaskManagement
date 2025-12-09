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