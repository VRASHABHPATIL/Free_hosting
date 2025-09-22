from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing. Set them in Vercel Environment Variables.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Supabase FastAPI + Frontend")

# User model
class User(BaseModel):
    email: str
    password: str = None

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return FileResponse("static/index.html")

# Health check
@app.get("/health")
async def health_check():
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        return {"status": "ok", "sample_data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add user
@app.post("/add-user")
async def add_user(user: User):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    try:
        response = supabase.table("users").insert({
            "email": user.email,
            "password": user.password
        }).execute()

        # Check if insertion succeeded
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to insert user")

        return {"status": "success", "data": response.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional local run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
