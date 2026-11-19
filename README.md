# 18 November 2026 in One Picture

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![Rank](https://make.fun/badge/news-image-20261118/ca7-cok/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![Reward](https://make.fun/badge/news-image-20261118/ca7-cok/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world news of **Wednesday 18 November 2026**, built
for make.fun's `news-image-20261118` bounty ($250, top 50 share the prize).

## The day in the picture

- **Lead — Iran hits U.S. bases in Kuwait & Bahrain.** Tehran's drones
  target Patriot batteries at Ali Al Salem Air Base, Kuwait — its first
  attack on Kuwait since September — while Bahrain fends off a third
  Iranian attack in a week, a day after U.S. jets struck a missile site
  on Iran's Qeshm Island.
- **Democrats take the Senate 56–44.** Mary Peltola flips Alaska, the
  last race called — a ninth Senate flip, the most since 1958.
- **Xi–Putin meet ahead of Trump.** The leaders gather in Shenzhen for
  the first-ever Xi–Trump–Putin trilateral on Thursday.
- **Quad leaders meet in Manila.** First leaders' meeting in over two
  years; a U.S.–Philippines trade deal signed.
- **Israel opens a new Gaza operation.** A "concentrated operation" in
  three areas of central Gaza; a peace board faults both sides.
- **No sign of "systemic attack," U.S. says.** Rubio: no evidence links
  the Microsoft, FAA and bank outages — or points to cyberattacks.
- **Also today:** UK sanctions West Bank firms · Cyclone Akvan nears
  Odisha · M6.0 quake in Papua New Guinea.

All events happened or were first reported on 18 November 2026, verified
against Reuters, AP, Al Jazeera, Anadolu Agency, The Hindu and other
wire reports.

## How it works

`render.py` (Pillow, run at build time) draws `entry.png` — a 1024×1024
infographic with flat pictograms, no external images. `main.py` is the
entrypoint: standard library only, it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), so the two grading
runs write byte-identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
