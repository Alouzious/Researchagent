#!/bin/bash


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "AI Research Agent - Phase 1 Setup"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo -e "${RED} Python 3.9+ required. You have: $python_version${NC}"
    exit 1
else
    echo -e "${GREEN}Python $python_version${NC}"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW} venv already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN} Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate
echo -e "${GREEN} Virtual environment activated${NC}"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN} Dependencies installed${NC}"

# Create .env file
echo ""
if [ -f ".env" ]; then
    echo -e "${YELLOW}  .env already exists${NC}"
else
    echo "Creating .env file..."
    cp .env.template .env
    echo -e "${GREEN} .env file created${NC}"
    echo ""
    echo -e "${YELLOW}  IMPORTANT: Edit .env and add your GROQ_API_KEY${NC}"
    echo "   Get your free key at: https://console.groq.com/keys"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p .cache/topics
mkdir -p .cache/papers
echo -e "${GREEN} Cache directories created${NC}"

# Check if Groq API key is set
echo ""
if grep -q "your_groq_api_key_here" .env 2>/dev/null; then
    echo -e "${YELLOW} WARNING: Groq API key not configured!${NC}"
    echo "   Please edit .env and add your GROQ_API_KEY"
    echo ""
    read -p "Do you want to set it now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Groq API key: " api_key
        sed -i.bak "s/your_groq_api_key_here/$api_key/" .env
        rm .env.bak 2>/dev/null
        echo -e "${GREEN} API key saved${NC}"
    fi
fi

# Run tests
echo ""
read -p "Run tests now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running tests..."
    python test_agent.py
fi

# Summary
echo ""

echo -e "${GREEN} Setup complete!${NC}"

echo ""
echo "Next steps:"
echo "1. Make sure your GROQ_API_KEY is set in .env"
echo "2. Run the app: streamlit run app.py"
echo "3. Open browser at: http://localhost:8501"
echo ""
echo "For deployment to Render:"
echo "1. Push to GitHub"
echo "2. Follow DEPLOYMENT_CHECKLIST.md"
echo ""
echo "Happy researching!"
