#!/bin/bash
# ===========================================
# Composition Assistant - Check SoundFont
# ===========================================
# This script checks if the SoundFont file exists
# Run: ./scripts/check-soundfont.sh

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

SOUNDFONT_DIR=${SOUNDFONT_DIR:-./transcriptionLibs/FluidR3_GM}
SOUNDFONT_FILE="${SOUNDFONT_DIR}/FluidR3_GM.sf2"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  🎵 Checking SoundFont${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check common locations
LOCATIONS=(
    "./transcriptionLibs/FluidR3_GM/FluidR3_GM.sf2"
    "./FluidR3_GM/FluidR3_GM.sf2"
    "../FluidR3_GM/FluidR3_GM.sf2"
)

FOUND=false
FOUND_PATH=""

for loc in "${LOCATIONS[@]}"; do
    if [ -f "$loc" ]; then
        FOUND=true
        FOUND_PATH="$loc"
        break
    fi
done

if [ "$FOUND" = true ]; then
    SIZE=$(du -h "$FOUND_PATH" | cut -f1)
    echo -e "${GREEN}✓ SoundFont found at: ${FOUND_PATH}${NC}"
    echo -e "  Size: ${SIZE}"
    echo ""
    
    # Check if .env has correct path
    DIR_PATH=$(dirname "$FOUND_PATH")
    echo -e "${YELLOW}Ensure your .env has:${NC}"
    echo "  SOUNDFONT_DIR=${DIR_PATH}"
else
    echo -e "${RED}✗ SoundFont not found${NC}"
    echo ""
    echo -e "${YELLOW}Please download FluidR3_GM.sf2 from:${NC}"
    echo "  https://sites.google.com/site/soundfonts4u/"
    echo ""
    echo -e "${YELLOW}Then place it in one of these locations:${NC}"
    echo "  ./transcriptionLibs/FluidR3_GM/FluidR3_GM.sf2"
    echo "  ./FluidR3_GM/FluidR3_GM.sf2"
    echo ""
    echo -e "${YELLOW}Or create the directory:${NC}"
    echo "  mkdir -p transcriptionLibs/FluidR3_GM"
    echo "  # Then copy FluidR3_GM.sf2 into it"
    echo ""
    exit 1
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ SoundFont check complete${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
