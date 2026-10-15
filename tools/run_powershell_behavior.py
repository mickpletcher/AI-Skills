#!/usr/bin/env python3
"""Run synthetic PowerShell Refactor scenarios through an OpenAI-compatible chat API.

Requires MODEL_API_KEY and MODEL_API_URL, plus explicit MODEL_ID. Does not run
PowerShell code. Produces ungraded model responses for separate human review.
"""
import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evaluations/fixtures/powershell-refactor.json"

class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "API redirects are disabled", headers, fp)


def save_checkpoint(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix="." + path.name + ".", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(document, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


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
    if not args.dry_run:
        try:
            endpoint = urllib.parse.urlsplit(url)
            valid_endpoint = endpoint.scheme == "https" and bool(endpoint.hostname)
        except ValueError:
            valid_endpoint = False
        if not valid_endpoint or not key:
            p.error("Set MODEL_API_URL (HTTPS chat completions endpoint) and MODEL_API_KEY")
    if args.output.exists() or args.output.is_symlink():
        p.error("Output already exists; choose a new path to preserve previous results")
    records = []
    document = {"mode": "dry_run" if args.dry_run else "model_execution",
                "status": "running", "cases": records}
    save_checkpoint(args.output, document)
    opener = urllib.request.build_opener(NoRedirects()) if not args.dry_run else None
    for case in cases:
        prompt = case["prompt"] + "\n\nInput script:\n" + (case["input_script"] or "[NOT PROVIDED]")
        record = {"case_id": case["id"], "model": args.model, "skill": str(args.skill),
                  "timestamp_utc": datetime.now(timezone.utc).isoformat(), "response": None}
        try:
            if not args.dry_run:
                payload = {"model": args.model, "temperature": args.temperature,
                           "messages": [{"role": "system", "content": skill},
                                        {"role": "user", "content": prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
                with opener.open(req, timeout=120) as res:
                    result = json.load(res)
                record["response"] = result["choices"][0]["message"]["content"]
                if not isinstance(record["response"], str):
                    raise ValueError("Expected a text response")
        except (Exception, KeyboardInterrupt) as error:
            document.update(status="partial" if records else "error",
                            failed_case_id=case["id"], error_type=type(error).__name__)
            save_checkpoint(args.output, document)
            print("Model run stopped; completed responses saved. No requests retried.", file=sys.stderr)
            return 1
        records.append(record)
        save_checkpoint(args.output, document)
    document["status"] = "completed"
    save_checkpoint(args.output, document)
    print(f"Wrote {len(records)} {'dry-run' if args.dry_run else 'model'} records to {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
