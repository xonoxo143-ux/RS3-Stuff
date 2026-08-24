# RS3 Equilibrium account state — 112321

Refreshed from the live fallback tracker on **2026-08-24 at about 05:18 UTC**.

## Read this first

Use `live-summary.json` as the current account snapshot whenever it is newer than `latest.json`. Keep manually confirmed facts from `config.json`. Do not carry forward old strategy assumptions that are not present in `config.json`.

### Current concrete state

- **4,270 LP**
- **160 tasks** completed
- **15 tasks** to the first elective-region unlock at 175
- **T4 relic tier unlocked**; T4 relic choice is **not yet confirmed in the tracker**
- **4 blessing tasks** completed
- **1 blessing task** to the 5-task blessing threshold
- **Total level 1,265**
- Confirmed unlocked regions: **Misthalin, Havenhythe, Karamja**
- Confirmed first elective region pick: **Asgarnia**
- Later elective region choices: **unset until reconfirmed**
- Confirmed relic picks: **T1 Golden Touch, T2 Divine Druid, T3 Voidwalker**

### Current skill levels

| Skill | Level |
|---|---:|
| Thieving | 100 |
| Agility | 99 |
| Prayer | 97 |
| Necromancy | 75 |
| Crafting | 70 |
| Defence | 67 |
| Magic | 65 |
| Constitution | 63 |
| Mining | 60 |
| Fletching | 52 |
| Runecrafting | 51 |
| Cooking | 51 |
| Smithing | 48 |
| Woodcutting | 43 |
| Herblore | 38 |
| Firemaking | 36 |
| Summoning | 39 |
| Attack | 36 |
| Strength | 36 |
| Divination | 34 |
| Fishing | 32 |
| Ranged | 28 |
| Archaeology | 19 |
| Slayer | 19 |
| Farming | 2 |
| Hunter | 2 |
| Construction | 1 |
| Dungeoneering | 1 |
| Invention | 1 |

## Recent notable progress visible in the refreshed snapshot

- Completed-task count is now **160** and LP is **4,270**.
- Necromancy reached **75**.
- Prayer reached **97**.
- Defence reached **67**.
- Magic reached **65**.
- Firemaking reached **36**.
- New tracked completions since the previous live snapshot include **Conjure a Skeleton Warrior** and **Conjure a Vengeful Ghost** at the City of Um ritual site.

## Source discipline

- `live-summary.json`: freshest live WikiSync + Equilibrium task-catalog fallback snapshot.
- `config.json`: manual facts the APIs cannot reliably infer, especially region/relic choices.
- `task-catalog.json`: full Equilibrium task database.
- `latest.json` / older generated files: useful historical data, but **do not treat them as current if their timestamp predates `live-summary.json`**.

The previous Tirannwn-first plan is obsolete. **Asgarnia is the confirmed first elective pick.**
