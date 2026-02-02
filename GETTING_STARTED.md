# 🚀 Getting Started - Shazam Clone

Welcome! This guide will get you up and running in minutes.

## What You'll Build

A complete Shazam-like application with:
- 🎵 Add songs to your personal music database
- 🔍 Recognize songs from short audio clips
- 💻 Beautiful web interface
- ⚡ Lightning-fast recognition (<2 seconds)

---

## Prerequisites

Make sure you have:
- ✅ Python 3.9 or higher
- ✅ Node.js 18 or higher
- ✅ 2GB free disk space
- ✅ Internet connection (for package installation)

Check versions:
```bash
python3 --version
node --version
npm --version
```

---

## 📥 Step 1: Get the Code

You already have it! The project is in:
```
/Users/arushsinghal/Documents/shazam
```

Navigate there:
```bash
cd /Users/arushsinghal/Documents/shazam
```

---

## 🚀 Step 2: One-Command Start

The easiest way:

```bash
./start.sh
```

This automatically:
1. ✅ Installs backend dependencies
2. ✅ Starts backend server (port 8000)
3. ✅ Installs frontend dependencies
4. ✅ Starts frontend server (port 3000)

**Wait for:**
```
✅ Application is running!
   Frontend: http://localhost:3000
   Backend:  http://localhost:8000
```

Then open your browser to: **http://localhost:3000**

---

## 🎯 Step 3: Add Your First Song

You have sample songs already! Let's add one:

### Via Web Interface (Recommended)

1. Click **"Add Songs"** on the home page
2. Click the upload area
3. Select: `5 Seconds of Summer - Wildflower (Official Video).mp3`
4. Enter song name: `Wildflower`
5. Click **"Add to Database"**
6. Wait ~10 seconds for processing
7. You should see success message!

### Via Command Line (Alternative)

```bash
curl -X POST \
  "http://localhost:8000/api/songs/add?song_name=Wildflower" \
  -F "file=@5 Seconds of Summer - Wildflower (Official Video).mp3"
```

---

## 🔍 Step 4: Test Recognition

Now let's recognize a clip!

### Via Web Interface (Recommended)

1. Go back to home page
2. Click **"Recognize Music"**
3. Upload the trimmed file: `5 Seconds of Summer - Wildflower (Official Video)-trimmed.mp3`
4. Click **"Identify Song"**
5. Watch the animated "Listening..." state
6. See the result! Should match "Wildflower"

### Via Command Line (Alternative)

```bash
curl -X POST \
  http://localhost:8000/api/songs/recognize \
  -F "file=@5 Seconds of Summer - Wildflower (Official Video)-trimmed.mp3"
```

---

## ✨ Step 5: Explore the Features

### Add More Songs

Add the other sample song:
```bash
curl -X POST \
  "http://localhost:8000/api/songs/add?song_name=Sunflower" \
  -F "file=@Post_Malone_Swae_Lee_-_Sunflower_2018_(mp3.pm).mp3"
```

### View Your Database

Via web: Check the home page for stats

Via API:
```bash
curl http://localhost:8000/api/songs/list
```

### Check System Health

```bash
curl http://localhost:8000/api/health
```

---

## 🎨 Understanding the Interface

### Home Page
- **Gradient design** with two action cards
- **Feature highlights** at the bottom
- **Fully responsive** - works on mobile too!

### Add Songs Page
- **Drag & drop** or click to upload
- **Auto-fills** song name from filename
- **Real-time feedback** on processing
- **Shows fingerprint count** on success

### Recognize Page
- **Animated sound waves** during processing
- **Color-coded confidence**:
  - 🟢 Green = High confidence
  - 🟡 Yellow = Medium confidence
  - 🟠 Orange = Low confidence
- **Shows exact position** in song (MM:SS format)
- **Match score** (number of matching fingerprints)

---

## 🔧 Troubleshooting

### Backend won't start

**Issue:** Port 8000 already in use

**Fix:**
```bash
lsof -ti:8000 | xargs kill -9
./start.sh
```

### Frontend won't start

**Issue:** Port 3000 already in use

**Fix:**
```bash
lsof -ti:3000 | xargs kill -9
cd frontend && npm run dev
```

### Can't connect to backend

**Check if backend is running:**
```bash
curl http://localhost:8000/api/health
```

Should return: `{"status":"healthy",...}`

If not, restart:
```bash
cd backend
python app.py
```

### Recognition not working

