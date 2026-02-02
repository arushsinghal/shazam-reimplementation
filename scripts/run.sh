#!/bin/bash

echo "🚀 Starting Shazam Clone Application"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

echo "📦 Installing/checking backend dependencies..."
pip install fastapi uvicorn python-multipart pydantic numpy scipy librosa soundfile -q

echo ""
echo "🔧 Starting Backend Server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   API running on http://localhost:8000"
echo ""

# Wait for backend to be ready
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend may still be starting up..."
fi

echo ""
echo "🎨 Starting Frontend Server..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies (this may take a few minutes)..."
    npm install
fi

echo ""
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   UI running on http://localhost:3000"
echo ""
echo "================================================"
echo "✅ Application is fully running!"
echo "================================================"
echo ""
echo "   🌐 Frontend: http://localhost:3000"
echo "   🔧 Backend:  http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Handle cleanup
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Servers stopped'; exit 0" INT TERM

# Keep script running
wait
