#!/usr/bin/env python3
"""
DAR Ingester — scrape, structure, and translate academic papers.

Usage:
  python3 ingester.py https://doi.org/10.1109/ACCESS.2026.3673557
  python3 ingester.py https://arxiv.org/abs/2304.12345
  python3 ingester.py path/to/paper.pdf

Output:
  - papers/<slug>/index.html   → Arabic + English viewer page
  - papers/<slug>/original.json  → raw structured data

Requires:
  pip install requests beautifulsoup4
  DEEPSEEK_API_KEY env var (optional, for translation)
"""

import argparse, hashlib, json, os, re, sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = "deepseek-chat"
OUTPUT_DIR = Path("papers")

# ─── URL Pattern Detection ─────────────────────────────────────

def detect_source(url: str) -> str:
    """Detect whether the URL is IEEE Xplore, arXiv, DOI resolver, or PDF."""
    domain = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()

    if "ieeexplore" in domain:
        return "ieee"
    if "arxiv.org" in domain:
        return "arxiv"
    if "doi.org" in domain:
        return "doi"
    if path.endswith(".pdf"):
        return "pdf"
    return "unknown"

# ─── IEEE Xplore Scraper ───────────────────────────────────────

def scrape_ieee(url: str) -> dict:
    """Scrape paper metadata and full text from IEEE Xplore."""
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""

    # DOI
    doi = ""
    for meta in soup.find_all("meta"):
        if meta.get("name") == "citation_doi":
            doi = meta.get("content", "")
            break

    # Authors
    authors = []
    for a in soup.find_all("meta"):
        if a.get("name") == "citation_author":
            authors.append(a.get("content", ""))

    # Abstract
    abstract = ""
    for meta in soup.find_all("meta"):
        if meta.get("name") == "description":
            abstract = meta.get("content", "")
            break

    # Publication date
    pub_date = ""
    for meta in soup.find_all("meta"):
        if meta.get("name") == "citation_publication_date":
            pub_date = meta.get("content", "")

    # Full text sections — try to extract the article text
    sections = []
    body_div = soup.find("div", class_=re.compile("article-text|body|full-text"))
    if body_div:
        for heading in body_div.find_all(["h2", "h3"]):
            section = {
                "heading": heading.get_text(strip=True),
                "body": []
            }
            for sibling in heading.find_next_siblings():
                if sibling.name in ["h2", "h3"]:
                    break
                if sibling.name == "p":
                    section["body"].append(sibling.get_text(strip=True))
            if section["body"]:
                sections.append(section)

    # License
    license_url = ""
    cc_link = soup.find("a", href=re.compile(r"creativecommons"))
    if cc_link:
        license_url = cc_link.get("href", "")

    return {
        "source": "ieee",
        "source_url": url,
        "title": title,
        "doi": doi,
        "authors": authors,
        "abstract": abstract,
        "publication_date": pub_date,
        "license_url": license_url,
        "sections": sections,
        "scraped_at": datetime.utcnow().isoformat()
    }

# ─── arXiv Scraper ─────────────────────────────────────────────

def scrape_arxiv(url: str) -> dict:
    """Scrape paper from arXiv (prefer abstract page, fallback to PDF)."""
    headers = {"User-Agent": "Mozilla/5.0"}
    # Normalize to abstract page
    arxiv_id = url.split("/abs/")[-1].split("/")[0] if "/abs/" in url else url.split("/")[-1]
    abstract_url = f"https://arxiv.org/abs/{arxiv_id}"

    resp = requests.get(abstract_url, headers=headers, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title = ""
    t = soup.find("h1", class_="title")
    if t:
        title = t.get_text(strip=True).replace("Title:", "").strip()

    authors = []
    a = soup.find("div", class_="authors")
    if a:
        authors = [x.get_text(strip=True) for x in a.find_all("a")]

    abstract = ""
    ab = soup.find("blockquote", class_="abstract")
    if ab:
        abstract = ab.get_text(strip=True).replace("Abstract:", "").strip()

    # Get full text via arXiv HTML
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    sections = []

    return {
        "source": "arxiv",
        "source_url": abstract_url,
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "sections": sections,
        "scraped_at": datetime.utcnow().isoformat()
    }

# ─── DOI Resolver ──────────────────────────────────────────────

def resolve_doi(doi_url: str) -> str:
    """Resolve a DOI to find the best open-access source URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
    return resp.url

# ─── Text-to-Slug ──────────────────────────────────────────────

def title_to_slug(title: str) -> str:
    """Convert a paper title to a filesystem-safe slug."""
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s[:80].strip("-")

# ─── Translation ───────────────────────────────────────────────

def translate_text(text: str, target_lang: str = "Arabic") -> str:
    """Translate text using DeepSeek API."""
    if not DEEPSEEK_API_KEY:
        return "[Translation pending — set DEEPSEEK_API_KEY]"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"You are a scientific translator. Translate the following academic "
                    f"text to {target_lang}. Keep all citations [1], equation numbers (1), "
                    f"URLs, DOIs, and LaTeX math unchanged. Use formal academic Arabic."
                )
            },
            {"role": "user", "content": text}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }
    resp = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ─── Main Pipeline ─────────────────────────────────────────────

def pipeline(url: str):
    """Run the full pipeline: scrape → structure → translate → output."""

    # Step 1: Detect source and scrape
    source = detect_source(url)
    print(f"[+] Detected source: {source}")

    if source == "doi":
        resolved = resolve_doi(url)
        source = detect_source(resolved)
        url = resolved
        print(f"[+] Resolved DOI → {url}")

    if source == "ieee":
        paper = scrape_ieee(url)
    elif source == "arxiv":
        paper = scrape_arxiv(url)
    else:
        print(f"[-] Unsupported source: {source}")
        print("    Supported: IEEE Xplore, arXiv, DOI links")
        sys.exit(1)

    # Step 2: Create output directory
    slug = title_to_slug(paper.get("title", "untitled"))
    out_dir = OUTPUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 3: Save original JSON
    json_path = out_dir / "original.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(paper, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved structured data → {json_path}")

    # Step 4: Translate abstract
    print(f"[+] Translating abstract...")
    abstract_ar = translate_text(paper.get("abstract", ""))
    paper["abstract_ar"] = abstract_ar

    # Step 5: Save updated JSON with translation
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(paper, f, ensure_ascii=False, indent=2)

    # Step 6: Generate HTML
    html_path = out_dir / "index.html"
    generate_html(paper, html_path)
    print(f"[+] Generated viewer → {html_path}")
    print(f"[✓] Done! Papers available at {out_dir}")


def generate_html(paper: dict, path: Path):
    """Generate a bilingual HTML viewer page from paper data."""
    # Placeholder — will expand for full paper reconstruction
    title = paper.get("title", "")
    authors = ", ".join(paper.get("authors", []))
    abstract_ar = paper.get("abstract_ar", "")
    abstract = paper.get("abstract", "")

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — DAR</title>
</head>
<body>
<h1>{title}</h1>
<p dir="ltr">{authors}</p>
<hr>
<h2 dir="rtl">الملخص</h2>
<p dir="rtl">{abstract_ar}</p>
<hr>
<h2>Abstract</h2>
<p dir="ltr">{abstract}</p>
</body>
</html>""".strip()

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DAR — Paper Ingester")
    parser.add_argument("url", help="Paper URL (DOI, arXiv, IEEE Xplore)")
    args = parser.parse_args()
    pipeline(args.url)
