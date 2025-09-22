from fastapi import FastAPI, HTTPException
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

@app.get("/")
async def health_check():
    try:
        # Simple query to test connection
        response = supabase.table("users").select("*").limit(1).execute()
        return {"status": "ok", "message": "Connected to Supabase", "sample_data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
