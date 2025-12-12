from fastapi import FastAPI
from app.routers import org, auth
from app.db import create_indexes

app = FastAPI(
    title="Organization Management Service",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await create_indexes()

app.include_router(org.router, tags=["Organization"])
app.include_router(auth.router, tags=["Admin"])

@app.get("/")
def home():
    return {"message": "Organization Service Running"}
