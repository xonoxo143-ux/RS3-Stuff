# RS3 Equilibrium account state — 112321

Updated from the live fallback tracker on **2026-08-22 around 23:34 UTC**.

## Read this first

Use `live-summary.json` as the current account snapshot whenever it is newer than `latest.json`. Keep manually confirmed facts from `config.json`. Do not carry forward old strategy assumptions that are not present in `config.json`.

### Current concrete state

- **3,760 LP**
- **145 tasks** completed
- **T4 relic tier unlocked**; T4 relic choice is **not yet confirmed in the tracker**
- **2 blessing tasks** completed
- **Total level 1,147**
- Confirmed unlocked regions: **Misthalin, Havenhythe, Karamja**
- Confirmed first elective region pick: **Asgarnia**
- First elective region unlock threshold: **175 tasks**
- Later elective region choices: **unset until reconfirmed**
- Confirmed relic picks: **T1 Golden Touch, T2 Divine Druid, T3 Voidwalker**

### Current skill levels

| Skill | Level |
|---|---:|
| Agility | 99 |
| Thieving | 96 |
| Prayer | 92 |
| Crafting | 67 |
| Mining | 60 |
| Magic | 56 |
| Defence | 54 |
| Fletching | 52 |
| Constitution | 51 |
| Cooking | 49 |
| Necromancy | 46 |
| Smithing | 45 |
| Woodcutting | 42 |
| Summoning | 37 |
| Attack | 36 |
| Strength | 36 |
| Divination | 34 |
| Runecrafting | 33 |
| Fishing | 32 |
| Firemaking | 29 |
| Herblore | 28 |
| Ranged | 28 |
| Archaeology | 19 |
| Slayer | 19 |
| Farming | 2 |
| Hunter | 2 |
| Construction | 1 |
| Dungeoneering | 1 |
| Invention | 1 |

## Source discipline

- `live-summary.json`: freshest live WikiSync + Equilibrium task-catalog fallback snapshot.
- `config.json`: manual facts the APIs cannot reliably infer, especially region/relic choices.
- `task-catalog.json`: full Equilibrium task database.
- `latest.json` / older generated files: useful historical data, but **do not treat them as current if their timestamp predates `live-summary.json`**.

The previous Tirannwn-first plan is obsolete. **Asgarnia is the confirmed first elective pick.**
