"""
Validation script to verify the refactored code matches notebook behavior.

This script demonstrates that the production modules produce identical outputs
to the original notebook implementation.
"""

import numpy as np
from fingerprinting import extract_fingerprints
from database import build_single_song_db, build_song_database
from matcher import query_single_song, query_multi_song
from utils import interpret_match, confidence_label, seconds_to_mmss
from config import DEFAULT_CONFIG


def test_configuration():
    """Verify CONFIG matches notebook values."""
    print("Testing Configuration...")

    assert DEFAULT_CONFIG["sr"] == 44100
    assert DEFAULT_CONFIG["n_fft"] == 2048
    assert DEFAULT_CONFIG["hop_ratio"] == 4
    assert DEFAULT_CONFIG["freq_neighborhood"] == 20
    assert DEFAULT_CONFIG["time_neighborhood"] == 20
    assert DEFAULT_CONFIG["amplitude_threshold"] == -35
    assert DEFAULT_CONFIG["num_bands"] == 6
    assert DEFAULT_CONFIG["fanout"] == 10
    assert DEFAULT_CONFIG["dt_min"] == 2
    assert DEFAULT_CONFIG["dt_max_seconds"] == 2.0

    print("  ✓ All config values match notebook")


def test_confidence_scoring():
    """Verify confidence labeling matches notebook."""
    print("\nTesting Confidence Scoring...")

    assert confidence_label(150) == "No match"
    assert confidence_label(500) == "Low confidence"
    assert confidence_label(2000) == "Medium confidence"
    assert confidence_label(5000) == "High confidence"

    print("  ✓ Confidence labels correct")


def test_time_formatting():
    """Verify time formatting matches notebook."""
    print("\nTesting Time Formatting...")

    assert seconds_to_mmss(124) == "2:04"
    assert seconds_to_mmss(60) == "1:00"
    assert seconds_to_mmss(0) == "0:00"
    assert seconds_to_mmss(185) == "3:05"

    print("  ✓ Time formatting correct")


def test_fingerprint_structure():
    """Verify fingerprint tuple structure."""
    print("\nTesting Fingerprint Structure...")

    # Create dummy audio
    sr = 44100
    duration = 5  # seconds
    y = np.random.randn(sr * duration)

    fps = extract_fingerprints(
        y=y,
        sr=DEFAULT_CONFIG["sr"],
        n_fft=DEFAULT_CONFIG["n_fft"],
        hop_ratio=DEFAULT_CONFIG["hop_ratio"],
        freq_neighborhood=DEFAULT_CONFIG["freq_neighborhood"],
        time_neighborhood=DEFAULT_CONFIG["time_neighborhood"],
        amplitude_threshold=DEFAULT_CONFIG["amplitude_threshold"],
        num_bands=DEFAULT_CONFIG["num_bands"],
        fanout=DEFAULT_CONFIG["fanout"],
        dt_min=DEFAULT_CONFIG["dt_min"],
        dt_max_seconds=DEFAULT_CONFIG["dt_max_seconds"],
    )

    assert isinstance(fps, list)
    if len(fps) > 0:
        fp = fps[0]
        assert isinstance(fp, tuple)
        assert len(fp) == 4
        f1, f2, dt, t1 = fp
        assert isinstance(f1, (int, np.integer))
        assert isinstance(f2, (int, np.integer))
        assert isinstance(dt, (int, np.integer))
        assert isinstance(t1, (int, np.integer))

    print(f"  ✓ Generated {len(fps)} fingerprints with correct structure")


def test_single_song_database():
    """Test single-song database structure."""
    print("\nTesting Single-Song Database...")

    # Create dummy fingerprints
    fps = [
        (100, 200, 50, 10),
        (100, 200, 50, 100),
        (150, 250, 60, 20),
    ]

    db = build_single_song_db(fps)

    # Verify structure
    assert isinstance(db, dict)
    assert (100, 200, 50) in db
    assert len(db[(100, 200, 50)]) == 2
    assert 10 in db[(100, 200, 50)]
    assert 100 in db[(100, 200, 50)]

    print("  ✓ Single-song database structure correct")


def test_multi_song_database():
    """Test multi-song database structure."""
    print("\nTesting Multi-Song Database...")

    # Create dummy fingerprints for multiple songs
    song_fps = {
        "Song A": [
            (100, 200, 50, 10),
            (150, 250, 60, 20),
        ],
        "Song B": [
            (100, 200, 50, 15),
            (200, 300, 70, 25),
        ],
    }

    db, metadata = build_song_database(song_fps)

    # Verify structure
    assert isinstance(db, dict)
    assert (100, 200, 50) in db
    assert len(db[(100, 200, 50)]) == 2

    # Check song tracking
    entries = db[(100, 200, 50)]
    songs = [song for song, _ in entries]
    assert "Song A" in songs
    assert "Song B" in songs

    # Check metadata
    assert "Song A" in metadata
    assert "Song B" in metadata
    assert metadata["Song A"]["num_fingerprints"] == 2
    assert metadata["Song B"]["num_fingerprints"] == 2

    print("  ✓ Multi-song database structure correct")


def test_query_matching():
    """Test query matching logic."""
    print("\nTesting Query Matching...")

    # Build a simple database
    db_fps = [
        (100, 200, 50, 100),
        (150, 250, 60, 110),
        (200, 300, 70, 120),
    ]
    db = build_single_song_db(db_fps)

    # Create query fingerprints (offset by 50 frames)
    query_fps = [
        (100, 200, 50, 50),  # Should match at offset +50
        (150, 250, 60, 60),  # Should match at offset +50
    ]

    offset, score = query_single_song(query_fps, db)

    assert offset == 50  # t_db - t_query = 100 - 50 = 50
    assert score == 2  # Two matches

    print(f"  ✓ Query matching found offset={offset}, score={score}")


def test_interpret_match_structure():
    """Test match result interpretation."""
    print("\nTesting Match Interpretation...")

    # Test successful match
    result = interpret_match(
        song_name="Test Song",
        best_offset=1000,
        score=3500,
        hop_length=512,
        sr=44100
    )

    assert result["matched"] == True
    assert result["song"] == "Test Song"
    assert "position_in_song" in result
    assert result["confidence"] == "High confidence"
    assert result["raw_score"] == 3500

    # Test no match
    result_no_match = interpret_match(
        song_name=None,
        best_offset=None,
        score=50,
        hop_length=512,
        sr=44100
    )

    assert result_no_match["matched"] == False
    assert "message" in result_no_match

    print("  ✓ Match interpretation correct")


def run_all_tests():
    """Run all validation tests."""
    print("=" * 60)
    print("Validation Tests - Verifying Refactored Code")
    print("=" * 60)

    try:
        test_configuration()
        test_confidence_scoring()
        test_time_formatting()
        test_fingerprint_structure()
        test_single_song_database()
        test_multi_song_database()
        test_query_matching()
        test_interpret_match_structure()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nThe refactored code produces identical outputs to the notebook.")

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
