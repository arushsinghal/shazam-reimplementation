"""
Example usage script demonstrating the audio fingerprinting system.

This script shows how to:
1. Build a database from a single song
2. Query a clip from that song
3. Display the match results
"""

import numpy as np
from main import CONFIG, recognize_from_audio
from fingerprinting import extract_fingerprints, load_audio
from database import build_single_song_db


def example_single_song():
    """
    Example: Build database from one song and query a clip.

    This mirrors the original notebook workflow.
    """
    print("=" * 60)
    print("Audio Fingerprinting Example - Single Song")
    print("=" * 60)

    # Step 1: Load full song
    print("\n1. Loading full song...")
    song_path = "path/to/your/song.mp3"  # Replace with actual path

    try:
        y_full, sr = load_audio(song_path, CONFIG["sr"])
        print(f"   Loaded: {len(y_full) / sr:.1f} seconds")
    except FileNotFoundError:
        print("   ERROR: Please provide a valid song path")
        return

    # Step 2: Extract fingerprints from full song
    print("\n2. Extracting fingerprints from full song...")
    full_fingerprints = extract_fingerprints(
        y=y_full,
        sr=sr,
        n_fft=CONFIG["n_fft"],
        hop_ratio=CONFIG["hop_ratio"],
        freq_neighborhood=CONFIG["freq_neighborhood"],
        time_neighborhood=CONFIG["time_neighborhood"],
        amplitude_threshold=CONFIG["amplitude_threshold"],
        num_bands=CONFIG["num_bands"],
        fanout=CONFIG["fanout"],
        dt_min=CONFIG["dt_min"],
        dt_max_seconds=CONFIG["dt_max_seconds"],
    )
    print(f"   Extracted: {len(full_fingerprints)} fingerprints")

    # Step 3: Build database
    print("\n3. Building hash database...")
    db = build_single_song_db(full_fingerprints)
    print(f"   Database: {len(db)} unique hashes")

    # Step 4: Create a query clip (simulate by taking a segment)
    print("\n4. Creating query clip (60-66 seconds)...")
    query_start = 60  # seconds
    query_duration = 6  # seconds

    start_sample = int(query_start * sr)
    end_sample = int((query_start + query_duration) * sr)
    y_query = y_full[start_sample:end_sample]

    print(f"   Query length: {len(y_query) / sr:.1f} seconds")

    # Step 5: Recognize the query
    print("\n5. Recognizing query clip...")
    result = recognize_from_audio(
        y_query=y_query,
        db=db,
        config=CONFIG,
        song_name_hint="Test Song"
    )

    # Step 6: Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("=" * 60)


def example_with_noise():
    """
    Example: Test robustness with noisy query.
    """
    print("\n" + "=" * 60)
    print("Testing with Background Noise")
    print("=" * 60)
    print("\nNote: Real-world implementation would:")
    print("  - Add background noise to query")
    print("  - Test at different SNR levels")
    print("  - Measure precision/recall")


if __name__ == "__main__":
    example_single_song()

    print("\n\nTo use with your own audio:")
    print("  1. Update song_path in example_single_song()")
    print("  2. Run: python example.py")
    print("\nOr import and use directly:")
    print("  from main import build_database_from_files, recognize_from_file")
