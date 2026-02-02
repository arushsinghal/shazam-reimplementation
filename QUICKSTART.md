# Quick Start Guide

## Installation

```bash
# Navigate to project
cd /Users/arushsinghal/Documents/shazam

# Install dependencies (already done with uv)
# Dependencies: numpy, scipy, librosa, soundfile
```

## Verify Installation

```bash
python3 test_validation.py
```

Expected output:
```
============================================================
✓ ALL TESTS PASSED
============================================================
```

## Basic Usage

### 1. Single Song Recognition

```python
from main import CONFIG, recognize_from_audio
from fingerprinting import load_audio, extract_fingerprints
from database import build_single_song_db

# Load full song
y_full, sr = load_audio("5 Seconds of Summer - Wildflower (Official Video).mp3", CONFIG["sr"])

# Build database
fingerprints = extract_fingerprints(y_full, sr, **CONFIG)
db = build_single_song_db(fingerprints)

# Test with a clip (60-66 seconds)
y_clip = y_full[60*sr:66*sr]
result = recognize_from_audio(y_clip, db, song_name_hint="Wildflower")

print(result)
# {
#   'matched': True,
#   'song': 'Wildflower',
#   'position_in_song': '1:00',
#   'confidence': 'High confidence',
#   'raw_score': 3500+
# }
```

### 2. Multi-Song Database

```python
from main import build_database_from_files, recognize_from_file

# Build database from multiple songs
audio_files = {
    "Wildflower": "5 Seconds of Summer - Wildflower (Official Video).mp3",
    "Sunflower": "Post_Malone_Swae_Lee_-_Sunflower_2018_(mp3.pm).mp3",
}

db, metadata = build_database_from_files(audio_files)

# Recognize a clip
result = recognize_from_file("query_clip.mp3", db)
print(result)
```

### 3. Using Existing Audio Files

You already have audio files in the workspace:
- `5 Seconds of Summer - Wildflower (Official Video).mp3`
- `5 Seconds of Summer - Wildflower (Official Video)-trimmed.mp3`
- `Post_Malone_Swae_Lee_-_Sunflower_2018_(mp3.pm).mp3`

Try this:

```python
from main import build_database_from_files, recognize_from_file

# Build database
db, metadata = build_database_from_files({
    "Wildflower": "5 Seconds of Summer - Wildflower (Official Video).mp3"
})

# Query with trimmed version
result = recognize_from_file(
    "5 Seconds of Summer - Wildflower (Official Video)-trimmed.mp3",
    db
)

print(result)
```

## Module Import Examples

```python
# Low-level API
from fingerprinting import extract_fingerprints, load_audio
from database import build_song_database
from matcher import query_multi_song
from utils import interpret_match
from config import DEFAULT_CONFIG

# High-level API (recommended)
from main import (
    build_database_from_files,
    recognize_from_file,
    recognize_from_audio
)
```

## Common Patterns

### Pattern 1: Build DB Once, Query Many Times

```python
from main import build_database_from_files, recognize_from_file

# Build once
db, _ = build_database_from_files({
    "Song A": "a.mp3",
    "Song B": "b.mp3",
})

# Query multiple times
for query_file in ["clip1.mp3", "clip2.mp3", "clip3.mp3"]:
    result = recognize_from_file(query_file, db)
    print(f"{query_file}: {result['song']}")
```

### Pattern 2: Working with Audio Arrays

```python
from main import recognize_from_audio
import librosa

# Load with custom processing
y, sr = librosa.load("audio.mp3", sr=44100, mono=True)

# Add preprocessing if needed
# y = apply_noise_reduction(y)

# Recognize
result = recognize_from_audio(y, db)
```

### Pattern 3: Persistence

```python
import pickle

# Save database
with open("database.pkl", "wb") as f:
    pickle.dump(db, f)

# Load database
with open("database.pkl", "rb") as f:
    db = pickle.load(f)
```

## Next Steps

1. **Run validation tests**: `python3 test_validation.py`
2. **Try example script**: Edit `example.py` with your audio paths
3. **Build your database**: Use songs from the workspace
4. **Read ARCHITECTURE.md**: Understand the design
5. **Explore API integration**: See README.md for FastAPI example

## Troubleshooting

### No matches found
- Ensure audio is clean (minimal background noise)
- Try longer clips (6+ seconds recommended)
- Check that audio formats match (both should be same quality)

### Low confidence matches
- Query clip may be too short
- High background noise in query
- Different audio quality/encoding

### Memory issues
- Large databases consume RAM
- Consider chunking song files
- Use persistence (pickle) to avoid rebuilding

## Configuration Tuning

**Do not modify these unless you know what you're doing:**

```python
from config import get_config

config = get_config()
# config["amplitude_threshold"] = -40  # More sensitive peaks
# config["fanout"] = 15  # More fingerprints per anchor
```

Changes affect:
- Recognition accuracy
- Database size
- Query speed
- False positive rate

## Performance Tips

- **Preprocessing**: Normalize audio to prevent amplitude issues
- **Sampling rate**: All audio should use same sample rate (44.1kHz)
- **Database size**: ~500KB per minute of audio
- **Query time**: Typically <100ms for 6-second clip
