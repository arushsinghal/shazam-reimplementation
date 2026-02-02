# Backend API - Shazam Clone

FastAPI backend for audio fingerprinting and recognition.

## Structure

```
backend/
├── app.py              # Main FastAPI application
├── routes.py           # API endpoint handlers
├── models.py           # Pydantic request/response models
├── service.py          # Business logic layer
└── requirements.txt    # Python dependencies
```

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Running

### Development
```bash
python app.py
```

Server runs on `http://localhost:8000`

### Production
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app:app
```

## API Documentation

When running, visit:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Environment

No environment variables required for basic operation. Optional:

```bash
# Optional: Custom database path
export DB_PATH=/path/to/fingerprint_db.pkl
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `pydantic` - Data validation
- `numpy`, `scipy`, `librosa` - Audio processing
- `soundfile` - Audio file I/O

## Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test with existing songs
curl -X POST "http://localhost:8000/api/songs/add?song_name=Test" \
  -F "file=@../5 Seconds of Summer - Wildflower (Official Video).mp3"
```

## Logging

Backend prints detailed logs to console. For production, configure file logging in `app.py`.

## Performance

- Processes 3-minute songs in ~5-10 seconds
- Recognition typically <2 seconds
- Scales with number of CPU cores (gunicorn workers)

## Security Notes

Development mode has:
- Open CORS for localhost:3000
- No authentication
- No rate limiting

For production, add:
- API key authentication
- Rate limiting (slowapi)
- Restricted CORS
- Request validation

## Database

Fingerprint database auto-saved to `fingerprint_db.pkl`:
- Pickle format (Python)
- Loads on startup
- Saves after each song addition
- ~500KB per minute of audio

## Troubleshooting

**Import errors:**
Ensure you're running from the shazam root directory, not inside backend/:
```bash
cd /Users/arushsinghal/Documents/shazam/backend
python app.py
```

**Module not found:**
The service.py imports core modules from parent directory. This is intentional.

**Port conflict:**
Change port in app.py: `uvicorn.run(..., port=8001)`
