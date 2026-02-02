"""
API models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class SongAddResponse(BaseModel):
    """Response for adding a song to the database."""
    success: bool
    song_name: str
    fingerprints_count: int
    message: str


class RecognitionRequest(BaseModel):
    """Request model (not used for file upload, but kept for reference)."""
    pass


class RecognitionResponse(BaseModel):
    """Response for audio recognition."""
    matched: bool
    song: Optional[str] = None
    position_in_song: Optional[str] = None
    confidence: Optional[str] = None
    raw_score: Optional[int] = None
    message: Optional[str] = None


class SongInfo(BaseModel):
    """Information about a song in the database."""
    name: str
    fingerprints_count: int
    duration_seconds: Optional[float] = None


class SongsListResponse(BaseModel):
    """Response for listing all songs."""
    songs: List[SongInfo]
    total_songs: int
    total_hashes: int


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
