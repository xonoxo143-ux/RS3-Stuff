# RS3 Equilibrium tracker

The tracker is split into three layers so live data, League rules, and manual player choices cannot silently overwrite each other.

## Canonical inputs

- `task-catalog.json` — master 1,152-task Equilibrium catalog. Refreshed from ScapeLeagues with cached fallback.
- `league-rules.json` — relic, blessing, task-tier, region, and milestone rules. This is the only place thresholds belong.
- `player-state.json` — compact manual account state: relic/blessing choice vectors, selected regions, exclusions, key items, flags, goal, and route preferences.
- `task-overrides.json` — optional requirement/time/location enrichment for task IDs. Tasks without enrichment are explicitly treated as requirement-unknown rather than guaranteed-ready.
- `live-wikisync.json` — authoritative live completed-task IDs and skill levels.
- `live-hiscores.html` — optional diagnostic/enrichment source only. Tracker generation must not depend on its HTML structure.

## Generated outputs

- `assistant-state.json` — canonical structured briefing for ChatGPT. Read this first.
- `assistant-context.md` — human-readable version with all currently active relic/blessing effects and quick-task routing.
- `live-summary.json` — compact compatibility snapshot.
- `live-unfinished.json` — every unfinished task with tracker status, blockers/checks, and enriched quick-task lists.
- `changes.json` — new task IDs, named tasks, LP delta, and level-ups from the previous live snapshot.
- `health.json` — source health/freshness and mapping status.
- `live-history.json` — compact state-change history.

## Choice encoding

Relics use a 1-based option vector in tier order. The current vector is `2 3 3 2 3 - -`, resolving to Golden Touch / Divine Druid / Voidwalker / Transmutation / Devout.

Blessing paths use `1=Order`, `2=Balance`, `3=Chaos`. Only numbered-tier picks are stored; God-tier blessings are derived automatically from the three preceding picks.

## Refresh model

GitHub Actions runs hourly and on demand. WikiSync is mandatory for live task/skill state. ScapeLeagues refresh failure falls back to the cached master catalog. HiScores is optional, so a Jagex HTML redesign cannot stop task tracking again.
