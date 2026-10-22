# JOURNEY Website

Static production-ready website inspired structurally by the supplied Seer Worlds site, rebuilt with a distinct **Journey** identity.

**Series name:** Journey  
**Written by:** B. Carter  
**Published by:** Seer Press  
**Status:** Ten-book series — Books 1–3 published in Kindle and paperback; Books 4–10 forthcoming.

## Pages
- `/` — full-width road landscape hero and series home
- `/books` — ten-book library
- `/books/<slug>` — individual book pages
- `/journey` — spoiler-marked book-by-book journey with one progressive map per book and a complete final series map
- `/about`
- `/news`
- `/contact`

## Map note
The reader maps are schematic and intentionally labeled not to scale. They are derived from manuscript geography and plot relationships, not invented as precise surveyed cartography.

## Hosting
The files are root-relative and ready for static hosting. `CNAME` still contains `seerjourneys.com` because no replacement domain was specified; change or remove it when the Journey domain is finalized.

## October 22, 2026 refresh

- Updated all ten covers from the latest print-ready front panels and versioned every reference.
- Verified all six individual edition URLs for the three published books. See publication-sources.json.
- Added the supplied signed author note and refreshed publication news.
- Brought book detail pages into the Seer Worlds layout rhythm with a 330px cover column, purchase links, and current cover-copy.txt sections. Existing descriptions, progression, navigation, and Known Network panels remain.
- Added a professional landscape hero using the built-in image-generation tool, with book covers 1 and 3 as visual references. The source image is assets/hero-road.png; the optimized website asset is assets/hero-road.webp. See assets/hero-road-prompt.txt for the full prompt.
- Preserved all map assets and map-specific styling.
