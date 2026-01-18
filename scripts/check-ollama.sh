#!/bin/bash
# ===========================================
# Composition Assistant - Check Ollama
# ===========================================
# This script checks if Ollama is running and the model is available
# Run: ./scripts/check-ollama.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load environment
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

OLLAMA_HOST=${OLLAMA_HOST:-http://localhost:11434}
OLLAMA_MODEL=${OLLAMA_MODEL:-qwen2.5:7b}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  🔍 Checking Ollama Status${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if Ollama is running
echo -e "${YELLOW}Checking Ollama server at ${OLLAMA_HOST}...${NC}"
if curl -sf "${OLLAMA_HOST}/api/tags" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama server is running${NC}"
else
    echo -e "${RED}✗ Ollama server is not responding${NC}"
    echo ""
    echo -e "${YELLOW}To start Ollama:${NC}"
    echo "  ollama serve"
    echo ""
    exit 1
fi

# Check if model is available
echo ""
echo -e "${YELLOW}Checking for model: ${OLLAMA_MODEL}...${NC}"
MODELS=$(curl -sf "${OLLAMA_HOST}/api/tags" | grep -o "\"name\":\"[^\"]*\"" | cut -d'"' -f4)

if echo "$MODELS" | grep -q "^${OLLAMA_MODEL}$"; then
    echo -e "${GREEN}✓ Model ${OLLAMA_MODEL} is available${NC}"
else
    echo -e "${YELLOW}⚠ Model ${OLLAMA_MODEL} not found${NC}"
    echo ""
    echo -e "${YELLOW}Available models:${NC}"
    echo "$MODELS" | while read model; do
        echo "  - $model"
    done
    echo ""
    echo -e "${YELLOW}To pull the model:${NC}"
    echo "  ollama pull ${OLLAMA_MODEL}"
    echo ""
    
    read -p "Do you want to pull ${OLLAMA_MODEL} now? (y/N): " pull_model
    if [[ "$pull_model" =~ ^[Yy]$ ]]; then
        echo ""
        ollama pull ${OLLAMA_MODEL}
    fi
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Ollama check complete${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
