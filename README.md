# prep2go-exam-facts

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23322073.svg)](https://doi.org/10.5281/zenodo.23322073) [![PyPI](https://img.shields.io/pypi/v/prep2go-exam-facts.svg)](https://pypi.org/project/prep2go-exam-facts/)

Install: `pip install prep2go-exam-facts`

Open, source-linked facts about the language exams people take for **citizenship and residency** in Portugal, Spain, France and Italy: CIPLE A2, DELE A2 + CCSE, DELF A2/B1/B2 and CELI 2 (B1). Each record has the exam format (sections, durations, weights), the pass rule, fee (with country), official 2026 dates, who accepts it, an **official** `source_url` and a `verified_on` date. Anything we could not verify on an official page is `null`.

- Data: [`data/facts.json`](data/facts.json) · [`data/facts.csv`](data/facts.csv) · [`data/requirements.csv`](data/requirements.csv)
- Guides: [`guides/`](guides/)
- Website: https://marfa77.github.io/prep2go-exam-facts/
- Last verified: **2026-10-12**

## Exams at a glance

| Exam | Pass rule | Fee | Official source | Practice |
|---|---|---|---|---|
| [CIPLE A2](guides/ciple-a2.md) | 55% overall, no per-section minimum | €95 | [CAPLE](https://caple.letras.ulisboa.pt/exame/2/ciple) | [Prep2Go mocks](https://www.prep2go.study/ciple-a2) |
| [DELE A2](guides/dele-a2.md) | ≥30/50 in each of 2 groups (reading+writing; listening+speaking) | €138 (Spain, 2026) | [Instituto Cervantes](https://examenes.cervantes.es/es/dele/examenes/a2) | [Prep2Go mocks](https://www.prep2go.study/dele-a2) |
| [CCSE](guides/ccse.md) | not verified | €85 (2 attempts) | [Instituto Cervantes](https://examenes.cervantes.es/es/ccse/cuanto) | — |
| [DELF A2](guides/delf-a2.md) | ≥50/100 and ≥5/25 per paper | set by centre | [France Éducation international](https://www.france-education-international.fr/diplome/delf-tout-public) | [Prep2Go mocks](https://www.prep2go.study/delf-a2) |
| [DELF B1](guides/delf-b1.md) | ≥50/100 and ≥5/25 per paper | set by centre | [France Éducation international](https://www.france-education-international.fr/diplome/delf-tout-public) | — |
| [DELF B2](guides/delf-b2.md) | ≥50/100 and ≥5/25 per paper | set by centre | [France Éducation international](https://www.france-education-international.fr/diplome/delf-tout-public) | [Prep2Go mocks](https://www.prep2go.study/delf-b2-mock-test) |
| [CELI 2 (B1)](guides/celi-2-b1.md) | ≥72/120 written and ≥22/40 oral (94–160) | €120 standard / €65 Immigrati (Perugia) | [Università per Stranieri di Perugia](https://www.unistrapg.it/sites/default/files/docs/certificazioni/celi-2-valutazione.pdf) | [Prep2Go mocks](https://www.prep2go.study/celi-2-guide) |

## Citizenship & residency language levels

See [guides/citizenship-residency-requirements.md](guides/citizenship-residency-requirements.md).

- **Portugal:** naturalisation requires A2 Portuguese (e.g. CIPLE). Lei Orgânica 1/2026 (in force 19 May 2026) adds culture, history and civic knowledge requirements.
- **Spain:** nationality by residence requires DELE A2 or higher plus CCSE (exemptions exist).
- **France (since 1 Jan 2026):** A2 for a first multi-year card, B1 for a first resident card, B2 for naturalisation.
- **Italy:** B1 for citizenship (CELI, CILS, CERT.IT, PLIDA); A2 for the EU long-term residence permit.

## About Prep2Go practice

Prep2Go ([prep2go.study](https://www.prep2go.study)) runs timed mock exams. Mock pack: $15 for 3 timed mocks with AI reports plus 3 live AI orals (live AI orals are CIPLE only). Pro: $27 lifetime, including 1 timed mock and 1 live AI CIPLE oral. There is no free scored mock.

## Validate / rebuild

```bash
pip install jsonschema  # optional
python scripts/build.py      # regenerate CSVs, guides and docs/ from data/facts.json
python scripts/validate.py   # structure checks + URL checks (--no-net to skip)
```

## License & citation

Data and guides: [CC BY 4.0](LICENSE-DATA). Code: [MIT](LICENSE). Please cite using [CITATION.cff](CITATION.cff).

This dataset replaces [marfa77/prep2go.study.docs](https://github.com/marfa77/prep2go.study.docs).
