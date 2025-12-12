from fastapi import APIRouter, HTTPException, Depends, Header
from app.schemas.org_schemas import CreateOrg, UpdateOrg
from app.db import organizations, admins, get_dynamic_collection, db
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import decode_token

router = APIRouter(prefix="/org")

def get_current_admin(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = parts[1]
    try:
        return decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/create")
async def create_org(data: CreateOrg):
    existing = await organizations.find_one({"name": data.organization_name})
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    collection_name = f"org_{data.organization_name.lower()}"

    # create the org collection
    await db.create_collection(collection_name)

    hashed_pw = hash_password(data.password)

    admin = await admins.insert_one({
        "email": data.email,
        "password": hashed_pw,
        "organization": data.organization_name
    })

    await organizations.insert_one({
        "name": data.organization_name,
        "collection": collection_name,
        "admin_id": str(admin.inserted_id)
    })

    return {"message": "organization created"}


@router.get("/get")
async def get_org(name: str):
    org = await organizations.find_one({"name": name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.put("/update")
async def update_org(data: UpdateOrg, admin_data: dict = Depends(get_current_admin)):
    old_name = admin_data.get("organization")
    old_org = await organizations.find_one({"name": old_name})

    if not old_org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # check if new name already exists
    if data.organization_name != old_name:
        existing = await organizations.find_one({"name": data.organization_name})
        if existing:
            raise HTTPException(status_code=400, detail="Organization name already exists")

    new_collection = f"org_{data.organization_name.lower()}"
    old_collection = old_org["collection"]

    # create new collection
    await db.create_collection(new_collection)

    old_col_ref = get_dynamic_collection(old_collection)
    new_col_ref = get_dynamic_collection(new_collection)

    items = old_col_ref.find({})
    docs = []
    async for doc in items:
        doc.pop("_id", None)
        docs.append(doc)

    if docs:
        await new_col_ref.insert_many(docs)

    await db.drop_collection(old_collection)

    await organizations.update_one(
        {"name": old_name},
        {"$set": {
            "name": data.organization_name,
            "collection": new_collection
        }}
    )

    hashed_pw = hash_password(data.password)
    await admins.update_one(
        {"organization": old_name},
        {"$set": {
            "email": data.email,
            "password": hashed_pw,
            "organization": data.organization_name
        }}
    )

    return {"message": "organization updated"}


@router.delete("/delete")
async def delete_org(name: str, admin_data: dict = Depends(get_current_admin)):
    if name != admin_data.get("organization"):
        raise HTTPException(status_code=403, detail="Not allowed")

    org = await organizations.find_one({"name": name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    await db.drop_collection(org["collection"])
    await organizations.delete_one({"name": name})
    await admins.delete_one({"organization": name})

    return {"message": "organization deleted"}
