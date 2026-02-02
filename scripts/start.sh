#!/bin/bash

echo "================================================"
echo "   Shazam Clone - Full Stack Application"
echo "================================================"
echo ""

# Check if running from the correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the shazam directory"
    exit 1
fi

echo "🔧 Setting up Backend..."
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed"
else
    echo "⚠️  Some backend dependencies may have failed to install"
fi

# Start backend in background
echo "🚀 Starting backend server..."
python3 app.py &
BACKEND_PID=$!
echo "✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 3

cd ../frontend

echo ""
echo "🔧 Setting up Frontend..."

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    kill $BACKEND_PID
    exit 1
fi

# Install frontend dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies (this may take a few minutes)..."
    npm install > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ Frontend dependencies installed"
    else
        echo "❌ Frontend dependencies installation failed"
        kill $BACKEND_PID
        exit 1
    fi
else
    echo "✅ Frontend dependencies already installed"
fi

# Start frontend
echo "🚀 Starting frontend server..."
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"

echo ""
echo "================================================"
echo "✅ Application is running!"
echo "================================================"
echo ""
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; echo '✅ Servers stopped'; exit 0" INT

# Keep script running
wait
