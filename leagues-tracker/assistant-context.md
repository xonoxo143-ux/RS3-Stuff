# RS3 Equilibrium account state — 112321

Refreshed from the live fallback tracker on **2026-08-24 at about 20:55 UTC**.

## Read this first

Use `live-summary.json` as the current account snapshot whenever it is newer than `latest.json`. Keep manually confirmed facts from `config.json`. Treat all gameplay advice in an **Equilibrium-first** context: account for unlocked regions, League quest overrides, relic/passive effects, blessing effects, XP multipliers, and task requirements before applying normal-RS3 advice.

### Current concrete state

- **5,170 LP**
- **180 tasks** completed
- First elective-region threshold at 175 is complete
- **120 tasks** to the second elective-region unlock at 300
- **T4 relic tier unlocked**
- **830 LP** to T5 at 6,000 LP
- **6 blessing tasks** completed
- **3 blessing tasks** to the 9-task blessing threshold
- **Total level 1,477**
- Confirmed unlocked regions: **Misthalin, Havenhythe, Karamja, Desert**
- Later elective region choices: **unset until reconfirmed**
- Confirmed relic picks: **T1 Golden Touch, T2 Divine Druid, T3 Voidwalker, T4 Transmutation**
- Confirmed third blessing: **Eternal Sustenance**

### Current skill levels

| Skill | Level |
|---|---:|
| Thieving | 101 |
| Agility | 99 |
| Prayer | 98 |
| Necromancy | 84 |
| Defence | 80 |
| Constitution | 77 |
| Crafting | 75 |
| Magic | 66 |
| Mining | 64 |
| Cooking | 61 |
| Attack | 58 |
| Strength | 58 |
| Herblore | 57 |
| Slayer | 57 |
| Fletching | 56 |
| Smithing | 52 |
| Woodcutting | 51 |
| Runecrafting | 51 |
| Firemaking | 45 |
| Summoning | 45 |
| Archaeology | 41 |
| Divination | 34 |
| Fishing | 32 |
| Ranged | 28 |
| Farming | 2 |
| Hunter | 2 |
| Construction | 1 |
| Dungeoneering | 1 |
| Invention | 1 |

## Recent notable progress visible in the refreshed snapshot

- Completed-task count rose from **160 to 180**.
- LP rose from **4,270 to 5,170**.
- Blessing-task count rose from **4 to 6**.
- The first elective region is now **Desert**, confirmed manually in `config.json`.
- **Hermod** is now complete as a blessing task (task 76).
- **Silverquill** is now complete as a blessing task (task 1206).
- Combat level 100 task (145) is complete.
- Easy clue task (869) is complete.
- The **spin 5 bowstrings** task (861) and **spin a ball of wool** task (863) are complete.
- **Catch an anchovy** (178), **cook 200 fish** (836), **mine 30 adamantite** (889), and **burn 25 willow logs** (920) are complete.
- Archaeology jumped to **41**, Slayer to **57**, Necromancy to **84**, Defence to **80**, and Thieving to **101**.

## Source discipline

- `live-summary.json`: freshest live WikiSync + Equilibrium task-catalog fallback snapshot.
- `live-wikisync.json`: authoritative live completed task IDs and skill levels.
- `config.json`: manual facts APIs cannot reliably infer, especially region/relic/blessing choices.
- `task-catalog.json`: full Equilibrium task database.
- `latest.json` / older generated files: historical only when older than the live files.

The current League baseline is **Misthalin + Havenhythe + Karamja + Desert**, with **Golden Touch / Divine Druid / Voidwalker / Transmutation** and **Eternal Sustenance**. Do not resurrect older Tirannwn-first or Asgarnia-first assumptions.
