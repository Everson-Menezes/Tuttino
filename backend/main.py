from fastapi import FastAPI
from controllers.health_controller import router as health_router
from controllers.home_controller import router as home_router
from controllers.game_controller import router as game_router

app = FastAPI()

app.include_router(game_router)
app.include_router(home_router)
app.include_router(health_router)