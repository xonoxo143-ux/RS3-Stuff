# RS3 Equilibrium account state — 112321

Refreshed from the live fallback tracker on **2026-08-23 at about 14:08 UTC**.

## Read this first

Use `live-summary.json` as the current account snapshot whenever it is newer than `latest.json`. Keep manually confirmed facts from `config.json`. Do not carry forward old strategy assumptions that are not present in `config.json`.

### Current concrete state

- **4,250 LP**
- **158 tasks** completed
- **17 tasks** to the first elective-region unlock at 175
- **T4 relic tier unlocked**; T4 relic choice is **not yet confirmed in the tracker**
- **4 blessing tasks** completed
- **1 blessing task** to the 5-task blessing threshold
- **Total level 1,249**
- Confirmed unlocked regions: **Misthalin, Havenhythe, Karamja**
- Confirmed first elective region pick: **Asgarnia**
- Later elective region choices: **unset until reconfirmed**
- Confirmed relic picks: **T1 Golden Touch, T2 Divine Druid, T3 Voidwalker**

### Current skill levels

| Skill | Level |
|---|---:|
| Thieving | 100 |
| Agility | 99 |
| Prayer | 96 |
| Necromancy | 71 |
| Crafting | 70 |
| Defence | 66 |
| Magic | 64 |
| Constitution | 62 |
| Mining | 60 |
| Fletching | 52 |
| Runecrafting | 51 |
| Cooking | 50 |
| Smithing | 48 |
| Woodcutting | 43 |
| Summoning | 39 |
| Herblore | 38 |
| Attack | 36 |
| Strength | 36 |
| Divination | 34 |
| Fishing | 32 |
| Firemaking | 29 |
| Ranged | 28 |
| Archaeology | 19 |
| Slayer | 19 |
| Farming | 2 |
| Hunter | 2 |
| Construction | 1 |
| Dungeoneering | 1 |
| Invention | 1 |

## Recent notable progress visible in the refreshed snapshot

- Thieving reached **100**.
- Necromancy reached **71**.
- Prayer reached **96**.
- Crafting reached **70**.
- Defence reached **66**.
- Magic reached **64**.
- Runecrafting reached **51**.
- Completed-task count rose to **158** and LP to **4,250**.
- Blessing-task count rose to **4**.
- New tracked completions include the **Arch-Glacor blessing task** and **Ivar, King of Bones blessing task**.

## Source discipline

- `live-summary.json`: freshest live WikiSync + Equilibrium task-catalog fallback snapshot.
- `config.json`: manual facts the APIs cannot reliably infer, especially region/relic choices.
- `task-catalog.json`: full Equilibrium task database.
- `latest.json` / older generated files: useful historical data, but **do not treat them as current if their timestamp predates `live-summary.json`**.

The previous Tirannwn-first plan is obsolete. **Asgarnia is the confirmed first elective pick.**
