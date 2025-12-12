# Organization Management Service

Simple backend service built using FastAPI and MongoDB.
It supports creating and managing organizations in a multi-tenant style.

## Features
- Create organization (dynamic MongoDB collection)
- Admin login (JWT)
- Update and delete organization
- Password hashing
- Simple multi-tenant architecture

## Tech Stack
- FastAPI
- MongoDB (Motor)
- JWT
- bcrypt

## Running the App
1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Set environment variables in `.env`
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=master_db
JWT_SECRET=supersecretkey
```

3. Start the server
```bash
./run.sh
```

## Folder Structure
```
app/
    main.py
    config.py
    db.py
    routers/
    schemas/
    models/
    utils/
```

## API Endpoints

### Organization
- `POST /org/create` - Create new organization
- `GET /org/get?name={name}` - Get organization details
- `PUT /org/update` - Update organization (requires JWT)
- `DELETE /org/delete?name={name}` - Delete organization (requires JWT)

### Admin
- `POST /admin/login` - Admin login (returns JWT token)

## Architecture Diagram
(Architecture diagram will be added here)
