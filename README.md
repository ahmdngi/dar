# DAR — Arabic Research Archive

ترجمة الأبحاث العلمية مفتوحة المصدر إلى العربية

Translate open-access research papers to Arabic while preserving references, citations, equations, and formatting.

## How it works

1. **Submit** — Open a GitHub Issue with the paper URL
2. **Review** — Rights check (must be OA/CC-licensed)
3. **Translate** — AI pipeline translates to formal academic Arabic
4. **Publish** — Arabic version goes live with attribution

## Pipeline

```
URL / DOI
   ↓
[Scraper] → structured JSON (sections, refs, equations)
   ↓
[Translator] → DeepSeek API, academic Arabic
   ↓
[Composer] → RTL HTML with MathJax
   ↓
[GitHub Pages] → Live
```

## Supported Sources

- **IEEE Access** (CC BY) — HTML scrape with full-text extraction
- **arXiv** — Abstract page + TeX source
- **DOI** — Auto-resolve to OA source
- **PDF** — Fallback via GROBID/Nougat (in development)

## Tech Stack

| Component | Choice |
|-----------|--------|
| Hosting | GitHub Pages |
| Search | Fuse.js (client-side) |
| Pipeline | Python + DeepSeek API |
| Scraping | BeautifulSoup + requests |
| Translation | DeepSeek Chat API |

## Local Development

```bash
# Serve locally
python3 -m http.server 9999
```

```bash
# Run the ingester on a paper
cd scripts
pip install requests beautifulsoup4
export DEEPSEEK_API_KEY="sk-..."
python3 ingester.py https://doi.org/10.1109/ACCESS.2026.3673557
```

## License

Code: MIT
Papers: As per their original licenses (all papers hosted are CC or OA)
