#!/usr/bin/env python3
"""Merge premium body chunks into article-bodies.json and regenerate HTML."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


def main() -> int:
    base_path = CONTENT / "article-bodies.json"
    if not base_path.exists():
        print("Run enrich_bodies.py first", file=sys.stderr)
        return 1

    base_list = json.loads(base_path.read_text(encoding="utf-8"))
    bodies = {item["slug"]: item for item in base_list}
    merged = 0
    for path in sorted(CONTENT.glob("bodies-premium-*.json")):
        chunk = json.loads(path.read_text(encoding="utf-8"))
        items = chunk if isinstance(chunk, list) else list(chunk.values())
        for item in items:
            slug = item["slug"]
            item["tier"] = item.get("tier") or "premium"
            item["handcrafted"] = True
            bodies[slug] = item
            merged += 1
        print(f"merged {path.name}: {len(items)}")

    out = list(bodies.values())
    # keep catalog order when possible
    order = [t["slug"] for t in json.loads((CONTENT / "topics.json").read_text(encoding="utf-8"))]
    out.sort(key=lambda b: order.index(b["slug"]) if b["slug"] in order else 10**9)
    base_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"article-bodies.json now {len(out)} entries; premium merges this run: {merged}")

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "generate_articles.py")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
