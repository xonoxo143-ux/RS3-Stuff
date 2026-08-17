# RS3 Equilibrium tracker

Generated account intelligence for player `112321`.

- `assistant-context.md` — read this first; concise human/assistant briefing.
- `assistant-context.json` — structured briefing.
- `latest.json` — canonical raw+derived current snapshot.
- `changes.json` — deltas and progress velocity.
- `tasks.json` — WikiSync completions translated to task names.
- `task-catalog.json` — full 1,152-task Equilibrium catalog with IDs, names, tiers, regions, points, blessing flags and issue flags.
- `task-pools.json` — incomplete routing pools for inferred/confirmed accessible regions.
- `region-summary.json` — task/point/blessing density by region.
- `history.json` — rolling six full snapshots.
- `timeline.json` — rolling six compact snapshots.
- `config.json` — manually confirmed relic/region strategy facts that public APIs cannot observe.

The workflow runs hourly at minute 17 and can also be dispatched manually. WikiSync is authoritative for task completion IDs; Jagex HiScores is authoritative for LP/levels/XP. The task catalog is refreshed from ScapeLeagues and retains the last valid cached copy if that fetch fails.
