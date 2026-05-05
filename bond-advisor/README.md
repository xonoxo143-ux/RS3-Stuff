# RS3 Bond Sustainer Advisor

A legal RuneScape 3 bond-planning assistant.

The goal is to combine public account data, public market data, a curated method catalog, and user-provided account context into a realistic daily plan for sustaining membership bonds.

## Scope

This project is an advisor, not a bot.

It can:

- fetch public skill/profile data
- fetch public market data
- compare method requirements against an account profile
- calculate conservative profit estimates
- produce daily and 14-day bond-sustain plans

It must not:

- control the RuneScape client
- click, type, or automate gameplay
- read the game screen for gameplay decisions
- bypass game rules or client restrictions
- store API keys in the repo

## Current build target

Version 0 is data-first.

The first useful output is:

```text
output/bond_advisor_context.json
```

That file should be built from:

- `data/manual_profile.json`
- `data/item_watchlist.json`
- `data/method_catalog.json`
- public Hiscores/RuneMetrics data
- Wiki Prices and ItemDB market data

The OpenAI API layer should come after the context file is clean.

## Layout

```text
bond-advisor/
  config/
    example.manual_profile.json
    example.openai.env.txt

  data/
    item_watchlist.json
    method_catalog.json
    manual_profile.json
    actual_results_log.json

  docs/
    API_SOURCES.md
    METHOD_CATALOG_GUIDE.md
    SAFETY_BOUNDARIES.md
    ROADMAP.md

  scripts/
    fetch_hiscores.py
    fetch_runemetrics_profile.py
    fetch_runemetrics_quests.py
    fetch_wiki_prices.py
    fetch_itemdb.py
    build_context.py
    score_methods.py
    ask_openai.py

  output/
    .gitkeep
```

## Setup

Use Python 3.10+.

```bash
cd bond-advisor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Android/Termux, the same structure can work with Termux Python. Keep the repo and `.env` local.

## API key handling

Never commit your OpenAI API key.

Create a local `.env` file from `config/example.openai.env.txt`:

```text
OPENAI_API_KEY=your_key_here
```

`.env` is ignored by Git.

## First command target

Once scripts are implemented, the intended flow is:

```bash
python scripts/build_context.py --rsn "Your RSN"
python scripts/score_methods.py
python scripts/ask_openai.py
```

For now, the repo is intentionally scaffolded before logic is added.
