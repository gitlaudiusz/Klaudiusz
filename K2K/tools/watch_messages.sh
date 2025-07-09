#!/bin/bash
# K2K Message Watcher - inotifywait version
# Real-time file system monitoring instead of polling

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
CYAN='\033[96m'
RESET='\033[0m'
BOLD='\033[1m'

MY_UUID="A07F6A49-13A1-4C17-A1E4-F0E756E870C5"
K2K_DIR="$(dirname "$0")/.."
MESSAGES_DIR="$K2K_DIR/messages"

echo -e "${BOLD}${GREEN}🚀 K2K inotifywait Watcher Started!${RESET}"
echo -e "Watching for messages to: ${YELLOW}$MY_UUID${RESET}"
echo -e "Monitoring: ${BLUE}$MESSAGES_DIR${RESET}"
echo -e "${CYAN}Press Ctrl+C to stop${RESET}\n"

# Function to process new message
process_message() {
    local file_path="$1"
    local filename=$(basename "$file_path")
    
    # Check if file contains message TO us
    local to_field=$(jq -r '.to // empty' "$file_path" 2>/dev/null)
    
    if [[ "$to_field" == "$MY_UUID" ]]; then
        echo -e "\n${CYAN}============================================================${RESET}"
        echo -e "${BOLD}${BLUE}📨 NEW MESSAGE!${RESET}"
        
        # Extract key fields with jq
        local from=$(jq -r '.from // "Unknown"' "$file_path")
        local subject=$(jq -r '.subject // "No subject"' "$file_path")
        local timestamp=$(jq -r '.timestamp // "Unknown"' "$file_path")
        local message=$(jq -r '.message // "No message body"' "$file_path")
        
        echo -e "${YELLOW}From:${RESET} $from"
        echo -e "${YELLOW}Time:${RESET} $timestamp"
        echo -e "${YELLOW}Subject:${RESET} ${BOLD}$subject${RESET}"
        echo -e "${YELLOW}File:${RESET} $filename"
        echo -e "\n${GREEN}Message:${RESET}"
        echo "$message"
        
        # Check for special fields
        local urgent=$(jq -r '.urgent // empty' "$file_path")
        local ps=$(jq -r '.ps // empty' "$file_path")
        
        [[ -n "$urgent" ]] && echo -e "\n${RED}URGENT:${RESET} $urgent"
        [[ -n "$ps" ]] && echo -e "\n${CYAN}PS:${RESET} $ps"
        
        echo -e "${CYAN}============================================================${RESET}\n"
        echo -e "${YELLOW}💡 Remember to respond!${RESET}\n"
    fi
}

# Check if fswatch is available (macOS equivalent of inotifywait)
if ! command -v fswatch &> /dev/null; then
    echo -e "${RED}fswatch not found! Install with: brew install fswatch${RESET}"
    echo -e "${YELLOW}Falling back to simple polling...${RESET}"
    
    # Simple fallback
    while true; do
        sleep 30
        echo -e "\r$(date '+%H:%M:%S') - Checking for new messages..." 
    done
    exit 1
fi

# Monitor directory for new files using fswatch (macOS)
fswatch -o -r "$MESSAGES_DIR" | while read; do
    # Find newest .json files in the last 2 seconds
    find "$MESSAGES_DIR" -name "*.json" -newermt "2 seconds ago" | while read file_path; do
        # Only process .json files
        if [[ "$file_path" == *.json ]]; then
            echo -e "${GREEN}🔔 New file detected: $(basename "$file_path")${RESET}"
            
            # Give file time to be written completely
            sleep 0.5
            
            # Process the message
            process_message "$file_path"
        fi
    done
done