from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key not set in environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

class User(BaseModel):
    email: str
    password: str

@app.post("/")
async def add_user(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    try:
        response = supabase.table("users").insert({"email": email, "password": password}).execute()
        if response.error:
            raise HTTPException(status_code=500, detail=response.error.message)
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
