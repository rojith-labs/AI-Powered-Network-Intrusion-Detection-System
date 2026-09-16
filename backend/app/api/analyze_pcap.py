import os
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.network.pcap_analyzer import PCAPAnalyzer

router = APIRouter()

@router.post("/analyze-pcap")
async def analyze_pcap_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    ext = Path(file.filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format '{ext}'. Only .pcap and .pcapng files are supported."
        )

    # Save uploaded file safely
    temp_path = settings.UPLOAD_DIR / f"upload_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded PCAP file: {str(e)}")

    try:
        report = PCAPAnalyzer.process_file(db, str(temp_path), file.filename)
        return report
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during PCAP parsing: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_path.exists():
            try:
                os.remove(temp_path)
            except Exception:
                pass
