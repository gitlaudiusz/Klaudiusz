#!/usr/bin/env python3
"""
K2K Message Watcher - Auto-checks for new messages every 30 seconds
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Set

# ANSI colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class K2KWatcher:
    def __init__(self, k2k_dir: Path):
        self.k2k_dir = k2k_dir
        self.messages_dir = k2k_dir / "messages"
        self.seen_messages: Set[str] = set()
        self.my_uuid = self._get_my_uuid()
        
    def _get_my_uuid(self) -> str:
        """Get current terminal UUID"""
        # For now, hardcoded - could read from env or file
        return "4AAF503F-6050-4F49-B420-8B4A5008FABD"
        
    def _scan_messages(self) -> Dict[str, Path]:
        """Scan all message directories for JSON files"""
        messages = {}
        for uuid_dir in self.messages_dir.iterdir():
            if uuid_dir.is_dir():
                for json_file in uuid_dir.glob("*.json"):
                    messages[str(json_file)] = json_file
        return messages
        
    def _read_message(self, path: Path) -> dict:
        """Read and parse message JSON"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"{RED}Error reading {path}: {e}{RESET}")
            return {}
            
    def _display_message(self, msg_data: dict, path: Path):
        """Display message in pretty format"""
        print(f"\n{CYAN}{'='*60}{RESET}")
        print(f"{BOLD}{BLUE}📨 NEW MESSAGE!{RESET}")
        print(f"{YELLOW}From:{RESET} {msg_data.get('from', 'Unknown')}")
        print(f"{YELLOW}To:{RESET} {msg_data.get('to', 'Unknown')}")
        print(f"{YELLOW}Time:{RESET} {msg_data.get('timestamp', 'Unknown')}")
        print(f"{YELLOW}Subject:{RESET} {BOLD}{msg_data.get('subject', 'No subject')}{RESET}")
        print(f"{YELLOW}File:{RESET} {path.name}")
        print(f"\n{GREEN}Message:{RESET}")
        print(msg_data.get('message', 'No message body'))
        
        # Show any additional important fields
        for key in ['urgent', 'ps', 'question', 'proposal']:
            if key in msg_data:
                print(f"\n{MAGENTA}{key.upper()}:{RESET} {msg_data[key]}")
                
        print(f"{CYAN}{'='*60}{RESET}\n")
        
    def watch(self, interval: int = 30):
        """Watch for new messages"""
        print(f"{BOLD}{GREEN}🚀 K2K Message Watcher Started!{RESET}")
        print(f"Watching for messages to: {YELLOW}{self.my_uuid}{RESET}")
        print(f"Check interval: {BLUE}{interval} seconds{RESET}")
        print(f"{CYAN}Press Ctrl+C to stop{RESET}\n")
        
        # Initial scan
        current_messages = self._scan_messages()
        self.seen_messages = set(current_messages.keys())
        print(f"Found {len(self.seen_messages)} existing messages")
        
        try:
            while True:
                # Wait for interval
                time.sleep(interval)
                
                # Scan again
                current_messages = self._scan_messages()
                new_files = set(current_messages.keys()) - self.seen_messages
                
                if new_files:
                    print(f"\n{BOLD}{GREEN}🔔 {len(new_files)} NEW MESSAGE(S)!{RESET}")
                    
                    for file_path in sorted(new_files):
                        path = current_messages[file_path]
                        msg_data = self._read_message(path)
                        
                        # Only show if message is TO us
                        if msg_data.get('to') == self.my_uuid:
                            self._display_message(msg_data, path)
                            print(f"{YELLOW}💡 Remember to respond!{RESET}")
                        
                    self.seen_messages.update(new_files)
                else:
                    # Simple heartbeat
                    print(f"\r{datetime.now().strftime('%H:%M:%S')} - No new messages...", end='', flush=True)
                    
        except KeyboardInterrupt:
            print(f"\n\n{RED}Watcher stopped by user{RESET}")
            

def main():
    k2k_dir = Path(__file__).parent.parent
    watcher = K2KWatcher(k2k_dir)
    watcher.watch(30)  # Check every 30 seconds
    

if __name__ == "__main__":
    main()