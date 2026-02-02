# Audio Fingerprinting System (Shazam-style)

A production-grade Python implementation of audio fingerprinting for music recognition, using STFT spectrograms, constellation mapping, and offset voting.

## Overview

This system implements the core algorithm behind audio recognition services like Shazam:

1. **Spectrogram Analysis**: Compute Short-Time Fourier Transform (STFT) to convert audio into a time-frequency representation
2. **Constellation Mapping**: Extract local spectral peaks using frequency-banded maximum filtering
3. **Fingerprint Generation**: Create anchor-target pairs with fan-out pattern and time-delta constraints
4. **Hash Database**: Store fingerprints as hashes `(f1, f2, dt)` → song/time pairs
5. **Offset Voting**: Match query audio by voting on time-shift alignments

The algorithm is **time-shift invariant** — it can recognize a song regardless of where the query clip starts.

## Architecture

```
├── fingerprinting.py    # STFT, peak detection, fingerprint extraction
├── database.py          # Hash database creation and storage
├── matcher.py           # Query matching via offset voting
├── utils.py             # Confidence scoring and time formatting
└── main.py              # High-level API and orchestration
```

## Installation

```bash
# Install dependencies
uv add numpy scipy librosa soundfile

# Or with pip
pip install numpy scipy librosa soundfile
```

## Usage

### Building a Database

```python
from main import build_database_from_files

# Build database from audio files
audio_files = {
    "Wildflower – 5 Seconds of Summer": "path/to/wildflower.mp3",
    "Another Song": "path/to/another.mp3",
}

db, metadata = build_database_from_files(audio_files)
print(f"Database contains {len(db)} unique hashes")
```

### Recognizing Audio

```python
from main import recognize_from_file

# Query with an audio clip
result = recognize_from_file("query_clip.mp3", db)

print(result)
# {
#   "matched": True,
#   "song": "Wildflower – 5 Seconds of Summer",
#   "position_in_song": "2:04",
#   "confidence": "High confidence",
#   "raw_score": 3847
# }
```

### Working with Audio Arrays

```python
from main import recognize_from_audio
import librosa

# Load audio as numpy array
y_query, sr = librosa.load("clip.mp3", sr=44100, mono=True)

# Recognize
result = recognize_from_audio(y_query, db)
print(result)
```

## Configuration

The fingerprinting parameters are defined in `main.CONFIG`:

```python
CONFIG = {
    "sr": 44100,                    # Sampling rate
    "n_fft": 2048,                  # FFT window size (~46ms at 44.1kHz)
    "hop_ratio": 4,                 # Hop = n_fft / 4 (~11ms steps)
    "freq_neighborhood": 20,        # Frequency bins for peak detection
    "time_neighborhood": 20,        # Time frames for peak detection
    "amplitude_threshold": -35,     # Minimum peak amplitude (dB)
    "num_bands": 6,                 # Frequency bands for peak distribution
    "fanout": 10,                   # Max targets per anchor
    "dt_min": 2,                    # Min time delta (frames)
    "dt_max_seconds": 2.0,          # Max time delta (seconds)
}
```

**Do not modify these values** unless you understand their impact on the fingerprinting algorithm.

## Algorithm Details

### 1. Spectrogram Computation
- Uses STFT with 2048-sample window (~46ms at 44.1kHz)
- 75% overlap (512-sample hop)
- Converts to dB scale for uniform amplitude comparison

### 2. Peak Detection
- Divides frequency axis into 6 bands to ensure peak distribution
- Applies local maximum filtering (20×20 neighborhood)
- Filters peaks below -35dB threshold
- Produces "constellation map" of spectral landmarks

### 3. Fingerprint Generation
- For each peak (anchor), looks forward in time
- Pairs with up to 10 target peaks within 2 seconds
- Creates fingerprints: `(f1, f2, dt, t1)`
  - `f1`: anchor frequency bin
  - `f2`: target frequency bin
  - `dt`: time delta in frames
  - `t1`: absolute anchor time

### 4. Hash Database
- Hashes fingerprints by `(f1, f2, dt)`
- Stores: `hash → [(song_name, time_offset), ...]`
- Supports multiple songs in same database

### 5. Offset Voting
- For each query fingerprint, looks up matches in database
- Computes time offset: `offset = t_db - t_query`
- Votes on `(song_name, offset)` pairs
- Best match = highest vote count

## Confidence Scoring

Match confidence is based on the raw score (number of matching fingerprints):

- **< 200**: No match
- **200–1000**: Low confidence
- **1000–3000**: Medium confidence
- **≥ 3000**: High confidence

## Extensibility

### Multi-Song Database
The system natively supports multiple songs:

```python
db, metadata = build_database_from_files({
    "Song A": "a.mp3",
    "Song B": "b.mp3",
    "Song C": "c.mp3",
})

result = recognize_from_file("query.mp3", db)
# Automatically identifies which song matches
```

### API Integration
The modules are designed for easy API wrapping:

```python
from fastapi import FastAPI, UploadFile
from main import recognize_from_audio
import librosa
import io

app = FastAPI()

@app.post("/recognize")
async def recognize(file: UploadFile):
    audio_bytes = await file.read()
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=44100, mono=True)
    result = recognize_from_audio(y, GLOBAL_DB)
    return result
```

## Performance Characteristics

- **Fingerprint Density**: ~1000–3000 fingerprints per second of audio
- **Database Size**: ~500KB per minute of audio (depends on content)
- **Query Time**: O(query_fingerprints × avg_hash_collisions)
- **Memory**: Hash database stored in-memory as Python dict

## Limitations

- Requires relatively clean audio (low noise)
- Short clips (<5 seconds) may have insufficient fingerprints
- No pitch-shift or time-stretch invariance
- Database must fit in memory

## License

This is a research/educational implementation. For production use, consider:
- Persistent database (e.g., Redis, PostgreSQL)
- Batch fingerprint extraction
- Fingerprint compression
- Distributed matching

## References

- **Original Paper**: Wang, A. (2003). "An Industrial-Strength Audio Search Algorithm" (Shazam)
- **Librosa**: McFee et al. (2015). "librosa: Audio and Music Signal Analysis in Python"

---

**Note**: This implementation preserves the exact algorithm from the research notebook. All thresholds, parameters, and logic are unchanged to maintain bit-for-bit compatibility.
