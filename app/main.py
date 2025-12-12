from fastapi import FastAPI
from app.routers import org, auth

app = FastAPI()

app.include_router(org.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Organization Service Running"}
