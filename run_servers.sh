#!/bin/bash

set -euo pipefail

# PopSyn Development Server Launcher
# This script starts both the FastAPI backend and Astro frontend servers

echo "🎵 Starting PopSyn development servers..."
echo ""

# Function to cleanup background processes on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill ${BACKEND_PID:-0} ${FRONTEND_PID:-0} 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Parse flags
SKIP_BACKEND=0
if [[ "${1:-}" == "--frontend-only" ]]; then
  SKIP_BACKEND=1
fi

# Check if uv is installed (optional now)
if ! command -v uv &> /dev/null; then
    if [[ $SKIP_BACKEND -eq 0 ]]; then
      echo "⚠️  uv not found. Backend will be skipped. To install uv:"
      echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    fi
    SKIP_BACKEND=1
fi

# Check if Node.js and npm are installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js first."
    exit 1
fi
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install npm first."
    exit 1
fi

# Start FastAPI backend
if [[ $SKIP_BACKEND -eq 0 ]]; then
  echo "🚀 Starting FastAPI backend on http://127.0.0.1:8000"
  pushd fastapi-backend >/dev/null
  uv sync
  uv run fastapi dev main.py --host 127.0.0.1 --port 8000 &
  BACKEND_PID=$!
  popd >/dev/null
  # Wait a moment for backend to start
  sleep 2
else
  echo "⏭️  Skipping backend. Running frontend only."
fi

# Install frontend deps if needed, then start Astro frontend
echo "🎨 Starting Astro frontend on http://127.0.0.1:4321"
pushd frontend >/dev/null
if [ ! -d node_modules ]; then
  echo "📦 Installing frontend dependencies..."
  if [ -f package-lock.json ]; then
    npm ci
  else
    npm install
  fi
fi
npm run dev &
FRONTEND_PID=$!
popd >/dev/null

echo ""
echo "✅ Development servers starting..."
if [[ ${BACKEND_PID:-} ]]; then
  echo "   Backend:  http://127.0.0.1:8000"
fi
echo "   Frontend: http://127.0.0.1:4321"
echo ""
echo "📝 Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
if [[ ${BACKEND_PID:-} ]]; then
  wait $BACKEND_PID $FRONTEND_PID
else
  wait $FRONTEND_PID
fi
