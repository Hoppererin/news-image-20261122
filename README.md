# The World Today — Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Hoppererin/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Hoppererin/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image summing up the world's news of Sunday 22 November 2026:
**47 real stories from 7 regions**, drawn as a newspaper front page.

- **Lead:** Iran strikes US bases in Kuwait and Bahrain as the Gulf war
  widens; Trump says he will seek a permanent nuclear deal with Iran.
- **Big stories:** Russian missiles hit Lviv; EU–Indonesia sign a trade
  deal after 10 years; COP31 deadlocked; a magnitude 6.9 quake shakes
  Peru's Andes; Trump and Xi meet in Shenzhen; Hong Kong election
  committee voting begins.
- **In brief:** 40 more stories — North America 6, Latin America 4,
  Europe 7, Africa 4, Middle East 8, Asia 8, Oceania & Pacific 3.

## How it is built

`render.py` (Python 3 + Pillow + DejaVu system fonts) draws `entry.png`
(1024×1024, under 1 MiB). It is fully deterministic — no network, no
randomness, no clock — so running it twice writes byte-identical bytes.
`main.ts` (Node 22, standard library only) only copies `entry.png` to
the output directory.

## Run

```sh
python3 render.py          # draws entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/
```

## Files

| File | What it is |
|---|---|
| `entry.png` | The entry image, 1024×1024 PNG |
| `render.py` | Draws `entry.png` from the story list |
| `main.ts` | Entrypoint: copies `entry.png` to the output dir |
| `RESEARCH.md` | All 47 stories with their sources |
| `REPORT.md` | File hashes and verification results |
| `LICENSE` | MIT |
| `.makefun/owner.json` | Claim file naming the payout wallet |
