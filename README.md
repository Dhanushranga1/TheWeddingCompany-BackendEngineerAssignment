# Organization Management Service

A backend service for managing organizations in a multi-tenant architecture. Built with FastAPI and MongoDB, this service allows creating organizations, managing admins, and handling authentication using JWT tokens.

## What This Does

This service lets you create separate organizations, where each organization gets its own space in the database. Think of it like creating separate workspaces - each organization is isolated from others but all managed from one place.

Key features:
- Create organizations with admin accounts
- Secure login system with JWT tokens
- Update organization details and migrate data
- Delete organizations safely
- Each organization gets its own database collection

## Tech Stack
- **FastAPI** - Fast and modern Python web framework
- **MongoDB (Motor)** - NoSQL database with async support
- **JWT** - Token-based authentication
- **bcrypt** - Password hashing for security

## Architecture

![Architecture Diagram](./app/architecture.png)

### How It Works

**Master Database**: This is the main database that keeps track of all organizations and their admins. It has two collections:
- `organizations` - stores org name, collection name, and admin reference
- `admins` - stores admin credentials (hashed passwords) and which org they belong to

**Dynamic Collections**: When you create a new organization (say "alpha"), the system automatically creates a new collection called `org_alpha`. This is where all that organization's data would live. Each org is completely separate.

**Authentication Flow**: 
1. Admin logs in with email and password
2. System checks credentials and returns a JWT token
3. This token is used for protected operations like updating or deleting organizations
4. The token contains the admin's ID and their organization name

## Setup and Running

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with these variables:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=master_db
JWT_SECRET=supersecretkey
```

3. Make sure MongoDB is running on your system

4. Start the server
```bash
./run.sh
```

The API will be available at `http://localhost:8000`

You can also check the interactive API docs at `http://localhost:8000/docs`

## API Endpoints

### Create Organization
```bash
POST /org/create
```
Creates a new organization with an admin account. This also creates a dedicated database collection for the organization.

### Get Organization
```bash
GET /org/get?name={organization_name}
```
Retrieves organization details from the master database.

### Update Organization
```bash
PUT /org/update
```
Updates organization details. Requires JWT token in Authorization header. Can rename the organization and update admin credentials. Also handles migrating data to the new collection if org name changes.

### Delete Organization
```bash
DELETE /org/delete?name={organization_name}
```
Deletes an organization. Requires JWT token. Only the org's admin can delete it.

### Admin Login
```bash
POST /admin/login
```
Login with email and password. Returns a JWT token to use for authenticated requests.

## Project Structure
```
app/
    main.py          # FastAPI app and route registration
    config.py        # Environment configuration
    db.py            # MongoDB connection and collections
    routers/
        org.py       # Organization CRUD operations
        auth.py      # Admin login
    schemas/
        org_schemas.py      # Request/response models for orgs
        admin_schemas.py    # Request/response models for admins
    utils/
        security.py         # Password hashing functions
        jwt_handler.py      # JWT token creation and validation
```

## Design Decisions

**Why MongoDB?** - MongoDB's flexible schema and ability to create collections dynamically made it perfect for this multi-tenant setup.

**Why separate collections per org?** - This gives good data isolation between organizations. Each org's data is completely separate, making it easier to manage and more secure.

**What are the tradeoffs?** - Having many collections can get harder to manage at scale. A better approach for production might be using a single collection with an `org_id` field and proper indexing. But for this assignment, separate collections clearly demonstrate the multi-tenant concept.
