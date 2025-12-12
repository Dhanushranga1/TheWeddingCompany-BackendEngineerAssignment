from pydantic import BaseModel

class CreateOrg(BaseModel):
    organization_name: str
    email: str
    password: str

class GetOrg(BaseModel):
    organization_name: str

class UpdateOrg(BaseModel):
    organization_name: str
    email: str
    password: str
