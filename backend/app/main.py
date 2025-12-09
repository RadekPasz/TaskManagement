from fastapi import FastAPI
from backend.app.routers import board, card, list

app = FastAPI()

app.include_router(board.router)
app.include_router(list.router)
app.include_router(card.router)