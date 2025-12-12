from fastapi import APIRouter, HTTPException, Depends
from app.schemas.org_schemas import CreateOrg, UpdateOrg
from app.db import organizations, admins, get_dynamic_collection, db
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import decode_token

router = APIRouter(prefix="/org")

# simple token dependency
def get_current_admin(token: str):
    try:
        return decode_token(token)
    except:
        raise HTTPException(401, "Invalid token")


@router.post("/create")
async def create_org(data: CreateOrg):
    existing = await organizations.find_one({"name": data.organization_name})
    if existing:
        raise HTTPException(400, "Organization already exists")

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
        raise HTTPException(404, "Organization not found")
    return org


@router.put("/update")
async def update_org(data: UpdateOrg, token: str = Depends(get_current_admin)):
    # verify admin belongs to org
    if data.organization_name != token.get("organization"):
        raise HTTPException(403, "Not allowed")

    old_name = token.get("organization")
    old_org = await organizations.find_one({"name": old_name})

    if not old_org:
        raise HTTPException(404, "Organization not found")

    new_collection = f"org_{data.organization_name.lower()}"
    old_collection = old_org["collection"]

    # create new collection
    await db.create_collection(new_collection)

    old_col_ref = get_dynamic_collection(old_collection)
    new_col_ref = get_dynamic_collection(new_collection)

    items = old_col_ref.find({})
    docs = []
    async for doc in items:
        doc["_id"] = None
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
async def delete_org(name: str, token: str = Depends(get_current_admin)):
    if name != token.get("organization"):
        raise HTTPException(403, "Not allowed")

    org = await organizations.find_one({"name": name})
    if not org:
        raise HTTPException(404, "Organization not found")

    await db.drop_collection(org["collection"])
    await organizations.delete_one({"name": name})
    await admins.delete_one({"organization": name})

    return {"message": "organization deleted"}
