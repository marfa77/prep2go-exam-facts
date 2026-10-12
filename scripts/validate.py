#!/usr/bin/env python3
"""Validate data/facts.json structure, CSV sync, and URLs.
Usage: python scripts/validate.py [--no-net] [--strict]
404/410/DNS errors fail; 403/429/5xx/timeouts are WARN (many official sites block scripted clients)."""
import csv, json, sys, pathlib, re, urllib.request, urllib.error, concurrent.futures as cf
root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(root / "data/facts.json"))
err = []
REQ = ["id","name","language","cefr","issuer","sections","pass_rule","fee","dates_2026","accepted_for","source_url","practice_url","verified_on"]
ids = [e["id"] for e in d["exams"]]
if len(set(ids)) != len(ids): err.append("duplicate ids")
for e in d["exams"]:
    for k in REQ:
        if k not in e: err.append(f"{e.get('id')}: missing {k}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", e["verified_on"]): err.append(f"{e['id']}: bad verified_on")
    if not e["source_url"].startswith("https://"): err.append(f"{e['id']}: bad source_url")
    for x in e["dates_2026"] or []:
        for k in ("exam_date","registration_closes"):
            if k in x and not re.match(r"^2026-\d{2}-\d{2}$", x[k]): err.append(f"{e['id']}: bad {k}")
for r in d["requirements"]:
    for k in ("country","route","level","source_url","verified_on"):
        if k not in r: err.append(f"requirement missing {k}")
rows = list(csv.DictReader(open(root / "data/facts.csv")))
if [r["id"] for r in rows] != ids: err.append("facts.csv out of sync: run scripts/build.py")
for m in err: print("ERROR:", m)
nulls = sum(1 for e in d["exams"] for v in e.values() if v is None)
print(f"{len(ids)} exams, {len(d['requirements'])} requirements, {nulls} null fields")
fail = bool(err)
if "--no-net" not in sys.argv:
    urls = sorted({e["source_url"] for e in d["exams"]} | {u for e in d["exams"] for u in e.get("extra_sources", [])}
                  | {e["practice_url"] for e in d["exams"] if e["practice_url"]} | {r["source_url"] for r in d["requirements"]})
    def check(u):
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (prep2go-exam-facts validator)"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r: return u, r.status
        except urllib.error.HTTPError as e: return u, e.code
        except Exception as e: return u, type(e).__name__
    with cf.ThreadPoolExecutor(8) as ex:
        for u, s in ex.map(check, urls):
            if s == 200: tag = "OK  "
            elif "--strict" in sys.argv or s in (404, 410): tag = "FAIL"; fail = True
            else: tag = "WARN"
            print(f"{tag} {s} {u}")
print("RESULT:", "FAIL" if fail else "PASS")
sys.exit(1 if fail else 0)
