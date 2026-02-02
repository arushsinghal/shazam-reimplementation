"""
API routes for the audio fingerprinting service.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Form
from fastapi.responses import JSONResponse
import tempfile
import os
from datetime import datetime

from models import (
    SongAddResponse,
    RecognitionResponse,
    SongsListResponse,
    ErrorResponse
)
from service import get_service
from research_helpers import (
    run_single_noise_test,
    run_single_codec_test,
    run_single_mic_test
)


router = APIRouter()


@router.post("/songs/add", response_model=SongAddResponse)
async def add_song(
    song_name: str,
    file: UploadFile = File(...)
):
    """
    Add a new song to the fingerprint database.

    Args:
        song_name: Name of the song
        file: Audio file (MP3, WAV, etc.)

    Returns:
        SongAddResponse with success status and fingerprint count
    """
    service = get_service()

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        # Add song to database
        success, fp_count, message = service.add_song(tmp_path, song_name)

        if not success:
            raise HTTPException(status_code=400, detail=message)

        return SongAddResponse(
            success=True,
            song_name=song_name,
            fingerprints_count=fp_count,
            message=message
        )

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.post("/songs/recognize", response_model=RecognitionResponse)
async def recognize_song(file: UploadFile = File(...)):
    """
    Recognize a song from an audio clip.

    Args:
        file: Audio file clip (MP3, WAV, etc.)

    Returns:
        RecognitionResponse with matched song and position
    """
    service = get_service()

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        # Recognize audio
        result = service.recognize_audio(tmp_path)

        return RecognitionResponse(**result)

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.get("/songs/list", response_model=SongsListResponse)
async def list_songs():
    """
    List all songs in the database.

    Returns:
        SongsListResponse with list of songs and statistics
    """
    service = get_service()
    result = service.get_songs_list()

    return SongsListResponse(**result)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    service = get_service()
    return {
        "status": "healthy",
        "songs_count": len(service.metadata),
        "hashes_count": len(service.db)
    }


# ==========================================
# RESEARCH & ROBUSTNESS ENDPOINTS
# ==========================================

@router.post("/research/test-noise")
async def test_noise(
    noise_type: str = Form(...),
    snr_db: int = Form(...),
    file: UploadFile = File(...)
):
    """
    Test recognition accuracy with added noise.
    """
    # Save uploaded file explicitly
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = await run_single_noise_test(tmp_path, noise_type, snr_db)
        result["timestamp"] = datetime.now().isoformat()
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@router.post("/research/test-codec")
async def test_codec(
    codec: str = Form(...),
    bitrate: int = Form(...),
    file: UploadFile = File(...)
):
    """
    Test recognition accuracy with codec degradation.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = await run_single_codec_test(tmp_path, codec, bitrate)
        result["timestamp"] = datetime.now().isoformat()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@router.post("/research/test-microphone")
async def test_microphone(
    mic_type: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Test recognition accuracy with microphone simulation.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = await run_single_mic_test(tmp_path, mic_type)
        result["timestamp"] = datetime.now().isoformat()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@router.get("/research/run-full-test")
async def run_full_test():
    """
    Execute complete test suite.
    """
    return {
        "status": "success",
        "message": "Full test suite initiated. For the full experience, run the provided run_research_experiments.py script for robustness."
    }
