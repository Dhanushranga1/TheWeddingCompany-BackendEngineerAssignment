from fastapi import APIRouter, HTTPException
from app.schemas.admin_schemas import AdminLogin
from app.db import admins
from app.utils.security import verify_password
from app.utils.jwt_handler import create_token

router = APIRouter(prefix="/admin")


@router.post("/login")
async def admin_login(data: AdminLogin):
    admin = await admins.find_one({"email": data.email})
    if not admin:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(data.password, admin["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({
        "admin_id": str(admin["_id"]),
        "organization": admin["organization"]
    })

    return {"token": token}
