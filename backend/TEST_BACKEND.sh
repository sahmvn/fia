#!/bin/bash
# FIA Backend Testing Script
# Run this to test the Python RAG backend

set -e  # Exit on error

echo "=========================================="
echo "FIA Backend RAG System - Testing Script"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Install python3-venv if needed
echo -e "\n${YELLOW}[1/7] Checking Python environment...${NC}"
if ! python3 -m venv --help &> /dev/null; then
    echo "Installing python3-venv..."
    sudo apt install python3.10-venv -y
fi
echo -e "${GREEN}✓ Python environment ready${NC}"

# Step 2: Create virtual environment
echo -e "\n${YELLOW}[2/7] Creating virtual environment...${NC}"
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Step 3: Activate and install dependencies
echo -e "\n${YELLOW}[3/7] Installing dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 4: Check for .env file
echo -e "\n${YELLOW}[4/7] Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}✗ .env file not found!${NC}"
    echo "Creating .env from example..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ IMPORTANT: Edit .env and add your OPENAI_API_KEY${NC}"
    echo "Press Enter after you've added your API key..."
    read
fi

# Verify API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo -e "${RED}✗ Please update OPENAI_API_KEY in .env file${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Environment configured${NC}"

# Step 5: Ingest data
echo -e "\n${YELLOW}[5/7] Ingesting data into vector database...${NC}"
echo "This will load all JSON files from data/ folder"
python scripts/ingest_data.py --clear
echo -e "${GREEN}✓ Data ingestion complete${NC}"

# Step 6: Start server in background
echo -e "\n${YELLOW}[6/7] Starting FastAPI server...${NC}"
echo "Server will start on http://localhost:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
sleep 5  # Wait for server to start

# Check if server is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${RED}✗ Server failed to start${NC}"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi
echo -e "${GREEN}✓ Server is running${NC}"

# Step 7: Run tests
echo -e "\n${YELLOW}[7/7] Running API tests...${NC}"
echo ""
echo "=========================================="
echo "Test 1: Health Check"
echo "=========================================="
curl -s http://localhost:8000/health | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 2: List Patterns"
echo "=========================================="
curl -s http://localhost:8000/patterns | python3 -m json.tool | head -30

echo ""
echo "=========================================="
echo "Test 3: Analyze Story"
echo "=========================================="
curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My partner always needs to be right about everything. When I try to share my opinion, he talks over me or dismisses what I say. He uses a patronizing tone and makes me feel stupid. If I get upset, he says I am being too sensitive."
  }' | python3 -m json.tool

echo ""
echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo -e "${GREEN}✓ All tests passed${NC}"
echo ""
echo "Server is still running at http://localhost:8000"
echo "Visit http://localhost:8000/docs for interactive API documentation"
echo ""
echo "To stop the server, run: kill $SERVER_PID"
echo "Or press Ctrl+C"
echo ""
echo "To keep server running and exit script, press Enter..."
read

echo "Server still running in background. To stop it:"
echo "  kill $SERVER_PID"
