# RS3 Equilibrium tracker — 112321-2

This is the F2P fork of the main `leagues-tracker` for the League character **112321-2**.

## Purpose

- Separate WikiSync/player state from the main **112321** character.
- Keep the same task intelligence and recommendation engine.
- Treat this account as a low-fatigue / experimentation character with no fixed endgame goal yet.
- Route toward quick, low-RNG tasks first, with the first major decision at **150 completed tasks**.

## F2P caps

The fork enforces the current free-account progression limits:

- **4 regions total**: Misthalin + Havenhythe, automatic Karamja at 50 tasks, then **one** elective region at 150 tasks.
- **Relic tier 3 maximum**.
- **Blessing tier 2 maximum**.

The task catalog itself is still the full Equilibrium catalog. Known tasks that appear available but are currently impossible on F2P are excluded in `player-state.json`.

## Read order

1. `assistant-state.json`
2. `recommendations.json`
3. `live-summary.json`
4. `live-unfinished.json`
5. `player-state.json`

WikiSync is authoritative for completed task IDs and skill levels. Manual state stores only choices, exclusions, account-mode facts, items, and preferences.
