"""
Utility functions for result interpretation and formatting.

Provides confidence scoring and time formatting for match results.
"""

from typing import Dict, Optional


def confidence_label(score: int) -> str:
    """
    Convert a raw match score to a human-readable confidence label.

    Score thresholds are based on empirical testing:
    - < 200: No meaningful match
    - 200-1000: Weak match (noisy environment or short clip)
    - 1000-3000: Medium confidence match
    - >= 3000: Strong match

    Args:
        score: Number of matching fingerprints

    Returns:
        Confidence label string
    """
    if score < 200:
        return "No match"
    elif score < 1000:
        return "Low confidence"
    elif score < 3000:
        return "Medium confidence"
    else:
        return "High confidence"


def seconds_to_mmss(seconds: float) -> str:
    """
    Format seconds as MM:SS string.

    Args:
        seconds: Time in seconds (can be negative)

    Returns:
        Formatted string like "2:34"
    """
    seconds = int(abs(seconds))
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def interpret_match(
    song_name: Optional[str],
    best_offset: Optional[int],
    score: int,
    hop_length: int,
    sr: int
) -> Dict:
    """
    Interpret raw match results into a structured response.

    Converts frame-based offset to time position and adds confidence labeling.

    Args:
        song_name: Identified song name (or None)
        best_offset: Time offset in frames (or None)
        score: Number of matching fingerprints
        hop_length: STFT hop length for time conversion
        sr: Sampling rate

    Returns:
        Dictionary with match results:
        - matched: bool
        - song: song name (if matched)
        - position_in_song: MM:SS format (if matched)
        - confidence: confidence label
        - raw_score: integer score
        - message: human-readable message (if not matched)
    """
    confidence = confidence_label(score)

    if confidence == "No match" or song_name is None or best_offset is None:
        return {
            "matched": False,
            "message": "No matching song detected",
            "raw_score": score
        }

    offset_seconds = best_offset * hop_length / sr
    position = seconds_to_mmss(offset_seconds)

    return {
        "matched": True,
        "song": song_name,
        "position_in_song": position,
        "confidence": confidence,
        "raw_score": score
    }
