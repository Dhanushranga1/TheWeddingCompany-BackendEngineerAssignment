from fastapi import FastAPI
from app.routers import org, auth

app = FastAPI(
    title="Organization Management Service",
    version="1.0.0"
)

app.include_router(org.router, tags=["Organization"])
app.include_router(auth.router, tags=["Admin"])

@app.get("/")
def home():
    return {"message": "Organization Service Running"}
