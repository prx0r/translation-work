#!/bin/bash
# THE BURN (continuous): T1+L0 factory at scale over every onboarded mukta-* work.
# BURN = T1 (contract gloss rows) + L0 (morphology/grounds), by free beam models.
# It stops at L0 on purpose: argmap/L2/C1 need a post-hoc brief + assessor.
# Supervised by tw-wave.service (Restart=always) — so it never stops.
# key comes from EnvironmentFile=/root/.tw-beam.env (systemd); fallback to vault
[ -n "$OPENCODE_GO_KEY" ] || export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle 2>/dev/null)"
cd /root/translation-work || exit 1
for d in $(ls -d mukta-m* 2>/dev/null); do
  [ -f "$d/STATUS.json" ] || continue
  python3 tools/auto_burn.py --work "$d" --from 1 --to 999 || true
done
echo "WAVE DONE $(date -Is)"
