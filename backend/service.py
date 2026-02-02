"""
Audio fingerprinting service layer.

Wraps the core fingerprinting modules and manages the database state.
"""

import sys
import os
from typing import Dict, Tuple, Optional, List
import numpy as np
import pickle
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fingerprinting import extract_fingerprints, load_audio
from database import build_song_database, Database
from matcher import query_multi_song
from utils import interpret_match
from config import DEFAULT_CONFIG


class AudioFingerprintingService:
    """
    Service for managing audio fingerprinting database and recognition.
    """

    def __init__(self, db_path: str = "fingerprint_db.pkl"):
        """
        Initialize the service.

        Args:
            db_path: Path to save/load the database
        """
        self.db_path = db_path
        self.db: Database = {}
        self.metadata: Dict = {}
        self.config = DEFAULT_CONFIG.copy()

        # Load existing database if it exists
        self.load_database()

    def load_database(self) -> bool:
        """
        Load database from disk if it exists.

        Returns:
            True if loaded successfully, False if no database exists
        """
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'rb') as f:
                    data = pickle.load(f)
                    self.db = data.get('db', {})
                    self.metadata = data.get('metadata', {})
                print(f"Loaded database with {len(self.db)} hashes and {len(self.metadata)} songs")
                return True
            except Exception as e:
                print(f"Error loading database: {e}")
                return False
        return False

    def save_database(self) -> bool:
        """
        Save database to disk.

        Returns:
            True if saved successfully
        """
        try:
            with open(self.db_path, 'wb') as f:
                pickle.dump({
                    'db': self.db,
                    'metadata': self.metadata
                }, f)
            print(f"Saved database to {self.db_path}")
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False

    def add_song(self, audio_path: str, song_name: str) -> Tuple[bool, int, str]:
        """
        Add a song to the database.

        Args:
            audio_path: Path to audio file
            song_name: Name of the song

        Returns:
            Tuple of (success, fingerprints_count, message)
        """
        try:
            # Load audio
            y, sr = load_audio(audio_path, self.config["sr"])

            # Extract fingerprints
            fingerprints = extract_fingerprints(
                y=y,
                sr=sr,
                n_fft=self.config["n_fft"],
                hop_ratio=self.config["hop_ratio"],
                freq_neighborhood=self.config["freq_neighborhood"],
                time_neighborhood=self.config["time_neighborhood"],
                amplitude_threshold=self.config["amplitude_threshold"],
                num_bands=self.config["num_bands"],
                fanout=self.config["fanout"],
                dt_min=self.config["dt_min"],
                dt_max_seconds=self.config["dt_max_seconds"],
            )

            # Add to database
            song_fingerprints = {song_name: fingerprints}
            new_db, new_metadata = build_song_database(song_fingerprints)

            # Merge with existing database
            for hash_key, entries in new_db.items():
                if hash_key in self.db:
                    self.db[hash_key].extend(entries)
                else:
                    self.db[hash_key] = entries

            # Update metadata
            self.metadata[song_name] = new_metadata[song_name]
            self.metadata[song_name]['duration_seconds'] = len(y) / sr

            # Save database
            self.save_database()

            return True, len(fingerprints), f"Successfully added {song_name}"

        except Exception as e:
            return False, 0, f"Error adding song: {str(e)}"

    def recognize_audio(self, audio_path: str) -> Dict:
        """
        Recognize audio from a file.

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with recognition results
        """
        try:
            # Load audio
            y_query, sr = load_audio(audio_path, self.config["sr"])

            # Extract query fingerprints
            query_fingerprints = extract_fingerprints(
                y=y_query,
                sr=sr,
                n_fft=self.config["n_fft"],
                hop_ratio=self.config["hop_ratio"],
                freq_neighborhood=self.config["freq_neighborhood"],
                time_neighborhood=self.config["time_neighborhood"],
                amplitude_threshold=self.config["amplitude_threshold"],
                num_bands=self.config["num_bands"],
                fanout=self.config["fanout"],
                dt_min=self.config["dt_min"],
                dt_max_seconds=self.config["dt_max_seconds"],
            )

            # Query database
            song_name, offset, score = query_multi_song(query_fingerprints, self.db)

            # Interpret results
            hop_length = self.config["n_fft"] // self.config["hop_ratio"]
            result = interpret_match(
                song_name=song_name,
                best_offset=offset,
                score=score,
                hop_length=hop_length,
                sr=self.config["sr"]
            )

            return result

        except Exception as e:
            return {
                "matched": False,
                "message": f"Error during recognition: {str(e)}"
            }

    def get_songs_list(self) -> Dict:
        """
        Get list of all songs in the database.

        Returns:
            Dictionary with songs list and statistics
        """
        songs = []
        for song_name, meta in self.metadata.items():
            songs.append({
                "name": song_name,
                "fingerprints_count": meta.get("num_fingerprints", 0),
                "duration_seconds": meta.get("duration_seconds")
            })

        return {
            "songs": songs,
            "total_songs": len(songs),
            "total_hashes": len(self.db)
        }


# Global service instance
_service: Optional[AudioFingerprintingService] = None


def get_service() -> AudioFingerprintingService:
    """Get or create the global service instance."""
    global _service
    if _service is None:
        _service = AudioFingerprintingService()
    return _service
