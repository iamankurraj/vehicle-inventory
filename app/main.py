from fastapi import FastAPI
from app.routers import inventory, reservation, chat
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(inventory.router)
app.include_router(reservation.router)
app.include_router(chat.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
