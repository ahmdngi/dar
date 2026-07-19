# Changelog

## v1.5.0 — 2025-07-19

### Added
- 8 new OA papers from license investigation batch: IET ITS, IET D&T, Renewable Energy, J. Env. Management, RSER, Int. J. InfoSec ×2, J. Unmanned Vehicle Systems
- DAR now hosts 26 bilingual AR/EN papers

### Fixed
- Paragraph parity script now counts `<p>` tags with attributes (fixes false failures on Arabic sections with inline styles)

### Changed
- Domain migrated: `dar.oversight.ee` → `dararchive.com`
- CNAME, OG tags, README updated for new domain

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
- CI/CD: GitHub Actions workflow with paragraph parity check + Pages deploy

### Changed
- Nav now uses logo image instead of text
- Cleaned up git history (removed old SVGs, wide logo)

### Deployment
- GitHub Pages at https://ahmdngi.github.io/dar/ (or directly via Tailscale: runner.tailb05740.ts.net:9999)
