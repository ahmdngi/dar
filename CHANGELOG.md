# Changelog

## v1.0.0 — 2025-07-17

### Added
- Initial site structure: browse, search, submit pages
- Bilingual paper viewer with 4-mode toggle (Arabic / English / Side by Side / Compare Sections)
- Full translation of ShipCrawler IEEE Access paper (DOI: 10.1109/ACCESS.2026.3673557)
- Full translation of M-SOC TransNav paper (DOI: 10.12716/1001.19.04.11)
- Paper ingester pipeline (`scripts/ingester.py`)
- GitHub Issue submission template
- Site-wide AR/EN language toggle (persists in localStorage)
- Paper cards show Arabic titles + abstracts when site language is Arabic
- Custom DAR logo (designed by Ahmed)
- Favicon across all pages
- Automated paragraph parity verification (skill: `arabic-academic-translation`)

### Changed
- Nav now uses logo image instead of text
- Cleaned up git history (removed old SVGs, wide logo)

### Deployment
- GitHub Pages at https://ahmdngi.github.io/dar/ (or directly via Tailscale: runner.tailb05740.ts.net:9999)
