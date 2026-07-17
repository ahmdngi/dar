# DAR — Arabic Research Archive

ترجمة الأبحاث العلمية مفتوحة الوصول إلى العربية

Translate open-access research papers to Arabic while preserving references, citations, equations, and formatting.

**Website:** [dar.oversight.ee](https://dar.oversight.ee)

## Mission

DAR bridges the language gap in academic research by translating open-access scientific papers into Modern Standard Arabic (MSA). Every paper maintains full section structure, bibliographic references, citation markers, equations, and figures — preserving academic integrity across both languages.

## How it works

1. **Submit** — Open a GitHub Issue with the paper URL
2. **Review** — Rights check (must be OA/CC-licensed)
3. **Translate** — AI pipeline translates to formal academic Arabic (DeepSeek, temp=0.2)
4. **Human Review** — Scientific and linguistic review by domain specialists
5. **Publish** — Arabic version goes live with attribution

## Feature Tour

| Feature | Description |
|---------|-------------|
| **4-Mode Viewer** | Read in Arabic, English, side-by-side, or per-section comparison |
| **Site Language Toggle** | Switch entire UI between AR and EN (persists in localStorage) |
| **Bilingual Paper Cards** | Titles and abstracts displayed in the active site language |
| **Search** | Client-side search across titles, abstracts, and authors in both languages |
| **GitHub Issues** | Submit papers via structured issue template |
| **CC/FAIR** | Only hosts papers under open-access licenses (CC BY, CC BY-SA, arXiv) |

## Supported Sources

- **IEEE Access** (CC BY) — HTML scrape with full-text extraction
- **TransNav Journal** (CC BY 4.0) — Full-text available
- **arXiv** — Abstract page + TeX source
- **DOI** — Auto-resolve to OA source
- **PDF** — Fallback via GROBID/Nougat (in development)

## Tech Stack

| Component | Choice |
|-----------|--------|
| Hosting | GitHub Pages + Tailscale |
| Domain | `dar.oversight.ee` (CNAME) |
| Search | Client-side (Fuse.js pattern) |
| Pipeline | Python + DeepSeek API |
| Scraping | BeautifulSoup + requests |
| Translation | DeepSeek Chat API (temp=0.2) |
| Verification | Automated paragraph parity check |
| I18n | Custom data-i18n system with localStorage |

## Local Development

```bash
# Serve locally
python3 -m http.server 9999
# Access at http://localhost:9999
```

```bash
# Run the ingester on a paper
cd scripts
pip install requests beautifulsoup4
export DEEPSEEK_API_KEY="sk-..."
python3 ingester.py https://doi.org/10.1109/ACCESS.2026.3673557
```

## Current Papers

| Paper | Venue | License |
|-------|-------|---------|
| Maritime Security Operations Center (M-SOC): SLR | TransNav, 2025 | CC BY 4.0 |
| A Proactive Defense: OSINT Framework for Maritime Cybersecurity | IEEE Access, 2026 | CC BY 4.0 |

## License

- **Code:** MIT
- **Papers:** As per their original licenses (all hosted papers are CC or OA)
- **Translations:** © DAR — Arabic Research Archive
