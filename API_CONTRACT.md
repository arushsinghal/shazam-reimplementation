# API Contract

Complete API specification for the Shazam Clone application.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

Currently no authentication required. Add API keys or JWT tokens for production.

## Content Types

- Request: `multipart/form-data` for file uploads
- Response: `application/json`

## Error Handling

All errors return consistent structure:

```json
{
  "detail": "Error message here"
}
```

HTTP Status Codes:
- `200`: Success
- `400`: Bad Request (validation error)
- `422`: Unprocessable Entity
- `500`: Internal Server Error

---

## Endpoints

### 1. Health Check

Check if the API is running and get database stats.

**Endpoint:** `GET /api/health`

**Request:** None

**Response:**
```json
{
  "status": "healthy",
  "songs_count": 5,
  "hashes_count": 125834
}
```

**Example (curl):**
```bash
curl http://localhost:8000/api/health
```

**Example (JavaScript):**
```javascript
const response = await fetch('http://localhost:8000/api/health');
const data = await response.json();
console.log(data.songs_count);
```

---

### 2. Add Song

Add a new song to the fingerprint database.

**Endpoint:** `POST /api/songs/add`

**Request:**
- **Query Parameters:**
  - `song_name` (required): Name of the song
- **Form Data:**
  - `file` (required): Audio file (MP3, WAV, FLAC, etc.)

**Response:**
```json
{
  "success": true,
  "song_name": "Wildflower",
  "fingerprints_count": 45230,
  "message": "Successfully added Wildflower"
}
```

**Error Response:**
```json
{
  "detail": "Error adding song: Invalid audio format"
}
```

**Example (curl):**
```bash
curl -X POST \
  "http://localhost:8000/api/songs/add?song_name=Wildflower" \
  -F "file=@/path/to/song.mp3"
```

**Example (JavaScript/FormData):**
```javascript
const formData = new FormData();
formData.append('file', audioFile);

const response = await fetch(
  'http://localhost:8000/api/songs/add?song_name=Wildflower',
  {
    method: 'POST',
    body: formData,
  }
);

const data = await response.json();
console.log(`Added with ${data.fingerprints_count} fingerprints`);
```

**Processing Time:**
- Depends on song length
- ~5-10 seconds for a 3-minute song
- Progress not currently streamed (future enhancement)

**Notes:**
- Song names should be unique (or will overwrite)
- Supports all formats supported by librosa
- Automatically converts to mono @ 44.1kHz
- Database is automatically saved to disk

---

### 3. Recognize Song

Recognize a song from an audio clip.

**Endpoint:** `POST /api/songs/recognize`

**Request:**
- **Form Data:**
  - `file` (required): Audio clip (5-10 seconds recommended)

**Response (Match Found):**
```json
{
  "matched": true,
  "song": "Wildflower",
  "position_in_song": "2:04",
  "confidence": "High confidence",
  "raw_score": 3847
}
```

**Response (No Match):**
```json
{
  "matched": false,
  "message": "No matching song detected",
  "raw_score": 150
}
```

**Confidence Levels:**
- `"High confidence"`: raw_score >= 3000
- `"Medium confidence"`: raw_score >= 1000
- `"Low confidence"`: raw_score >= 200
- `"No match"`: raw_score < 200

**Example (curl):**
```bash
curl -X POST \
  http://localhost:8000/api/songs/recognize \
  -F "file=@/path/to/clip.mp3"
```

**Example (JavaScript/Axios):**
```javascript
import axios from 'axios';

const formData = new FormData();
formData.append('file', audioClip);

const response = await axios.post(
  'http://localhost:8000/api/songs/recognize',
  formData,
  {
    headers: { 'Content-Type': 'multipart/form-data' }
  }
);

if (response.data.matched) {
  console.log(`Found: ${response.data.song} at ${response.data.position_in_song}`);
} else {
  console.log('No match found');
}
```

**Processing Time:**
- Typically 1-3 seconds
- Depends on clip length and database size

**Best Practices:**
- Use 5-10 second clips for best results
- Avoid clips that are too short (<3 seconds)
- Ensure reasonable audio quality
- Minimize background noise

---

### 4. List Songs

Get list of all songs in the database.

**Endpoint:** `GET /api/songs/list`

**Request:** None

**Response:**
```json
{
  "songs": [
    {
      "name": "Wildflower",
      "fingerprints_count": 45230,
      "duration_seconds": 245.5
    },
    {
      "name": "Sunflower",
      "fingerprints_count": 38492,
      "duration_seconds": 198.3
    }
  ],
  "total_songs": 2,
  "total_hashes": 67234
}
```

**Example (curl):**
```bash
curl http://localhost:8000/api/songs/list
```

