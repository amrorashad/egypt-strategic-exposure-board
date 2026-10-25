#!/usr/bin/env python3
"""Fail closed if separate mission-scope and deployment-status indicators disappear or assert unverified operations."""
import re
import sys
from pathlib import Path

page = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").read_text(encoding="utf-8")
section = re.search(r'<section class="panel" aria-labelledby="missionIndicatorsTitle".*?</section>', page, re.S)
assert section, "Missing dedicated military indicators section"
body = section.group()
assert body.count('class="trend-item"') == 2, "Expected exactly two separate indicator cards"
for label in ("MISSION SCOPE", "DEPLOYMENT STATUS"):
    match = re.search(r'<article class="trend-item">\s*<b>' + label + r'</b>(.*?)</article>', body, re.S)
    assert match, f"Missing {label} card"
    card = match.group(1)
    assert 'NOT VERIFIED' in card, f"{label}: status changed; manual evidence verification and review required"
    assert 'periodpoint unknown' in card, f"{label}: unverified status must remain unknown"
assert 'CIQ-GEO-2026-10-14' in body, "Baseline reference missing"
assert '18 October 2026' in body, "Assessment date missing"
print("PASS: two separate conservative military indicators, assessment date and baseline retained")
