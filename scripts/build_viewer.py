#!/usr/bin/env python3
"""Build a DAR bilingual paper viewer from structured data. Enforces AR/EN parity by construction."""
import os, shutil, html

def build(slug, meta, sections, refs, ref_note_en, ref_note_ar):
    """
    meta: dict(title_en, title_ar, authors, venue, doi, license, keywords_en, keywords_ar)
    sections: list of (h_en, h_ar, [en_paras_html], [ar_paras_html]) — counts must match
    refs: list of (num, text_html) with ORIGINAL paper numbers, ascending
    """
    for i, (he, ha, en, ar) in enumerate(sections):
        assert len(en) == len(ar) and len(en) > 0, f"section {i} ({he}): EN={len(en)} AR={len(ar)}"
    nums = [n for n, _ in refs]
    assert nums == sorted(nums) and len(set(nums)) == len(nums), "refs must be unique ascending original numbers"

    def sec_html(h, paras, rtl):
        inner = "\n".join(f"    {p}" for p in paras)
        d = ' dir="rtl"' if rtl else ' dir="ltr"'
        return f"  <section>\n    <h2{d}>{h}</h2>\n{inner}\n  </section>"

    ar_secs = "\n\n".join(sec_html(ha, ar, True) for _, ha, _, ar in sections)
    en_secs = "\n\n".join(sec_html(he, en, False) for he, _, en, _ in sections)
    ref_lis = "\n".join(f"      <li>{t}</li>" for _, t in refs)

    page = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(meta['title_ar'])} — DAR</title>
