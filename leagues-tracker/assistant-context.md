# RS3 Equilibrium account state — 112321

Refreshed from live WikiSync on **2026-08-24 at 22:59 UTC**.

## Read this first

Use `live-summary.json` as the authoritative current account snapshot. Use `live-unfinished.json` for task recommendations and honor `config.json` recommendation exclusions. Treat all gameplay advice in an **Equilibrium-first** context: unlocked regions, League quest overrides, relic/passive effects, blessings, XP multipliers, and task requirements come before normal-RS3 assumptions.

### Current concrete state

- **5,480 LP**
- **183 tasks** completed
- **117 tasks** to the second elective-region unlock at 300
- **T4 relic tier unlocked**
- **520 LP** to T5 at 6,000 LP
- **6 blessing tasks** completed
- **Total level 1,509**
- Confirmed unlocked regions: **Misthalin, Havenhythe, Karamja, Desert**
- Later elective region choices: **unset until reconfirmed**
- Confirmed relic picks: **T1 Golden Touch, T2 Divine Druid, T3 Voidwalker, T4 Transmutation**
- Confirmed third blessing: **Eternal Sustenance**

### Current skill levels

| Skill | Level |
|---|---:|
| Thieving | 104 |
| Agility | 99 |
| Prayer | 99 |
| Necromancy | 84 |
| Defence | 80 |
| Constitution | 78 |
| Crafting | 75 |
| Magic | 66 |
| Mining | 65 |
| Cooking | 61 |
| Attack | 60 |
| Strength | 60 |
| Fletching | 58 |
| Herblore | 57 |
| Slayer | 57 |
| Runecrafting | 55 |
| Smithing | 54 |
| Woodcutting | 53 |
| Firemaking | 51 |
| Archaeology | 47 |
| Summoning | 45 |
| Divination | 34 |
| Fishing | 32 |
| Ranged | 28 |
| Farming | 2 |
| Hunter | 2 |
| Construction | 1 |
| Dungeoneering | 1 |
| Invention | 1 |

## Recent live changes

- WikiSync rose to **183 tasks / 5,480 LP**.
- Newly observed task **908: Craft 1,000 runes** completed for **30 LP** after the user crafted 1,500 earth runes at once.
- Newly observed task **1205: Defeat Ivar while wielding the Bonecrushing maul** completed for **80 LP**.
- Runecrafting rose **51 → 55**.
- Archaeology rose **41 → 47**.
- Attack and Strength reached **60**.
- Firemaking reached **51**.

## Recommendation exclusions

Do not recommend these unless the user explicitly reopens them:

- **95 / 96 Croesus** — user does not want to do Croesus.
- **988 Cast a Wave spell** — user explicitly scrapped this recommendation.
- **131 Craft 100 earth runes simultaneously** — WikiSync still shows it incomplete after a 1,500-earth-rune craft. Current Equilibrium reports indicate Void-Shard/League-sourced essence can fail to trigger it. Keep excluded unless retrying with normal pure essence is explicitly requested.

## Tracker discipline

- `live-summary.json`: authoritative live account snapshot and completed task IDs.
- `live-wikisync.json`: raw live WikiSync task IDs and skill levels.
- `live-unfinished.json`: generated unfinished-task database filtered for unlocked regions and manual exclusions.
- `config.json`: manual facts and user preference/task exclusions.
- `latest.json`: historical only; never use it as the live completion baseline.

The current baseline is **Misthalin + Havenhythe + Karamja + Desert**, with **Golden Touch / Divine Druid / Voidwalker / Transmutation** and **Eternal Sustenance**.
