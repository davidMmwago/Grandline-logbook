# Grand Line Logbook

A One Piece reading and watching companion. The manga is the main voyage. The anime is there for the episodes worth watching alongside it.

- **Chart:** a zoomable map of the Grand Line. Click an island to see its arc's chapters, episodes, filler and must-watch episodes.
- **Chapter ↔ episode lookup:** page-level mapping for every adapted chapter.
- **Sessions, not checkboxes:** log a sitting as a chapter range plus any episodes you watched. Already partway through? Use **Catch up** or mark whole arcs as done.
- **Your ship:** follows your chapter progress, the Going Merry up to Enies Lobby and the Thousand Sunny after.
- **Stats:** total hours, what else you could have done in that time, and what was happening in the world when your chapter and episode came out.
- **Settings:** a must-watch rating slider (IMDb 7.0–9.8), light/dark mode, and export/import of your log as a JSON file.

## Run it

Open `index.html` in a browser. Everything (data, font, images) is built into that one file. The map library (Leaflet) and the body fonts load from CDNs, so the first load needs internet.

**GitHub Pages:** push this folder to a repo, then go to *Settings → Pages → Deploy from a branch → `main` / root*. The site is served from `index.html`.

Your log is saved in your browser (localStorage). To move it to another browser or device, use **Settings → Export file**, then **Import** on the other side.

## Project layout

```
index.html            built site (generated, so don't edit it directly)
build.py              assembles index.html from src/ + data/
src/template.html     the page: HTML, CSS and JS
src/assets/           font, parchment texture, ship sprites, log pose
data/build_data.py    builds data/one-piece.json from data/raw/
data/one-piece.json   chapters, episodes, arcs, ratings, release dates
data/raw/             source data pulled from the One Piece Wiki and IMDb
```

## Change something

```bash
# edit src/template.html (or swap files in src/assets/), then:
python build.py

# after updating anything in data/raw/:
python data/build_data.py
python build.py
```

Python 3.9+ and no extra packages.

## Updating the data

| File | What it is | Source |
|---|---|---|
| `raw_wc.txt` | chapter → episodes, with page ranges | One Piece Wiki, `Template:WC` |
| `raw_chdates.txt` | chapter release dates, stored as day gaps | One Piece Wiki, `Template:WhichMangaDate` |
| `raw_epdates.txt` | episode air dates, stored as day gaps | One Piece Wiki, `Template:WhichAnimeDate` |
| `raw_imdb.txt` | IMDb rating for every episode, plus titles for 8.5+ | IMDb episode list |

Arc boundaries and island positions live in `data/build_data.py` and `src/template.html` (the `LOCS` table). The world events on the stats page are hand-written in `src/template.html` (`EVENTS`).

Data last pulled: 2 November 2026 (chapter 1197, episode 1180).

## Credits and assets

- Chapter/episode mapping and release dates: [One Piece Wiki](https://onepiece.fandom.com/) (CC BY-SA).
- Episode ratings: [IMDb](https://www.imdb.com/title/tt0388629/episodes/) user ratings.
- Island placement guided by the [Library of Ohara world map](https://thelibraryofohara.com/onepieceworldmap/).
- Log pose art: Starlight1.
- Map rendering: [Leaflet](https://leafletjs.com/).

One Piece belongs to Eiichiro Oda / Shueisha / Toei Animation. This is an unofficial fan project. The ship sprites are official One Piece art, and the One Piece font and log pose art belong to their creators. Before making the repository public, check you're comfortable sharing them, or swap them out in `src/assets/` and rebuild.
