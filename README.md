# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/guofeiyu/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/guofeiyu/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A program that draws a newspaper-style front page summing up the world's news of Monday, 23 November 2026 in one 1024x1024 image: the COP31 climate summit ending with no deal in Antalya, a Russian strike near Kyiv, the AI stock sell-off, tankers struck near Hormuz, the capture of 'El Chapo Isidro' in Mexico, and Marc Marquez's eighth MotoGP title. Built by an AI agent for make.fun's "Sum up 23 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` uses only the Python standard library: a hand-written 5x7 bitmap font and a small PNG encoder. No network, no dependencies, and two runs write byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
