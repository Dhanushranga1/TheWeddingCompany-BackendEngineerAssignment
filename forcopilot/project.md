✅ 1. High-Level Architecture (Simple & Correct)
Master DB (Static Collections)

organizations

admins

Dynamic Per-Organization Collections

On /org/create, create collection:
org_<organization_name>

This is empty or with a basic schema placeholder.

Authentication

Admin login → returns JWT containing:

admin_id

organization_name

APIs
POST /org/create
GET  /org/get
PUT  /org/update
DELETE /org/delete
POST /admin/login

✅ 2. Folder Structure (Keep It Very Clean)
backend/
 ├── app/
 │    ├── main.py
 │    ├── config.py
 │    ├── db.py
 │    ├── routers/
 │    │      ├── org.py
 │    │      ├── auth.py
 │    ├── models/
 │    │      ├── organization.py
 │    │      ├── admin.py
 │    ├── schemas/
 │    │      ├── org_schemas.py
 │    │      ├── admin_schemas.py
 │    ├── utils/
 │    │      ├── security.py
 │    │      ├── jwt_handler.py
 │    ├── README.md
 ├── requirements.txt
 └── run.sh


This is about the simplest clean layout that also looks professional.

✅ 3. Step-by-Step Implementation Plan

Below is exactly what to build, in order.

Step 1: Setup FastAPI + Motor (Async MongoDB Driver)

pip install fastapi uvicorn motor passlib[bcrypt] python-jose

Step 2: Database Connection (db.py)

One connection → two logical types:

Master DB → static collections organizations, admins

Dynamic collections → we create using the same DB but with unique names
(org_xxx)

Step 3: Organization Logic
POST /org/create

Flow:

Check if organization already exists in organizations collection.

Create dynamic collection name: org_<organization_name.lower()>

db[collection].insert_one({ "created_at": ... }) → optional

Hash admin password → create admin entry in admins

Save org metadata to Master DB:

{
   "name": organization_name,
   "collection_name": org_organization,
   "admin_id": <id>
}


Return success JSON.

GET /org/get

Fetch org from organizations

If not found → send 404

PUT /org/update

This is basically a RE-NAME operation:

Validate new name isn't taken

Create new collection for updated name

Copy data from old collection to new collection

Delete old collection

Update metadata

Keep it simple: just copy all docs using find() → insert_many()

DELETE /org/delete

Only allow deletion if JWT is valid AND the logged-in admin belongs to that organization.

Drop dynamic collection

Delete organization entry

Delete related admin entry

Step 4: Admin Login
POST /admin/login

Find admin by email

Verify bcrypt password

Generate JWT:

{
  "admin_id": str(admin["_id"]),
  "organization": org_name
}


Return token

Step 5: JWT Auth Middleware

For delete/update operations

Extract token → load admin → attach org to request

Step 6: README Instructions

Your README should include:

✔ Project overview
✔ Tech stack
✔ Steps to run
✔ Example environment variables
✔ A simple architecture diagram (hand drawn also okay)
✔ Example API request bodies

✅ 4. The Architecture Question — What You Should Answer in Interview

Include this in repo or PDF:

Is this a scalable architecture?

Yes — but with tradeoffs.

Pros

Simple multi-tenant design

Fast creation of new orgs (just create a new collection)

Easy data isolation per organization

Works very well for CRUD-style SaaS backends

MongoDB fits dynamic schema requirements

Cons / Tradeoffs

Too many collections = performance overhead in MongoDB

Hard to run analytics across all tenants

No strict schema enforcement

Backup/restore per tenant becomes complex

Write amplification during rename/update operations

What could be better?

(Keep this honest and internship-level.)

Instead of per-org collections, use single collection with org_id partitioning → easier indexing and scaling.

Use AWS DynamoDB or PostgreSQL schemas (if strictly multi-tenant).

Use a proper metadata service with connection pooling per tenant.

But since the assignment explicitly wants dynamic collections, your solution is correct.

✅ 5. What You Should Commit in GitHub

Each commit should be clean and purposeful:

init: project structure + requirements

feat: add db connection + config

feat: add organization create API

feat: add admin model + password hashing

feat: implement JWT auth

feat: add update org logic

feat: add delete org logic with authorization

chore: add example .env file

docs: update README with architecture diagram

This looks professional and shows good engineering habits.

If you want, I can generate:

✅ The entire FastAPI codebase
✅ A clean repo template you can paste directly into VSCode
✅ A diagram image
✅ The README.md fully written

Just tell me:
Do you want me to generate the full code now?