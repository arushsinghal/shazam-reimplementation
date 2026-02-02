# Project Structure

```
shazam/
├── README.md                 # Main documentation
├── config.py                 # Configuration parameters
├── fingerprinting.py         # Core fingerprinting (STFT, peaks, fingerprints)
├── database.py               # Hash database creation and storage
├── matcher.py                # Query matching via offset voting
├── utils.py                  # Helper functions (confidence, formatting)
├── main.py                   # High-level API and orchestration
├── example.py                # Usage examples
├── test_validation.py        # Validation tests
├── untitled15.py            # Original notebook code (reference)
└── Untitled15.ipynb         # Original Jupyter notebook (reference)
```

## Module Responsibilities

### Core Modules

**fingerprinting.py**
- `extract_fingerprints()`: Complete fingerprinting pipeline
- `load_audio()`: Audio file loading
- STFT computation
- Banded peak detection
- Anchor-target fingerprint generation

**database.py**
- `build_song_database()`: Multi-song database creation
- `build_single_song_db()`: Single-song database creation
- Hash-based storage structure

**matcher.py**
- `query_single_song()`: Single-song matching
- `query_multi_song()`: Multi-song matching
- `recognize_audio()`: High-level recognition
- Offset voting algorithm

**utils.py**
- `confidence_label()`: Score → confidence string
- `seconds_to_mmss()`: Time formatting
- `interpret_match()`: Result structuring

**config.py**
- `DEFAULT_CONFIG`: All algorithm parameters
- `validate_config()`: Configuration validation
- Parameter documentation

### Application Layer

**main.py**
- `build_database_from_files()`: Build DB from audio files
- `recognize_from_file()`: Recognize from file path
- `recognize_from_audio()`: Recognize from audio array
- Main entry point

**example.py**
- Example usage patterns
- Single-song workflow demonstration
- Query testing

**test_validation.py**
- Unit tests for all modules
- Validates refactored code matches notebook behavior
- Ensures no regressions

## Design Principles

1. **Modularity**: Each file has a single, clear responsibility
2. **Type Safety**: Type hints on all public functions
3. **Documentation**: Docstrings explain intent and algorithm
4. **No Global State**: Configuration passed explicitly
5. **Testability**: Functions are pure and easily testable
6. **Extensibility**: Designed for API integration

## API Layers

### Layer 1: Core Algorithm (fingerprinting.py, database.py, matcher.py)
- Pure functions implementing the algorithm
- No I/O, no side effects
- Reusable across different interfaces

### Layer 2: Utilities (utils.py, config.py)
- Helper functions
- Configuration management
- Result formatting

### Layer 3: Application (main.py)
- Combines core modules
- Handles file I/O
- Provides high-level API

### Layer 4: Examples/Tests (example.py, test_validation.py)
- Usage demonstrations
- Validation and testing

## Data Flow

```
Audio File
    ↓
load_audio()
    ↓
Audio Array (numpy)
    ↓
extract_fingerprints()
    ↓
Fingerprints: [(f1, f2, dt, t1), ...]
    ↓
build_song_database()
    ↓
Database: {(f1, f2, dt): [(song, time), ...]}
    ↓
query_multi_song()
    ↓
(song_name, offset, score)
    ↓
interpret_match()
    ↓
Match Result Dict
```

## Extension Points

### Adding Persistence
```python
# database.py
def save_database(db, filepath):
    import pickle
    with open(filepath, 'wb') as f:
        pickle.dump(db, f)

def load_database(filepath):
    import pickle
    with open(filepath, 'rb') as f:
        return pickle.load(f)
```

### Building a REST API
```python
# api.py
from fastapi import FastAPI, UploadFile
from main import recognize_from_audio, GLOBAL_DB
import librosa, io

app = FastAPI()

@app.post("/recognize")
async def recognize(file: UploadFile):
    audio = await file.read()
    y, sr = librosa.load(io.BytesIO(audio), sr=44100, mono=True)
    return recognize_from_audio(y, GLOBAL_DB)
```

### Custom Configuration
```python
# custom_config.py
from config import get_config

my_config = get_config()
my_config["amplitude_threshold"] = -40  # More sensitive
my_config["fanout"] = 15  # More fingerprints per anchor

from main import build_database_from_files
db, _ = build_database_from_files(files, config=my_config)
```

## Migration from Notebook

The refactoring preserves all algorithm logic while removing:
- Notebook-specific imports (`IPython.display`, `google.colab`)
- Visualization code (`matplotlib`, `plt.show()`)
- Interactive elements (`files.upload()`)
- Exploratory prints and experiments
- Global variables

All functional code is preserved with identical behavior.
