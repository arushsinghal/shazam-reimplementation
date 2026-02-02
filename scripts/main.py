"""
Main orchestration module for the audio fingerprinting system.

Demonstrates building a multi-song database and recognizing query audio clips.
"""

from typing import Dict
import numpy as np

from core.fingerprinting import extract_fingerprints, load_audio
from core.database import build_song_database, build_single_song_db
from core.matcher import query_multi_song, query_single_song
from core.utils import interpret_match
from core.config import DEFAULT_CONFIG


# Use config from config module
CONFIG = DEFAULT_CONFIG


def build_database_from_files(audio_files: Dict[str, str], config: Dict = None) -> tuple:
    """
    Build a fingerprint database from multiple audio files.

    Args:
        audio_files: Dictionary mapping song_name -> file_path
        config: Configuration dict (uses CONFIG if None)

    Returns:
        Tuple of (database, metadata)
    """
    if config is None:
        config = CONFIG

    song_fingerprints = {}

    for song_name, file_path in audio_files.items():
        print(f"Processing {song_name}...")
        y, sr = load_audio(file_path, config["sr"])

        fingerprints = extract_fingerprints(
            y=y,
            sr=sr,
            n_fft=config["n_fft"],
            hop_ratio=config["hop_ratio"],
            freq_neighborhood=config["freq_neighborhood"],
            time_neighborhood=config["time_neighborhood"],
            amplitude_threshold=config["amplitude_threshold"],
            num_bands=config["num_bands"],
            fanout=config["fanout"],
            dt_min=config["dt_min"],
            dt_max_seconds=config["dt_max_seconds"],
        )

        song_fingerprints[song_name] = fingerprints
        print(f"  Extracted {len(fingerprints)} fingerprints")

    db, metadata = build_song_database(song_fingerprints)
    print(f"\nDatabase built with {len(db)} unique hashes")

    return db, metadata


def recognize_from_file(query_path: str, db: dict, config: Dict = None) -> Dict:
    """
    Recognize a query audio file against the database.

    Args:
        query_path: Path to query audio file
        db: Fingerprint database (multi-song or single-song)
        config: Configuration dict (uses CONFIG if None)

    Returns:
        Match result dictionary from interpret_match()
    """
    if config is None:
        config = CONFIG

    # Load query audio
    y_query, sr = load_audio(query_path, config["sr"])

    # Extract query fingerprints
    query_fingerprints = extract_fingerprints(
        y=y_query,
        sr=sr,
        n_fft=config["n_fft"],
        hop_ratio=config["hop_ratio"],
        freq_neighborhood=config["freq_neighborhood"],
        time_neighborhood=config["time_neighborhood"],
        amplitude_threshold=config["amplitude_threshold"],
        num_bands=config["num_bands"],
        fanout=config["fanout"],
        dt_min=config["dt_min"],
        dt_max_seconds=config["dt_max_seconds"],
    )

    print(f"Query fingerprints: {len(query_fingerprints)}")

    # Determine if multi-song or single-song database
    # Multi-song DB has tuple values: [(song, time), ...]
    # Single-song DB has list values: [time, ...]
    sample_value = next(iter(db.values())) if db else []
    is_multi_song = (
        len(sample_value) > 0 and
        isinstance(sample_value[0], tuple) and
        len(sample_value[0]) == 2 and
        isinstance(sample_value[0][0], str)
    )

    if is_multi_song:
        song_name, offset, score = query_multi_song(query_fingerprints, db)
    else:
        # Single-song database
        song_name = "Unknown"
        offset, score = query_single_song(query_fingerprints, db)

    # Interpret results
    hop_length = config["n_fft"] // config["hop_ratio"]
    result = interpret_match(
        song_name=song_name,
        best_offset=offset,
        score=score,
        hop_length=hop_length,
        sr=config["sr"]
    )

    return result


def recognize_from_audio(
    y_query: np.ndarray,
    db: dict,
    config: Dict = None,
    song_name_hint: str = None
) -> Dict:
    """
    Recognize a query audio signal against the database.

    Args:
        y_query: Query audio signal (mono)
        db: Fingerprint database
        config: Configuration dict (uses CONFIG if None)
        song_name_hint: Optional song name for single-song databases

    Returns:
        Match result dictionary from interpret_match()
    """
    if config is None:
        config = CONFIG

    # Extract query fingerprints
    query_fingerprints = extract_fingerprints(
        y=y_query,
        sr=config["sr"],
        n_fft=config["n_fft"],
        hop_ratio=config["hop_ratio"],
        freq_neighborhood=config["freq_neighborhood"],
        time_neighborhood=config["time_neighborhood"],
        amplitude_threshold=config["amplitude_threshold"],
        num_bands=config["num_bands"],
        fanout=config["fanout"],
        dt_min=config["dt_min"],
        dt_max_seconds=config["dt_max_seconds"],
    )

    # Determine database type
    sample_value = next(iter(db.values())) if db else []
    is_multi_song = (
        len(sample_value) > 0 and
        isinstance(sample_value[0], tuple) and
        len(sample_value[0]) == 2 and
        isinstance(sample_value[0][0], str)
    )

    if is_multi_song:
        song_name, offset, score = query_multi_song(query_fingerprints, db)
    else:
        song_name = song_name_hint or "Unknown"
        offset, score = query_single_song(query_fingerprints, db)

    # Interpret results
    hop_length = config["n_fft"] // config["hop_ratio"]
    result = interpret_match(
        song_name=song_name,
        best_offset=offset,
        score=score,
        hop_length=hop_length,
        sr=config["sr"]
    )

    return result


if __name__ == "__main__":
    # Example usage
    print("Audio Fingerprinting System")
    print("=" * 50)
    print("\nThis is the main orchestration module.")
    print("\nExample usage:")
    print("""
    from main import build_database_from_files, recognize_from_file

    # Build database from song files
    audio_files = {
        "Song A": "path/to/song_a.mp3",
        "Song B": "path/to/song_b.mp3",
    }
    db, metadata = build_database_from_files(audio_files)

    # Recognize a query clip
    result = recognize_from_file("query_clip.mp3", db)
    print(result)
    """)