**Possible causes:**
1. ✅ No songs in database - add songs first!
2. ✅ Clip too short - use 5+ seconds
3. ✅ Wrong audio format - use MP3/WAV
4. ✅ Too noisy - use cleaner audio

**Check database:**
```bash
curl http://localhost:8000/api/songs/list
```

Should show your songs.

---

## 📚 Next Steps

### 1. Add Your Own Music

Upload your own MP3 files:
1. Go to "Add Songs" page
2. Select your MP3 file
3. Enter the song name
4. Wait for processing

### 2. Create Test Clips

Extract a 6-second clip from a song:

**Using FFmpeg:**
```bash
ffmpeg -i song.mp3 -ss 60 -t 6 clip.mp3
```

This extracts 6 seconds starting at 1:00.

**Using online tools:**
- mp3cut.net
- audiotrimmer.com

### 3. Test with Different Clips

Try clips from:
- Different parts of the song
- Different audio quality
- With background noise
- Different formats (WAV, FLAC, etc.)

### 4. Explore the API

Open interactive docs:
```
http://localhost:8000/docs
```

Try the endpoints directly from the browser!

### 5. Read the Documentation

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete overview
- [API_CONTRACT.md](API_CONTRACT.md) - Full API spec
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design

---

## 🎓 How It Works (Simple Explanation)

### Adding Songs (Fingerprinting)

1. **Load audio** - Convert to 44.1kHz mono
2. **Create spectrogram** - Visual representation of frequencies over time
3. **Find peaks** - Identify prominent frequency points
4. **Generate fingerprints** - Create unique hashes from peak patterns
5. **Store in database** - Save with song name and time position

**Result:** ~1000-3000 fingerprints per second of audio

### Recognizing Songs (Matching)

1. **Process query clip** - Same steps as above
2. **Match against database** - Find matching fingerprints
3. **Vote on offsets** - Calculate time alignment
4. **Best match wins** - Song with most votes

**Result:** Song name + exact position in <2 seconds

### Why It's Fast

- **Hash-based lookup** - O(1) fingerprint matching
- **Parallel processing** - Multiple workers
- **In-memory database** - No disk I/O during queries
- **Efficient algorithm** - Only processes peaks, not full audio

---

## 💡 Tips & Tricks

### Best Practices

**For Adding Songs:**
- ✅ Use good quality audio (128kbps+ MP3)
- ✅ Full songs work best (not clips)
- ✅ Unique song names avoid confusion
- ✅ One at a time for stability

**For Recognition:**
- ✅ 5-10 second clips are ideal
- ✅ Clip from middle of song works best
- ✅ Minimize background noise
- ✅ Match audio quality to database

### Performance Optimization

**Speed up processing:**
```python
# Edit config.py
CONFIG = {
    "fanout": 5,  # Reduce from 10
    "num_bands": 4,  # Reduce from 6
}
```

**Trade-off:** Fewer fingerprints = faster but less accurate

### Database Management

**Backup database:**
```bash
cp fingerprint_db.pkl fingerprint_db_backup.pkl
```

**Clear database:**
```bash
rm fingerprint_db.pkl
# Restart backend - creates new empty database
```

**View database size:**
```bash
ls -lh fingerprint_db.pkl
```

---

## 🎉 You're All Set!

You now have a **fully functional Shazam clone** running locally!

### What you can do:
- ✅ Add unlimited songs
- ✅ Recognize clips from anywhere in the song
- ✅ See exactly where in the song the clip is from
- ✅ Get confidence scores for matches
- ✅ Use the beautiful web interface
- ✅ Access the REST API programmatically

### Share Your Results

Tweet about it with #ShazamClone or share screenshots!

---

## 🆘 Need Help?

1. **Check logs** - Backend prints detailed information
2. **Review docs** - See documentation folder
3. **Test with curl** - Isolate frontend vs backend issues
4. **Restart everything** - Stop servers and run `./start.sh` again

### Quick Diagnostics

```bash
# Is backend running?
curl http://localhost:8000/api/health

# Is frontend running?
curl http://localhost:3000

# Check database
curl http://localhost:8000/api/songs/list

# View backend logs
# (Check terminal where backend is running)
```

---

## 🚀 Ready to Deploy?

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Production deployment
- Docker setup
- AWS/DigitalOcean guides
- SSL configuration
- Performance tuning

---

## 🎊 Congratulations!

You've successfully set up and tested a production-grade Shazam clone!

**Next challenge:** Deploy it to the cloud and share with friends! 🌍

---

**Happy music recognition!** 🎵✨
