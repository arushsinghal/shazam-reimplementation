"""
Core audio fingerprinting implementation.

This package contains the core Shazam-style audio fingerprinting algorithm:
- fingerprinting: Audio spectrogram and fingerprint extraction
- database: Hash database creation and management
- matcher: Query matching via offset voting
- config: Configuration parameters
- utils: Utility functions for confidence scoring and formatting
"""

from .config import DEFAULT_CONFIG
from .fingerprinting import extract_fingerprints, load_audio
from .database import build_song_database, build_single_song_db, Database
from .matcher import query_multi_song, query_single_song
from .utils import interpret_match, confidence_label, seconds_to_mmss

__all__ = [
    'DEFAULT_CONFIG',
    'extract_fingerprints',
    'load_audio',
    'build_song_database',
    'build_single_song_db',
    'Database',
    'query_multi_song',
    'query_single_song',
    'interpret_match',
    'confidence_label',
    'seconds_to_mmss',
]
