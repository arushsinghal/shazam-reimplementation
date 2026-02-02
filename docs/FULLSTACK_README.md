# Shazam Clone - Full-Stack Application

A production-grade Shazam clone built with classical audio fingerprinting (no ML/neural networks). Features a FastAPI backend and Next.js frontend for a complete consumer product experience.

## 🎯 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐   │
│  │    Home    │  │  Add Songs │  │  Recognize Music   │   │
│  └────────────┘  └────────────┘  └────────────────────┘   │
│                          │                                   │
│                    API Client (axios)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
┌──────────────────────────┴──────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Routes Layer                                          │ │
│  │  POST /api/songs/add                                   │ │
│  │  POST /api/songs/recognize                            │ │
│  │  GET  /api/songs/list                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Service Layer (AudioFingerprintingService)           │ │
│  │  - Database management                                │ │
│  │  - Fingerprint extraction                             │ │
│  │  - Recognition logic                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Core Fingerprinting Engine                           │ │
│  │  - STFT spectrograms                                  │ │
│  │  - Constellation mapping                              │ │
│  │  - Anchor-target hashing                              │ │
│  │  - Offset voting                                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API server
python app.py

# Server runs on http://localhost:8000
```

The backend will:
- Load any existing fingerprint database
- Create a new one if none exists
- Be ready to accept API requests

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev

# Frontend runs on http://localhost:3000
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Add Song to Database
```http
POST /api/songs/add
```

**Parameters:**
- `song_name` (query param): Name of the song
- `file` (form data): Audio file (MP3, WAV, etc.)

**Response:**
```json
{
  "success": true,
  "song_name": "Wildflower",
  "fingerprints_count": 45230,
  "message": "Successfully added Wildflower"
}
```

#### 2. Recognize Song
```http
POST /api/songs/recognize
```

**Parameters:**
- `file` (form data): Audio clip (5-10 seconds recommended)

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
  "raw_score": 0
}
```

#### 3. List All Songs
```http
GET /api/songs/list
```

**Response:**
```json
{
  "songs": [
    {
      "name": "Wildflower",
      "fingerprints_count": 45230,
      "duration_seconds": 245.5
    }
  ],
  "total_songs": 1,
  "total_hashes": 38492
}
```

#### 4. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "songs_count": 1,
  "hashes_count": 38492
}
```

## 🎨 Frontend Features

### Home Page
- Modern gradient design
- Two primary actions: "Recognize Music" and "Add Songs"
- Feature highlights
- Responsive layout

### Add Songs Page
- Drag-and-drop file upload
- Auto-populate song name from filename
- Real-time upload progress
- Success/error feedback
- Displays fingerprint count

### Recognize Page
- Audio clip upload
- Animated "Listening..." state with sound waves
- Clear result display with:
  - Song name
  - Position in song
  - Confidence level (color-coded)
  - Match score
- "Try Another Song" flow

## 🔧 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Librosa** - Audio processing
- **NumPy/SciPy** - Scientific computing
- **Python Multipart** - File upload handling

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

### Fingerprinting Engine
- **STFT** - Spectrogram generation
- **Local Maxima Filtering** - Peak detection
- **Frequency Banding** - Distributed peak selection
- **Anchor-Target Hashing** - Fingerprint generation
- **Offset Voting** - Time-shift invariant matching

## 📁 Project Structure

```
shazam/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── routes.py           # API endpoints
│   ├── models.py           # Pydantic models
│   ├── service.py          # Business logic
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── pages/
│   │   ├── index.tsx       # Home page
│   │   ├── add-songs.tsx   # Add songs page
│   │   └── recognize.tsx   # Recognition page
│   ├── lib/
│   │   └── api.ts          # API client
│   ├── styles/
│   │   └── globals.css     # Global styles
│   └── package.json        # Node dependencies
│
├── Core Modules (unchanged)
│   ├── fingerprinting.py
│   ├── database.py
│   ├── matcher.py
│   ├── utils.py
│   └── config.py
│
└── fingerprint_db.pkl      # Persistent database (auto-created)
```

## 🎯 Usage Workflow

### Building Your Music Database

1. **Start both servers** (backend and frontend)
2. **Navigate to "Add Songs"**
3. **Upload full songs** (MP3, WAV, etc.)
   - Each song is fingerprinted (~1000-3000 fingerprints/second)
   - Database is saved automatically
4. **Repeat** for multiple songs

### Recognizing Music

1. **Navigate to "Recognize Music"**
2. **Upload a 5-10 second clip** from any point in a song
3. **Wait for recognition** (typically <2 seconds)
4. **View results:**
   - Song name
   - Exact position in the song
   - Confidence level
   - Match score

## 🔒 Security & Privacy

- All processing happens **locally**
- No data sent to external services
- Audio files are **temporarily stored** and deleted after processing
- Database is **persisted locally** in `fingerprint_db.pkl`

## ⚡ Performance

- **Recognition Speed**: <2 seconds for typical clips
- **Database Size**: ~500KB per minute of audio
- **Memory Usage**: Database loaded in RAM for fast queries
- **Scalability**: Can handle hundreds of songs efficiently

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in app.py
uvicorn.run("app:app", host="0.0.0.0", port=8001)
```

**Module not found:**
```bash
# Ensure you're in the correct directory
cd /Users/arushsinghal/Documents/shazam/backend
python app.py
```

### Frontend Issues

**API connection failed:**
- Verify backend is running on port 8000
- Check `.env.local` has correct API URL
- Ensure CORS is enabled in backend

**Dependencies error:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## 🚢 Deployment

### Backend (Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

### Frontend (Production)

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Docker (Optional)

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build
CMD ["npm", "start"]
```

## 📊 Confidence Levels

| Score Range | Confidence | Description |
|-------------|------------|-------------|
| < 200 | No match | Not enough matching fingerprints |
| 200-1000 | Low | Possible match, noisy environment |
| 1000-3000 | Medium | Good match, likely correct |
| 3000+ | High | Strong match, very confident |

## 🎓 Algorithm Details

The system uses **classical DSP** (no machine learning):

1. **Spectrogram**: STFT with 2048 samples, 75% overlap
2. **Peak Detection**: Local maxima in 6 frequency bands
3. **Fingerprints**: Anchor-target pairs with time delta
4. **Hashing**: (f1, f2, dt) → unique fingerprint hash
5. **Matching**: Histogram-based offset voting

**Time-shift invariant**: Recognizes songs regardless of where the clip starts.

## 🤝 Contributing

This is a complete, production-ready implementation. To extend:

- Add database persistence (PostgreSQL, Redis)
- Implement batch processing
- Add audio recording from microphone
- Build mobile apps (React Native)
- Add playlist management
- Implement user authentication

## 📄 License

Educational/research project. Core algorithm based on Shazam's original paper (Wang, 2003).

## 🙏 Acknowledgments

- **Avery Wang** - Original Shazam algorithm
- **Librosa** - Audio processing library
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework

---

**Built with classical DSP - no ML models, just pure signal processing magic!** 🎵
