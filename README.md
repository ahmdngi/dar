# DAR — Arabic Research Archive

ترجمة الأبحاث العلمية مفتوحة الوصول إلى العربية

Translate open-access research papers to Arabic while preserving references, citations, equations, and formatting.

**Website:** [dararchive.com](https://dararchive.com)

![Release](https://img.shields.io/github/v/release/ahmdngi/dar?style=flat-square&label=release)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Language](https://img.shields.io/badge/language-HTML-orange?style=flat-square)
![Deploy](https://github.com/ahmdngi/dar/actions/workflows/deploy.yml/badge.svg)
![Pages](https://img.shields.io/badge/hosting-GitHub%20Pages-222?style=flat-square&logo=github)
![Stars](https://img.shields.io/github/stars/ahmdngi/dar?style=flat-square)

## Mission

DAR bridges the language gap in academic research by translating open-access papers into Modern Standard Arabic (MSA). Any research topic is in scope. Every paper keeps its full section structure, references, citation markers, equations, and figures in both languages.

## Scope

- Open to any research field, not limited to one domain
- Only papers under an open license (CC BY, CC BY-SA, or equivalent open-access terms)
- Every translation keeps a bilingual viewer with full paragraph parity

## How it works

1. **Submit** — Open a GitHub Issue with the paper URL or DOI
2. **Review** — License check (must be openly licensed)
3. **Translate** — AI-assisted translation to formal academic Arabic
4. **Human Review** — Scientific and linguistic review
5. **Publish** — Bilingual version goes live with attribution to the original

## Feature Tour

| Feature | Description |
|---------|-------------|
| **4-Mode Viewer** | Read in Arabic, English, side-by-side, or per-section comparison |
| **Site Language Toggle** | Switch entire UI between AR and EN (persists in localStorage) |
| **Bilingual Paper Cards** | Titles and abstracts displayed in the active site language |
| **Search** | Client-side search across titles, abstracts, and authors in both languages |
| **GitHub Issues** | Submit papers via structured issue template |
| **CC/FAIR** | Only hosts openly licensed papers |

## Eligible sources

Any publisher or repository is fine as long as the paper itself carries an open license. Typical examples:

- Gold open-access journals (CC BY)
- Open-access conference proceedings with a CC license
- Preprint servers where the author kept translation rights
- Any paper page showing an explicit open-access or CC badge

Papers behind a paywall or without a visible open license are out of scope.

## Tech Stack

| Component | Choice |
|-----------|--------|
| Hosting | GitHub Pages |
| Search | Client-side |
| Pipeline | Python |
| Translation | LLM-assisted, human-reviewed |
| Verification | Automated paragraph parity check |
| I18n | Custom data-i18n system with localStorage |

## Local Development

```bash
# Serve locally
python3 -m http.server 9999
# Access at http://localhost:9999
```

```bash
# Verify translation parity
python3 scripts/check-parity.py
```

## License

- **Code:** MIT
- **Papers:** As per their original licenses (all hosted papers are openly licensed)
- **Translations:** © DAR — Arabic Research Archive