**Example (JavaScript):**
```javascript
const response = await fetch('http://localhost:8000/api/songs/list');
const data = await response.json();

data.songs.forEach(song => {
  console.log(`${song.name}: ${song.fingerprints_count} fingerprints`);
});
```

---

### 5. Root Info

Get API information and available endpoints.

**Endpoint:** `GET /`

**Request:** None

**Response:**
```json
{
  "message": "Shazam Clone API",
  "version": "1.0.0",
  "endpoints": {
    "add_song": "POST /api/songs/add",
    "recognize": "POST /api/songs/recognize",
    "list_songs": "GET /api/songs/list",
    "health": "GET /api/health"
  }
}
```

---

## Data Models

### Song

```typescript
interface Song {
  name: string;
  fingerprints_count: number;
  duration_seconds?: number;  // May be null for old entries
}
```

### Recognition Result

```typescript
interface RecognitionResult {
  matched: boolean;
  song?: string;              // Present if matched
  position_in_song?: string;  // Format: "M:SS"
  confidence?: string;        // "High confidence", "Medium confidence", etc.
  raw_score?: number;         // Number of matching fingerprints
  message?: string;           // Present if not matched
}
```

### Add Song Response

```typescript
interface AddSongResponse {
  success: boolean;
  song_name: string;
  fingerprints_count: number;
  message: string;
}
```

---

## Rate Limiting

Currently no rate limiting. Recommendations for production:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/songs/recognize")
@limiter.limit("10/minute")
async def recognize_song(...):
    ...
```

---

## CORS Configuration

Current CORS settings (development):

```python
allow_origins=["http://localhost:3000", "http://localhost:3001"]
allow_methods=["*"]
allow_headers=["*"]
```

For production, restrict to your domain:

```python
allow_origins=["https://your-domain.com"]
```

---

## WebSocket Support (Future)

For real-time microphone recognition:

```
ws://localhost:8000/ws/recognize
```

Send audio chunks → Receive recognition results

---

## Client Libraries

### Python

```python
import requests

# Add song
files = {'file': open('song.mp3', 'rb')}
params = {'song_name': 'My Song'}
response = requests.post('http://localhost:8000/api/songs/add', files=files, params=params)

# Recognize
files = {'file': open('clip.mp3', 'rb')}
response = requests.post('http://localhost:8000/api/songs/recognize', files=files)
print(response.json())
```

### JavaScript/TypeScript

See `frontend/lib/api.ts` for complete client implementation.

### cURL

See examples above for each endpoint.

---

## Testing

### Manual Testing

```bash
# Test health
curl http://localhost:8000/api/health

# Add a song
curl -X POST \
  "http://localhost:8000/api/songs/add?song_name=Test" \
  -F "file=@test.mp3"

# Recognize
curl -X POST \
  http://localhost:8000/api/songs/recognize \
  -F "file=@clip.mp3"
```

### Automated Testing

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_add_song():
    files = {"file": ("test.mp3", open("test.mp3", "rb"), "audio/mpeg")}
    params = {"song_name": "Test Song"}
    response = client.post("/api/songs/add", files=files, params=params)
    assert response.status_code == 200
    assert response.json()["success"] == True
```

---

## Performance Metrics

### Add Song
- **Input:** 3-minute song (MP3, ~3MB)
- **Processing:** 5-10 seconds
- **Output:** ~45,000 fingerprints
- **Database growth:** ~500KB

### Recognize
- **Input:** 6-second clip
- **Processing:** 1-3 seconds
- **Database query:** O(query_fingerprints × hash_lookups)
- **Typical response:** <2 seconds

### Database
- **In-memory:** Fast lookups
- **Disk persistence:** Pickle format
- **Size:** ~500KB per minute of audio

---

## Security Considerations

### Production Checklist

- [ ] Enable HTTPS
- [ ] Add authentication (API keys or JWT)
- [ ] Implement rate limiting
- [ ] Validate file types and sizes
- [ ] Sanitize song names
- [ ] Add request logging
- [ ] Configure CORS properly
- [ ] Add file size limits
- [ ] Implement request timeouts
- [ ] Add input validation

### File Upload Security

```python
# Max file size
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Allowed extensions
ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}

def validate_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file type")
```

---

## Versioning

Current: `v1.0.0`

Future versions will maintain backwards compatibility:
- `v1.x.x`: Backwards compatible features
- `v2.x.x`: Breaking changes

API path: `/api/...` (can add `/api/v2/...` later)

---

## Support

For issues or questions:
1. Check logs: Backend prints detailed info
2. Test with curl first
3. Verify file formats are supported
4. Ensure database has songs before recognizing
