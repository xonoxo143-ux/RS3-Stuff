# RS3 Equilibrium account state — 112321

Refreshed from the latest live tracker snapshot at **2026-08-28 02:00 UTC**.

## Read this first

Use `live-summary.json` as the authoritative current account snapshot. Use `live-unfinished.json` for task recommendations and honor `config.json` recommendation exclusions and priority tasks. Treat all gameplay advice in an **Equilibrium-first** context: unlocked regions, League quest overrides, relic/passive effects, blessings, XP multipliers, and task requirements come before normal-RS3 assumptions.

### Current concrete state

- **7,230 LP**
- **218 tasks** completed
- **57 tasks** to the second elective-region unlock at **275**
- **182 tasks** to the third elective-region unlock at **400**
- **T5 relic tier**
- **10 blessing tasks** completed
- **2 blessing tasks** to Tier 4 at 12
- **Total level 1,839**
- Confirmed unlocked regions: **Misthalin, Havenhythe, Karamja, Desert**
- Later elective region choices: **unset until reconfirmed**
- Confirmed relic picks: **T1 Golden Touch, T2 Divine Druid, T3 Voidwalker, T4 Transmutation, T5 Devout**
- Confirmed third blessing: **Eternal Sustenance**

### Current skill levels

| Skill | Level |
|---|---:|
| Thieving | 105 |
| Agility | 99 |
| Prayer | 99 |
| Necromancy | 91 |
| Defence | 88 |
| Constitution | 85 |
| Crafting | 80 |
| Divination | 80 |
| Smithing | 80 |
| Mining | 75 |
| Runecrafting | 73 |
| Attack | 71 |
| Strength | 71 |
| Slayer | 70 |
| Magic | 69 |
| Fletching | 67 |
| Herblore | 66 |
| Cooking | 61 |
| Woodcutting | 61 |
| Firemaking | 54 |
| Construction | 53 |
| Summoning | 51 |
| Archaeology | 48 |
| Dungeoneering | 39 |
| Fishing | 35 |
| Ranged | 28 |
| Invention | 14 |
| Farming | 13 |
| Hunter | 13 |

## Current goals

### Primary

Reach **275 completed tasks** for the next elective-region unlock. With 218 completed, **57 remain**. Prioritize fast easy/medium completions over point value unless a harder task stacks with useful progression.

### Immediate subgoal

Reach **12 blessing tasks**. Current count is **10**, so **2 remain**.

Priority route currently stored in `config.json`:

1. **Task 1200** — Defeat a Sanguine crawler in Havenhythe for blessing task 11.
2. **Task 643** — Complete the Fight Kiln.
3. **Task 1271** — Equip a TokHaar-Kal Ket, Xil, Mej, or Mor cape for blessing task 12.

## Recently completed progression

- **Invention unlocked** after reaching 80 Crafting, 80 Divination, and 80 Smithing.
- Invention is already **level 14**.
- Smithing rose **67 → 80**.
- Dungeoneering rose **1 → 39**.
- Farming rose **2 → 13**.
- Woodcutting rose **60 → 61**.
- Firemaking rose **51 → 54**.
- Mining rose **74 → 75**.
- Five new tasks were detected in the latest successful live refresh, bringing the total to **218**.

## Correct Equilibrium region thresholds

- Karamja automatic unlock: **50 tasks**
- First elective region: **150 tasks**
- Second elective region: **275 tasks**
- Third elective region: **400 tasks**

Older tracker values of 175 / 300 / 450 were incorrect and must not be used.

## Recommendation exclusions

Do not recommend these unless the user explicitly reopens them:

- **95 / 96 Croesus** — user does not want to do Croesus.
- **988 Cast a Wave spell** — user explicitly scrapped this recommendation.

Task 131 is completed and is not excluded.

## Tracker discipline

- `live-summary.json`: authoritative live account snapshot and completed task IDs.
- `live-wikisync.json`: raw live WikiSync task IDs and skill levels.
- `live-unfinished.json`: generated unfinished-task database filtered for unlocked regions and manual exclusions.
- `config.json`: manual facts, goals, priorities, owned items, and user preference/task exclusions.
- `latest.json`: historical only; never use it as the live completion baseline.

The current baseline is **Misthalin + Havenhythe + Karamja + Desert**, with **Golden Touch / Divine Druid / Voidwalker / Transmutation / Devout**, **10 blessing tasks**, **218 completed tasks**, and **Invention unlocked**.
