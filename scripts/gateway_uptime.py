#!/usr/bin/env python3
"""
Gateway Uptime Tracker - More forgiving version with retries
"""
import json
import time
from pathlib import Path
from datetime import datetime

DATA_FILE = Path.home() / ".openclaw/workspace/data/gateway_uptime.json"
LOG_FILE = Path.home() / ".openclaw/workspace/logs/gateway_uptime.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def load_history():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"checks": [], "uptime_percent": 100.0, "total_checks": 0, "last_status": None}

def save_history(history):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=2)

def check_gateway():
    import urllib.request
    
    # Try multiple times with longer timeouts
    for attempt in range(3):
        try:
            req = urllib.request.Request("http://localhost:3001/api/status")
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read())
                return data.get("gateway") == "online"
        except Exception as e:
            if attempt < 2:
                time.sleep(1)  # Wait before retry
                continue
            return False
    return False

def main():
    history = load_history()
    is_online = check_gateway()
    
    now = datetime.now().isoformat()
    history["checks"].append({"time": now, "online": is_online})
    
    # Keep last 1000 checks
    if len(history["checks"]) > 1000:
        history["checks"] = history["checks"][-1000:]
    
    # Calculate uptime
    total = len(history["checks"])
    online = sum(1 for c in history["checks"] if c.get("online", False))
    uptime = (online / total * 100) if total > 0 else 100.0
    
    history["uptime_percent"] = round(uptime, 2)
    history["total_checks"] = total
    history["last_check"] = now
    history["last_status"] = "online" if is_online else "offline"
    
    save_history(history)
    
    status = "ONLINE" if is_online else "OFFLINE"
    log(f"Gateway: {status} | Uptime: {uptime:.2f}% ({online}/{total} checks)")

if __name__ == "__main__":
    main()
