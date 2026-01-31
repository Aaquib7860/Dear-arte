import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.gcp_service import GCPService
from pydantic import BaseModel
import os

# Credentials and config should be loaded from environment variables or .env file
# handled by app.config locally, or system env vars in Cloud Run
app = FastAPI(title="Dear Art Content Filter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Service
# Note: In production, you might want to initialize this lazily or as a dependency
gcp_service = None

@app.on_event("startup")
async def startup_event():
    global gcp_service
    try:
        gcp_service = GCPService()
        print("GCP Service Initialized")
    except Exception as e:
        print(f"Failed to initialize GCP Service: {e}") 
        print("Make sure GOOGLE_APPLICATION_CREDENTIALS and environment variables are set.")

class AnalysisResponse(BaseModel):
    is_good_for_dearArt: bool
    is_art: bool
    has_nudity: bool
    is_artistic_nudity: bool
    reason: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_media(file: UploadFile = File(...)):
    """
    Upload an image or video to check if it's suitable for Dear Art.
    """
    if not gcp_service:
        raise HTTPException(status_code=503, detail="GCP Service not initialized")

    try:
        content = await file.read()
        content_type = file.content_type
        
        result_json_str = await gcp_service.analyze_content(content, content_type)
        result = json.loads(result_json_str)
        return result

    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Dear Art Content Filter API is running"}
