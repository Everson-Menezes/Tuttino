from fastapi import FastAPI, APIRouter

app = FastAPI()

home_router = APIRouter()

@home_router.get("/home")
async def home():
    return {"message": "API is online and running"}

app.include_router(home_router)
