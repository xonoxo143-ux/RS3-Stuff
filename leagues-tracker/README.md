# RS3 Equilibrium tracker

The tracker has three deliberate layers: **League rules**, **manual player state**, and **generated live intelligence**. A live-source failure must not silently rewrite League rules or manual facts.

## Read order

For assistant/gameplay use, read these in order:

1. `assistant-state.json` — canonical structured account + active League effects.
2. `recommendations.json` — precomputed task sprint, fast candidates, clusters, LP efficiency, and near-unlocks.
3. `live-summary.json` — compact current snapshot / completed task IDs.
4. `live-unfinished.json` — full evaluated unfinished-task database when deeper inspection is needed.
5. `player-state.json` — manual facts only; use this to change choices/preferences/flags.

Do **not** reconstruct current task counts, LP, levels, or milestones from old files or notes.

## Canonical inputs

- `task-catalog.json` — master 1,152-task Equilibrium catalog. Refreshed from ScapeLeagues with cached fallback.
- `league-rules.json` — relics, blessings, task tiers, region thresholds, and other League rules. Thresholds belong here and nowhere else.
- `player-state.json` — compact manual account state: relic/blessing vectors, selected regions, exclusions, key items, manual flags, goal, and route preferences.
- `task-overrides.json` — explicit task requirement/time/location metadata. These entries receive Grade-A recommendation confidence when their blockers are satisfied.
- `task_intelligence.py` — conservative automatic inference for task action type, rough time, skill wording, and location cluster.
- `live-wikisync.json` — authoritative live completed-task IDs and skill levels.

## Generated outputs

- `assistant-state.json` — canonical structured briefing for ChatGPT. Includes resolved active relic/blessing effects and health state.
- `assistant-context.md` — detailed human-readable assistant briefing generated from `assistant-state.json` + recommendations.
- `recommendations.json` — goal sprint, fastest verified tasks, inferred backups, manual checks, LP/minute ranking, cluster bundles, near-unlocks, and metadata coverage.
- `report.md` — concise human-readable account and route report.
- `live-summary.json` — compact compatibility snapshot.
- `live-unfinished.json` — every unfinished task with status, blockers, confidence, inferred/explicit metadata, and scoring.
- `changes.json` — new tasks, LP delta, and level-ups since the previous live snapshot.
- `catalog-changes.json` — added/removed/changed task IDs detected when the upstream task catalog changes.
- `health.json` — source freshness, state consistency, catalog mapping, recommendation coverage, and warnings/errors.
- `live-history.json` — current-generation compact state-change history (up to 200 changed snapshots).

`history.json` is retained only as a **legacy pre-upgrade historical archive**. It is never a source of current state.

## Recommendation confidence

The tracker intentionally prefers `unknown` over a convincing bad guess.

- **Grade A** — explicit metadata from `task-overrides.json`; skill/region/manual blockers have been evaluated. Required prep items may still need to be gathered.
- **Grade B** — conservative wording-based inference from `task_intelligence.py`. Useful as a backup candidate, but verify hidden quest/item/activity prerequisites before relying on it.
- **Grade U** — insufficient requirement data. These tasks remain visible in the full unfinished database but are not promoted into the primary sprint.

Task statuses include `verified_ready`, `inferred_candidate`, `manual_check`, `blocked`, `locked_region`, `known_issue`, `excluded`, and `accessible_requirements_unknown`.

## Choice encoding

Relics use a 1-based option vector in tier order. Current vector: `2 3 3 2 3 - -`, resolving to Golden Touch / Divine Druid / Voidwalker / Transmutation / Devout.

Blessing paths use `1=Order`, `2=Balance`, `3=Chaos`. Only numbered-tier picks are stored. God-tier blessings are derived automatically from the preceding three path picks. Dynamic effects such as True Equilibrium count only **currently unlocked** numbered blessing choices.

## Refresh model

GitHub Actions runs hourly at minute `:17`, on demand, and when tracker source files change.

- WikiSync is mandatory for task IDs and skill levels.
- ScapeLeagues task-catalog refresh is optional; the last valid cached 1,152-task catalog is retained if upstream parsing fails.
- Jagex HiScores HTML is no longer fetched or stored because it is not needed for task/skill tracking and previously created a brittle failure point.
- The workflow compiles the tracker, regenerates outputs, runs invariant tests, then performs a race-safe rebase/push.
- Catalog updates are diffed before replacement so upstream task changes are visible instead of silently accepted.

## Health/invariants

The tracker checks for conditions such as:

- correct elective thresholds (`150 / 275 / 400`),
- unlocked elective slots versus recorded selected regions,
- missing relic/blessing choices for already-unlocked tiers,
- completed task IDs missing from the master catalog,
- WikiSync/catalog freshness,
- recommendation metadata coverage.

A health warning does not necessarily stop refreshes; structural errors are surfaced prominently so they cannot be mistaken for healthy state.
