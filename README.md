# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Senz14/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Senz14/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

**The world in one day — Thursday, 26 November 2026.** One original broadsheet summing up the day's world news in six panels: the stories that happened, or were first reported, on 26 November 2026.

## The six stories

1. **Missiles hit Kyiv mall** — Russia strikes Kyiv with ballistic missiles overnight, hitting a shopping centre and two other buildings; seven people are wounded (Kyiv, Ukraine).
2. **Blast at Bangkok refinery** — An explosion and fire at the Bangchak oil refinery injures at least seven workers (Bangkok, Thailand).
3. **Flooded mine kills 13** — Floodwater swamps an illegal gold mine in Bogor, West Java; 13 miners are confirmed dead and 13 more are trapped underground (Indonesia).
4. **Migration at 29-year low** — UK net migration falls to 77,000 in the year to June, the lowest since 1997, the Office for National Statistics reports (United Kingdom).
5. **Parade halted by storm** — The Macy's Thanksgiving Day Parade is postponed by a nor'easter, the first postponement in its 100-year history; it moves to Saturday (United States).
6. **Nine killed in Gaza strikes** — Israeli strikes on Deir al-Balah kill nine Palestinians, the third straight night of attacks despite a year-old ceasefire (Gaza).

Plus, in the footer: EU leaders clash over a €45bn loan for Ukraine, the US proposes tariffs on 14 trading partners, the Houthis claim a strike on Saudi Arabia's Ras Tanura refinery, and SpaceX is cleared to launch up to a million Starmind satellites.

## The image

`entry.png` (1024×1024) is an original illustration drawn for this bounty by `draw.py` — no news-agency photographs, no copied artwork. Each panel pairs a pictogram with a short headline and summary, so a viewer who missed the day can tell what happened from the image alone.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png
```

No build step, no network. `main.ts` (Node 22, standard library only) validates `entry.png` as a whole PNG (signature, IHDR CRC, IEND CRC, 1024×1024 cap, 1 MiB cap), copies it to the output directory, then verifies the copy byte-for-byte (SHA-256 + timing-safe comparison) and reports the image's dimensions.

To redraw the image from scratch: `python3 draw.py` (needs Pillow).

## Files

- `entry.png` — the entry image (1024×1024 PNG).
- `draw.py` — the program that draws `entry.png` (Pillow, standard fonts).
- `main.ts` — the entry program: validates and copies `entry.png` to `/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=jkmc4mts&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
