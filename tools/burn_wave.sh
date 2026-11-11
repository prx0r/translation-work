#!/bin/bash
# Bulk wave burn: auto_burn every onboarded mukta-* work, sequentially.
# Supervised by tw-wave.service (Restart=always).
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle 2>/dev/null)"
cd /root/translation-work || exit 1
for d in $(ls -d mukta-m* 2>/dev/null); do
  [ -f "$d/STATUS.json" ] || continue
  python3 tools/auto_burn.py --work "$d" --from 1 --to 999 || true
done
echo "WAVE DONE $(date -Is)"
