"""
Audio matching module using offset voting for time-shift invariant recognition.

Implements the core query matching algorithm that compares query fingerprints
against a database and identifies matches using histogram-based offset voting.
"""

from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import numpy as np

from database import Database, FingerprintHash


MatchResult = Tuple[Optional[str], Optional[int], int]  # (song_name, offset, score)


def query_single_song(
    query_fingerprints: List[Tuple[int, int, int, int]],
    db: Dict[FingerprintHash, List[int]]
) -> Tuple[Optional[int], int]:
    """
    Query a single-song database and find the best time offset via voting.

    For each query fingerprint that matches a hash in the database,
    we compute time offsets and vote. The offset with the most votes
    indicates the alignment between query and database song.

    Args:
        query_fingerprints: List of (f1, f2, dt, t_query) from the query audio
        db: Hash database mapping (f1, f2, dt) -> list of time offsets

    Returns:
        Tuple of (best_offset, score) where:
        - best_offset: time alignment in frames (None if no matches)
        - score: number of matching fingerprints at that offset
    """
    offset_votes = defaultdict(int)

    for f1, f2, dt, t_query in query_fingerprints:
        hash_key = (f1, f2, dt)

        if hash_key in db:
            for t_db in db[hash_key]:
                offset = t_db - t_query
                offset_votes[offset] += 1

    if not offset_votes:
        return None, 0

    best_offset = max(offset_votes, key=offset_votes.get)
    return best_offset, offset_votes[best_offset]


def query_multi_song(
    query_fingerprints: List[Tuple[int, int, int, int]],
    db: Database
) -> MatchResult:
    """
    Query a multi-song database and identify the best matching song.

    For each query fingerprint, we look up matching database entries
    and vote on (song_name, offset) pairs. The song+offset with the
    highest vote count is returned as the match.

    Args:
        query_fingerprints: List of (f1, f2, dt, t_query) from the query audio
        db: Multi-song database mapping hash -> list of (song_name, time) pairs

    Returns:
        Tuple of (song_name, offset, score) where:
        - song_name: identified song (None if no match)
        - offset: time alignment in frames (None if no match)
        - score: number of matching fingerprints
    """
    # Vote on (song_name, offset) pairs
    votes = defaultdict(int)

    for f1, f2, dt, t_query in query_fingerprints:
        hash_key = (f1, f2, dt)

        if hash_key in db:
            for song_name, t_db in db[hash_key]:
                offset = t_db - t_query
                votes[(song_name, offset)] += 1

    if not votes:
        return None, None, 0

    # Find the (song, offset) pair with most votes
    best_match = max(votes, key=votes.get)
    song_name, offset = best_match
    score = votes[best_match]

    return song_name, offset, score


def recognize_audio(
    query_audio: np.ndarray,
    db: Database,
    config: Dict
) -> MatchResult:
    """
    High-level recognition function that extracts query fingerprints and matches.

    Args:
        query_audio: Raw audio signal (mono)
        db: Multi-song database
        config: Configuration dictionary with fingerprinting parameters

    Returns:
        Tuple of (song_name, offset, score)
    """
    from fingerprinting import extract_fingerprints

    query_fingerprints = extract_fingerprints(
        y=query_audio,
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

    return query_multi_song(query_fingerprints, db)
