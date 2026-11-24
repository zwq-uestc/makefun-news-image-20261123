# One image: Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/zwq-uestc/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/zwq-uestc/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

This program writes a single picture of the world's news on Monday 23 November 2026. The lead story is Nvidia bringing Jensen Huang back as chief executive, with the shares up 31% on the day. The other five stories are Ukraine saying its drones sank a Russian warship off Libya, three Russian missiles landing in Poland as NATO meets in emergency session, a factory fire in Indonesia confirmed to have killed 24 people, Congo halting cobalt exports, and drones hitting a Russian cargo ship in the Baltic Sea.

`generate_image.py` draws the picture in code (PIL, Noto Serif for headlines, Noto Sans for labels) from news checked on 24 November 2026 in Reuters, CNN, NPR and others. `main.py` copies the finished image to the output directory, unchanged and byte-identical on every run.

## Try it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image lands at `out/entry.png`, 1024 by 1024 pixels.

---

<sub>Entered on [make.fun](https://make.fun/?ref=v8kmerg7&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
