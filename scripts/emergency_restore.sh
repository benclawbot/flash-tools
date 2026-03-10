#!/bin/bash
# Emergency Backup & Restore Script
# Restores Flash to full operational state

set -e

echo "🔥 FLASH EMERGENCY RESTORE"
echo "========================="

# Clone repos
echo "[1/6] Cloning flash-tools..."
git clone https://github.com/benclawbot/flash-tools.git /tmp/flash-tools

echo "[2/6] Cloning flash-secrets (private)..."
git clone https://github.com/benclawbot/flash-secrets.git /tmp/flash-secrets || git clone git@github.com:benclawbot/flash-secrets.git /tmp/flash-secrets

echo "[3/6] Restoring secrets..."
cp /tmp/flash-secrets/credentials.json ~/.private/
cp /tmp/flash-secrets/openclaw.json ~/.openclaw/

echo "[4/6] Restoring tools..."
cp -r /tmp/flash-tools/scripts/* ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/*.sh
chmod +x ~/.openclaw/workspace/scripts/*.py

echo "[5/6] Starting Open Brain..."
cd /tmp/open-brain 2>/dev/null || git clone https://github.com/benclawbot/open-brain.git /tmp/open-brain
cd /tmp/open-brain && docker compose up -d

echo "[6/6] Starting Gateway..."
sudo openclaw gateway

echo ""
echo "✅ RESTORE COMPLETE!"
echo "- Secrets restored"
echo "- Tools restored"
echo "- Open Brain running"
echo "- Gateway running"
