"""
Hash database module for storing and retrieving audio fingerprints.

The database maps fingerprint hashes (f1, f2, dt) to lists of (song_name, time) pairs,
enabling efficient lookup during audio recognition.
"""

from typing import Dict, List, Tuple
from collections import defaultdict
import numpy as np


FingerprintHash = Tuple[int, int, int]  # (f1, f2, dt)
DatabaseEntry = Tuple[str, int]  # (song_name, time_offset)
Database = Dict[FingerprintHash, List[DatabaseEntry]]


def build_song_database(
    song_fingerprints: Dict[str, List[Tuple[int, int, int, int]]]
) -> Tuple[Database, Dict[str, Dict[str, int]]]:
    """
    Build a hash database from fingerprints of multiple songs.

    Each fingerprint (f1, f2, dt, t1) is hashed by (f1, f2, dt) and stored
    with the song name and time offset t1. This allows multiple songs to
    coexist in the same database.

    Args:
        song_fingerprints: Dictionary mapping song_name -> list of fingerprints
                          where each fingerprint is (f1, f2, dt, t1)

    Returns:
        Tuple of:
        - Database: hash -> list of (song_name, time_offset) pairs
        - Metadata: song_name -> {"num_fingerprints": count}
    """
    db: Database = defaultdict(list)
    metadata: Dict[str, Dict[str, int]] = {}

    for song_name, fingerprints in song_fingerprints.items():
        for f1, f2, dt, t1 in fingerprints:
            hash_key = (f1, f2, dt)
            db[hash_key].append((song_name, t1))

        metadata[song_name] = {
            "num_fingerprints": len(fingerprints)
        }

    return dict(db), metadata


def build_single_song_db(
    fingerprints: List[Tuple[int, int, int, int]]
) -> Dict[FingerprintHash, List[int]]:
    """
    Build a hash database for a single song (legacy interface).

    This is a simplified version that doesn't track song names,
    useful for single-song recognition scenarios.

    Args:
        fingerprints: List of (f1, f2, dt, t1) tuples

    Returns:
        Dictionary mapping hash -> list of time offsets
    """
    db = defaultdict(list)
    for f1, f2, dt, t1 in fingerprints:
        hash_key = (f1, f2, dt)
        db[hash_key].append(t1)
    return dict(db)
