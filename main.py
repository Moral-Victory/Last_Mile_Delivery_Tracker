import os
import json
import random
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import jwt

DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")
JWT_SECRET = os.environ.get("JWT_SECRET", "LAST_MILE_SECRET_12345")
ALGORITHM = "HS256"

app = FastAPI(
    title="Last-Mile Dispatch API - Phase 1",
    description="Backend API framework containing role-based user management and database storage.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

def read_db() -> dict:
    if not os.path.exists(DB_FILE):
        raise HTTPException(status_code=500, detail="Database store not initialized.")
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(data: dict):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_jwt_token(data: dict) -> str:
    return jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM)

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header.")
    try:
        token = authorization.split(" ")[1]
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed.")

# Models
class LoginModel(BaseModel):
    email: EmailStr
    password: str

class RegisterModel(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str # 'customer', 'agent', 'admin'
    zone: Optional[str] = None

@app.post("/api/auth/login")
def login(data: LoginModel):
    db = read_db()
    user = next((u for u in db["users"] if u["email"] == data.email and u["password"] == data.password), None)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    token = create_jwt_token({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "name": user["name"]
    })
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "name": user["name"]
        }
    }

@app.post("/api/auth/register")
def register(data: RegisterModel):
    db = read_db()
    if any(u["email"] == data.email for u in db["users"]):
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    new_user = {
        "id": "usr_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8)),
        "email": data.email,
        "password": data.password,
        "role": data.role,
        "name": data.name,
        "zone": data.zone,
        "location": { "lat": 28.61, "lng": 77.20 },
        "available": True
    }
    db["users"].append(new_user)
    write_db(db)
    return { "message": "User registered successfully.", "user": { "id": new_user["id"], "email": new_user["email"] } }

@app.get("/api/auth/me")
def check_me(current_user: dict = Depends(get_current_user)):
    return { "authenticated": True, "user": current_user }

# Server files
app.mount("/", StaticFiles(directory="public", html=True), name="public")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
