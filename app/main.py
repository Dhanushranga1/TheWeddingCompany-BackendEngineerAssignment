from fastapi import FastAPI
from app.routers import org

app = FastAPI()

app.include_router(org.router)

@app.get("/")
def home():
    return {"message": "Organization Service Running"}
