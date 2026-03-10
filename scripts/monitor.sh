#!/bin/bash
# Combined monitor: watchdog + gateway uptime

python3 ~/.openclaw/workspace/scripts/watchdog_services.py
python3 ~/.openclaw/workspace/scripts/gateway_uptime.py
