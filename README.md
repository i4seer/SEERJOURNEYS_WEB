# JOURNEY Website

Static production-ready website inspired structurally by the supplied Seer Worlds site, rebuilt with a distinct **Journey** identity.

**Series name:** Journey  
**Written by:** B. Carter  
**Published by:** Seer Press  
**Status:** Ten-book series â€” Books 1â€“3 published in Kindle and paperback; Books 4â€“10 forthcoming.

## Pages
- `/` â€” full-width road landscape hero and series home
- `/books` â€” ten-book library
- `/books/<slug>` â€” individual book pages
- `/journey` â€” spoiler-marked book-by-book journey with one progressive map per book and a complete final series map
- `/about`
- `/news`
- `/contact`

## Map note
The reader maps are schematic and intentionally labeled not to scale. They are derived from manuscript geography and plot relationships, not invented as precise surveyed cartography.

## Hosting
The files are root-relative and ready for static hosting. `CNAME` contains `journey.i4seer.com`; the current domain and hosting configuration are preserved.

## October 22, 2026 refresh

- Updated all ten covers from the latest print-ready front panels and versioned every reference.
- Verified all six individual edition URLs for the three published books. See publication-sources.json.
- Added the supplied signed author note and refreshed publication news.
- Brought book detail pages into the Seer Worlds layout rhythm with a 330px cover column, purchase links, and current cover-copy.txt sections. Existing descriptions, progression, navigation, and Known Network panels remain.
- Added a professional landscape hero using the built-in image-generation tool, with book covers 1 and 3 as visual references. The source image is assets/hero-road.png; the optimized website asset is assets/hero-road.webp. See assets/hero-road-prompt.txt for the full prompt.
- Preserved all map assets and map-specific styling.

## October 26, 2026 artwork refresh

All ten current source covers and book illustrations are exported by `scripts/sync_journey_artwork.py --source C:/SEERJOURNEYS` (Pillow, fonttools, beautifulsoup4). The warm contour-map paper, compass wordmark, pine ink, amber rules and licensed Alfa Slab One lettering match the approved Concept 4 cover design. The first three published books appear on the home and Books shelves, followed by a development notice. Existing reader maps and edition links are retained. Source books are never rebuilt by this script. Provenance is in `data/journey-artwork.json`.
