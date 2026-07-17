/**
 * DAR Site Language Toggle
 * Adds bilingual support for all site UI text.
 * Usage: add data-i18n="key" to any element, and translations[key] in i18n dict.
 */
(function() {
  const LANG_KEY = 'dar-lang';
  let lang = localStorage.getItem(LANG_KEY) || 'en';

  function applyLang(l) {
    lang = l;
    document.documentElement.lang = l;
    document.documentElement.dir = l === 'ar' ? 'rtl' : 'ltr';
    localStorage.setItem(LANG_KEY, l);
    // Update all data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (window.i18n && window.i18n[l] && window.i18n[l][key]) {
        el.textContent = window.i18n[l][key];
      }
    });
    // Update toggle button text
    const btn = document.getElementById('lang-toggle-btn');
    if (btn) btn.textContent = l === 'ar' ? 'English' : 'العربية';
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (window.i18n && window.i18n[l] && window.i18n[l][key]) {
        el.placeholder = window.i18n[l][key];
      }
    });
    // Dispatch event for dynamic content (paper cards, etc.)
    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang: l } }));
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Inject toggle button if not present
    if (!document.getElementById('lang-toggle-btn') && window.i18n) {
      const nav = document.querySelector('.nav-links') || document.querySelector('nav');
      if (nav) {
        const btn = document.createElement('button');
        btn.id = 'lang-toggle-btn';
        btn.className = 'lang-btn';
        btn.style.cssText = 'background:none;border:1px solid var(--border);color:var(--text-1);padding:4px 12px;border-radius:6px;cursor:pointer;font-size:0.85rem;margin-left:8px';
        btn.onclick = function() { applyLang(lang === 'ar' ? 'en' : 'ar'); };
        nav.appendChild(btn);
      }
    }
    applyLang(lang);
  });
})();