<meta name="description" content="{html.escape(meta['title_en'])} — Arabic/English bilingual viewer (DAR).">
<link rel="canonical" href="https://dararchive.com/papers/{slug}/">
<link rel="icon" type="image/png" href="../../assets/logo.png">
<link rel="stylesheet" href="../../assets/css/style.css">
<script>
window.i18n = {{
  ar: {{
    nav_browse: "تصفح",
    nav_search: "بحث",
    nav_submit: "تقديم"
  }},
  en: {{
    nav_browse: "Browse",
    nav_search: "Search",
    nav_submit: "Submit"
  }}
}};
</script>
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap" rel="stylesheet">
<style>
.ar {{ direction: rtl; }}
.en {{ direction: ltr; }}
.compare-section {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border);
}}
.compare-section:last-child {{ border-bottom: none; }}
.compare-ar {{ direction: rtl; }}
.compare-en {{ direction: ltr; }}
.compare-section .section-label {{
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-2);
  margin-bottom: 0.5rem;
  font-weight: 700;
}}
@media (max-width: 768px) {{
  .compare-section {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<nav>
  <a href="../../" class="logo">
    <img src="../../assets/logo.png" alt="DAR" style="height:32px;width:auto;vertical-align:middle">
    <small>Arabic Research Archive</small>
  </a>
  <div class="nav-links">
    <a href="../../" data-i18n="nav_browse">Browse</a>
    <a href="../../search.html" data-i18n="nav_search">Search</a>
    <a href="../../submit.html" data-i18n="nav_submit">Submit</a>
    <a href="https://github.com/ahmdngi/dar" target="_blank">GitHub</a>
  </div>
</nav>

<div class="container paper-view">

<div class="paper-header">
  <h1 dir="ltr">{meta['title_en']}</h1>
  <h2 dir="rtl" style="font-family:'Amiri',serif;font-size:1.2rem;color:var(--accent-2);margin-top:0.5rem;line-height:1.5">{meta['title_ar']}</h2>

  <div class="paper-meta">
    <span>👤 {meta['authors']}</span>
    <span>📄 {meta['venue']}</span>
    <span>🔗 <a href="https://doi.org/{meta['doi']}">{meta['doi']}</a></span>
    <span class="license-badge">✓ {meta['license']}</span>
  </div>

  <div class="lang-toggle" dir="ltr">
    <button class="active" onclick="setLang('ar')" id="toggle-ar">🇸🇦 العربية</button>
    <button onclick="setLang('en')" id="toggle-en">🇬🇧 English</button>
    <button onclick="setLang('both')" id="toggle-both">⇄ <span class="tog-label-side">Side by Side</span></button>
    <button onclick="setLang('compare')" id="toggle-compare">⇌ <span class="tog-label-compare">Compare Sections</span></button>
  </div>
</div>

<div id="paper-content" class="paper-body">

<!-- ==================== ARABIC ==================== -->
<div class="lang-content ar active">
{ar_secs}
</div>

<!-- ==================== ENGLISH ==================== -->
<div class="lang-content en">
{en_secs}
</div>

</div><!-- /paper-content -->

<!-- References -->
<div class="paper-body" style="margin-top:2rem">
  <section class="ref-section">
    <h2 dir="ltr">References</h2>
    <p dir="ltr" style="font-size:0.85rem;color:var(--text-2)">{ref_note_en}</p>
    <ol dir="ltr">
{ref_lis}
    </ol>
  </section>
</div>

<footer>
  <p>Original paper: <a href="https://doi.org/{meta['doi']}">{meta['doi']}</a> · License: {meta['license']}</p>
  <p>Translation © DAR — Arabic Research Archive</p>
</footer>
</div>

<script>
function setLang(lang) {{
  document.querySelectorAll('.lang-toggle button').forEach(b => b.classList.remove('active'));
  var btnId = (lang === 'both' ? 'both' : lang);
  document.getElementById('toggle-' + btnId).classList.add('active');
  document.querySelectorAll('.compare-section').forEach(function(el) {{ el.remove(); }});
  document.querySelectorAll('.lang-content').forEach(function(el) {{
    el.classList.remove('active', 'side-by-side');
    el.style.display = 'none';
  }});
  document.getElementById('paper-content').classList.remove('side-by-side');
  if (lang === 'both') {{
    document.querySelectorAll('.lang-content').forEach(function(el) {{
      el.classList.add('side-by-side');
      el.style.display = 'block';
    }});
    document.getElementById('paper-content').classList.add('side-by-side');
  }} else if (lang === 'compare') {{
    var arSections = document.querySelectorAll('.lang-content.ar > section');
    var enSections = document.querySelectorAll('.lang-content.en > section');
    var container = document.getElementById('paper-content');
    var count = Math.min(arSections.length, enSections.length);
    for (var i = 0; i < count; i++) {{
      var pair = document.createElement('div');
      pair.className = 'compare-section';
      var enCol = document.createElement('div');
      enCol.className = 'compare-en';
      var enLabel = document.createElement('div');
      enLabel.className = 'section-label';
      enLabel.textContent = 'ENGLISH';
      enCol.appendChild(enLabel);
      enCol.appendChild(enSections[i].cloneNode(true));
      var arCol = document.createElement('div');
      arCol.className = 'compare-ar';
      var arLabel = document.createElement('div');
      arLabel.className = 'section-label';
      arLabel.textContent = 'العربية';
      arCol.appendChild(arLabel);
      arCol.appendChild(arSections[i].cloneNode(true));
      pair.appendChild(enCol);
      pair.appendChild(arCol);
      container.appendChild(pair);
    }}
  }} else {{
    document.querySelector('.lang-content.' + lang).style.display = 'block';
    document.querySelector('.lang-content.' + lang).classList.add('active');
  }}
  if (lang === 'ar') {{
    document.documentElement.dir = 'rtl';
    document.documentElement.lang = 'ar';
  }} else {{
    document.documentElement.dir = 'ltr';
    document.documentElement.lang = 'en';
  }}
  var isAr = (lang === 'ar' || lang === 'both' || lang === 'compare');
  var sideEl = document.querySelector('.tog-label-side');
  var compEl = document.querySelector('.tog-label-compare');
  if (sideEl) sideEl.textContent = isAr ? 'جنباً إلى جنب' : 'Side by Side';
  if (compEl) compEl.textContent = isAr ? 'مقارنة' : 'Compare Sections';
}}
setLang('ar');
</script>
<script src="../../assets/js/i18n.js"></script>
</body>
</html>
"""
    outdir = f"/root/git-repos-personal/dar/papers/{slug}"
    os.makedirs(outdir, exist_ok=True)
    with open(f"{outdir}/index.html", "w") as f:
        f.write(page)
    pdf = f"/root/.hermes/cache/scratch/darpdfs/{slug}.pdf"
    if os.path.exists(pdf):
        shutil.copy(pdf, f"{outdir}/paper.pdf")
    print(f"BUILT {slug}: {len(sections)} sections, {len(refs)} refs, {len(page)//1024}KB")
