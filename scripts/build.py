#!/usr/bin/env python3
"""Build CSVs, guides/*.md, docs/index.html, docs/sitemap.xml from data/facts.json."""
import csv, json, pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(root / "data/facts.json"))
PAGES = "https://marfa77.github.io/prep2go-exam-facts/"
def fee_str(f):
    if not f: return ""
    fs = f if isinstance(f, list) else [f]
    return "; ".join(f"{x['amount']} {x['currency']} ({x['country']})" for x in fs)
def secs_str(s):
    if not s: return ""
    out = []
    for x in s:
        bits = [str(x["duration_min"]) + " min"] if x.get("duration_min") else []
        if x.get("weight_pct"): bits.append(f"{x['weight_pct']}%")
        if x.get("points"): bits.append(f"{x['points']} pts")
        out.append(f"{x['name']} ({', '.join(bits)})" if bits else x["name"])
    return "; ".join(out)
def dates_str(ds):
    if not ds: return ""
    return "; ".join(f"{x['exam_date']}" + (f" (reg. closes {x['registration_closes']})" if x.get("registration_closes") else "") for x in ds)
with open(root / "data/facts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id","name","language","cefr","issuer","sections","pass_rule","fee","dates_2026","accepted_for","source_url","practice_url","verified_on"])
    for e in d["exams"]:
        w.writerow([e["id"],e["name"],e["language"],e["cefr"] or "",e["issuer"],secs_str(e["sections"]),e["pass_rule"] or "",fee_str(e["fee"]),dates_str(e["dates_2026"]),e["accepted_for"],e["source_url"],e["practice_url"] or "",e["verified_on"]])
with open(root / "data/requirements.csv", "w", newline="") as f:
    w = csv.writer(f)
    keys = ["country","route","level","accepted","notes","source_url","verified_on"]
    w.writerow(keys)
    for r in d["requirements"]: w.writerow([r[k] or "" for k in keys])
(root/"guides").mkdir(exist_ok=True)
for e in d["exams"]:
    L = [f"# {e['name']}", "", f"- **CEFR level:** {e['cefr'] or 'n/a'}", f"- **Issuer:** {e['issuer']}",
         f"- **Pass rule:** {e['pass_rule'] or 'not verified'}", f"- **Fee:** {fee_str(e['fee']) or 'varies by centre / not verified'}",
         f"- **Accepted for:** {e['accepted_for']}", ""]
    if e["sections"]:
        L += ["## Sections", "", "| Section | Duration (min) | Weight / points |", "|---|---|---|"]
        for s in e["sections"]:
            dur = str(s.get("duration_min") or "—") + (f" (+{s['prep_min']} prep)" if s.get("prep_min") else "")
            wt = f"{s['weight_pct']}%" if s.get("weight_pct") else ""
            if s.get("points"): wt = (wt + " / " if wt else "") + f"{s['points']} pts"
            L.append(f"| {s['name']} | {dur} | {wt} |")
        L.append("")
    if e.get("total_duration"): L += [f"**Total duration:** {e['total_duration']}", ""]
    if e.get("partial_retake_note"): L += [f"**Partial retake:** {e['partial_retake_note']}", ""]
    if e["dates_2026"]:
        L += ["## 2026 dates (official)", ""] + [f"- {x.get('sitting','')}: {x['exam_date']}" + (f", registration closes {x['registration_closes']}" if x.get("registration_closes") else "") for x in e["dates_2026"]] + [""]
    L += ["## Sources", "", f"- {e['source_url']}"] + [f"- {u}" for u in e.get("extra_sources", [])] + ["", f"*Last verified: {e['verified_on']}*", ""]
    if e["practice_url"]: L += [f"Practice: [Prep2Go mocks]({e['practice_url']})", ""]
    (root/"guides"/f"{e['id']}.md").write_text("\n".join(L))
L = ["# Citizenship & residency language requirements", "", "| Country | Route | Level | Accepted | Notes | Source |", "|---|---|---|---|---|---|"]
for r in d["requirements"]:
    L.append(f"| {r['country']} | {r['route']} | {r['level'] or 'n/a'} | {r['accepted'] or '—'} | {r['notes'] or ''} | [link]({r['source_url']}) |")
L += ["", f"*Last verified: {d['verified_on']}*", ""]
(root/"guides"/"citizenship-residency-requirements.md").write_text("\n".join(L))
# Pages
ld = {"@context":"https://schema.org","@type":"Dataset","name":"Prep2Go exam facts: CIPLE, DELE, DELF, CELI and citizenship language requirements",
 "description":"Open, source-linked facts on immigration language exams (format, pass rules, fees, 2026 dates) and citizenship/residency language levels for Portugal, Spain, France and Italy. Unverifiable values are null.",
 "url":PAGES,"sameAs":"https://github.com/marfa77/prep2go-exam-facts","license":"https://creativecommons.org/licenses/by/4.0/","version":d["version"],
 "dateModified":d["verified_on"],"keywords":["CIPLE","DELE","DELF","CELI","citizenship","language requirement","open data"],
 "creator":{"@type":"Organization","name":"Prep2Go","url":"https://www.prep2go.study"},
 "distribution":[{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":PAGES+"facts.json"},{"@type":"DataDownload","encodingFormat":"text/csv","contentUrl":PAGES+"facts.csv"}]}
def practice(e):
    return f'<a href="{e["practice_url"]}">Prep2Go mocks</a>' if e["practice_url"] else "—"
rows = "".join(f"<tr><td>{html.escape(e['name'])}</td><td>{html.escape(e['pass_rule'] or '—')}</td><td>{html.escape(fee_str(e['fee']) or '—')}</td><td><a href=\"{e['source_url']}\">official</a></td><td>{practice(e)}</td></tr>" for e in d["exams"])
reqs = "".join(f"<tr><td>{r['country']}</td><td>{html.escape(r['route'])}</td><td>{r['level'] or '—'}</td><td><a href=\"{r['source_url']}\">source</a></td></tr>" for r in d["requirements"])
(root/"docs"/"index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prep2Go exam facts – CIPLE, DELE, DELF, CELI & citizenship language requirements</title>
<meta name="description" content="{html.escape(ld['description'])}"><link rel="canonical" href="{PAGES}">
<script type="application/ld+json">{json.dumps(ld)}</script>
<style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:2em auto;padding:0 1em}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:.4em;vertical-align:top}}</style></head><body>
<h1>Prep2Go exam facts</h1><p>{html.escape(ld['description'])} Last verified {d['verified_on']}. Data: <a href="facts.json">facts.json</a> · <a href="facts.csv">facts.csv</a> · <a href="requirements.csv">requirements.csv</a> · <a href="https://github.com/marfa77/prep2go-exam-facts">GitHub</a>. License CC BY 4.0.</p>
<h2>Exams</h2><table><tr><th>Exam</th><th>Pass rule</th><th>Fee</th><th>Source</th><th>Practice</th></tr>{rows}</table>
<h2>Citizenship & residency language levels</h2><table><tr><th>Country</th><th>Route</th><th>Level</th><th>Source</th></tr>{reqs}</table>
</body></html>
""")
for n in ["facts.json","facts.csv","requirements.csv"]: (root/"docs"/n).write_bytes((root/"data"/n).read_bytes())
(root/"docs"/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{PAGES}</loc><lastmod>{d["verified_on"]}</lastmod></url>\n</urlset>\n')
(root/"docs"/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {PAGES}sitemap.xml\n")
print("built")
