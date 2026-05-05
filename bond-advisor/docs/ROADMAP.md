# Roadmap

## v0.1 - Repo skeleton and data contract

Status: in progress.

Deliverables:

- folder structure
- README
- safety boundaries
- API source notes
- method catalog guide
- manual profile schema
- item watchlist
- starter method catalog

## v0.2 - Fetch layer

Goal:

Create scripts that fetch public data and write normalized JSON snapshots.

Scripts:

- `fetch_hiscores.py`
- `fetch_runemetrics_profile.py`
- `fetch_runemetrics_quests.py`
- `fetch_wiki_prices.py`
- `fetch_itemdb.py`

Output:

```text
output/public_profile_snapshot.json
output/price_snapshot.json
```

## v0.3 - Context builder

Goal:

Merge public data, manual profile data, item watchlist, and method catalog.

Script:

- `build_context.py`

Output:

```text
output/bond_advisor_context.json
```

## v0.4 - Scoring layer

Goal:

Calculate method eligibility and conservative profit estimates before OpenAI sees the data.

Script:

- `score_methods.py`

Output:

```text
output/scored_methods.json
```

## v0.5 - OpenAI advisor

Goal:

Use OpenAI to rank realistic options and produce an actionable daily plan.

Script:

- `ask_openai.py`

Output:

```text
output/daily_plan.json
output/daily_plan.md
```

## v1.0 - Usable command-line planner

Goal:

One command produces a readable bond-sustain plan.

Target command:

```bash
python scripts/build_context.py --rsn "Your RSN"
python scripts/score_methods.py
python scripts/ask_openai.py
```

Later this can be wrapped in a simple Android-friendly UI, but only after the planner logic is stable.
