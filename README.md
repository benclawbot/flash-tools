# Flash Tools

Utilities built by Flash (Tom's OpenClaw agent).

## Scripts

- `openbrain_client.py` - Connect to Open Brain for memory storage/retrieval
- `gateway_uptime.py` - Track gateway availability with retries
- `monitor.sh` - Combined watchdog + uptime monitor

## Usage

```bash
# Connect to Open Brain
python3 scripts/openbrain_client.py

# Track uptime
python3 scripts/gateway_uptime.py

# Combined monitor
./scripts/monitor.sh
```
