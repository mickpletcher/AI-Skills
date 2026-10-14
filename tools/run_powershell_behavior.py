#!/usr/bin/env python3
"""Run synthetic PowerShell Refactor scenarios through an OpenAI-compatible chat API.

Requires MODEL_API_KEY and MODEL_API_URL, plus explicit MODEL_ID. Does not run
PowerShell code. Produces ungraded model responses for separate human review.
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evaluations/fixtures/powershell-refactor.json"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skill", required=True, type=Path)
    p.add_argument("--model", required=True)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--temperature", type=float, default=0)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))["cases"]
    skill = args.skill.read_text(encoding="utf-8")
    url = os.environ.get("MODEL_API_URL", "")
    key = os.environ.get("MODEL_API_KEY", "")
    if not args.dry_run and (not url.startswith("https://") or not key):
        p.error("Set MODEL_API_URL (HTTPS chat completions endpoint) and MODEL_API_KEY")
    records = []
    for case in cases:
        prompt = case["prompt"] + "\n\nInput script:\n" + (case["input_script"] or "[NOT PROVIDED]")
        record = {"case_id": case["id"], "model": args.model, "skill": str(args.skill),
                  "timestamp_utc": datetime.now(timezone.utc).isoformat(), "response": None}
        if not args.dry_run:
            payload = {"model": args.model, "temperature": args.temperature,
                       "messages": [{"role": "system", "content": skill},
                                    {"role": "user", "content": prompt}]}
            req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as res:
                result = json.load(res)
            record["response"] = result["choices"][0]["message"]["content"]
        records.append(record)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"mode": "dry_run" if args.dry_run else "model_execution",
                                      "cases": records}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} {'dry-run' if args.dry_run else 'model'} records to {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
