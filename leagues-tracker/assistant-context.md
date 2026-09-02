# Equilibrium assistant state — 112321

Updated: **2026-09-02T00:33:12.994Z**

## Tracker discipline

- `assistant-state.json` is the canonical assistant briefing.
- `recommendations.json` is the canonical precomputed routing/sprint file.
- `task-catalog.json` is the master 1,152-task database.
- `player-state.json` contains only manual facts and choices.
- `live-wikisync.json` is authoritative for completed task IDs and skill levels.
- HiScores is optional and can never block task/skill refreshes.
- Milestones come only from `league-rules.json`; never copy generated totals into manual state.
- Recommendation grades: **A = explicit metadata**, **B = conservative inference**, **U = unknown**.

## Current snapshot

- **9,120 LP** · **260 tasks** · total level **2,031**
- **12 blessing tasks** · relic **T5**
- Regions: **Misthalin, Havenhythe, Karamja, Desert**
- Next region: **15 tasks** to 275
- Next relic: **2,880 LP** to T6
- Next blessing step: **4** to t5

## Active relics

Choice vector: `2 3 3 2 3 - -`

### T1 — Golden Touch
- Goldenhawk boots grant passive Agility XP while moving, skilling, or using ultimate abilities.
- Agility and Thieving can award goldenhawk feathers, which can be converted to Prayer XP or alchemised.
- Agility course base XP and completion coins are doubled.
- Agility obstacles and shortcuts cannot fail.
- Pickpocketing always succeeds; non-coin loot is tripled and noted.
- Stalls do not deplete and safes have no cooldown.
- Repeated Thieving actions continue automatically.
- Coins from Thieving are multiplied by 100.
- Chests and safes can award extra banked herb and potion-ingredient bundles.
Passive tier effects:
- League XP multiplier is 5x.
- Farming crops grow 5x faster.
- Run energy rapidly restores to 100%.
- The Archaeology Guild Shop is fully available without qualification requirements.
- Chronotes from artefacts and collections are multiplied by 5.
- Necromancy ritual souls are increased to 5x normal.
- Standard boss instance spawn times are greatly reduced.
- The Invention tutorial is treated as complete once Invention is unlocked; Invention starts at level 5 and tutorial tools/blueprints are available.

### T2 — Divine Druid
- Thera's Summoning pouch stores grimy herbs and charms.
- Summoning pouches require no spirit shards or empty pouches.
- Thera can teleport to large Summoning obelisks in unlocked regions.
- Grimy herbs can be toggled to become unfinished potions as they are cleaned.
- Cleaning one grimy herb cleans all matching grimy herbs in the inventory.
- Herbs and charms can be obtained while Mining, Fishing, Woodcutting, siphoning Divination springs, and excavating Archaeology hotspots.
- Monster charm drops are multiplied by 5.
- Potion making has a 75% chance to save the secondary ingredient.
- All Meilyr combination potion recipes are unlocked.
- Skill-boosting familiars give triple their normal skill boost.
- Summoning has a 50% chance to create an extra banked pouch and always banks 10 matching scrolls; extras give no XP.
- Divination springs always yield enriched memories.
- Memory conversion and divine-energy conversion use half the normal energy, rounded down.
- Converting memories has a 10% chance to bank a porter or divine charge.
- Crafting from divine energy uses half the usual energy.
- Memory strands are gained at 10x the normal rate.
- Chronicle fragments give double Hunter XP before League multipliers.
Passive tier effects:
- League XP multiplier is 8x.
- Thaler gain is multiplied by 10.
- Selected region drops are 2x as common.
- Slayer points and Reaper points from completed assignments are multiplied by 5.
- Heart of Gielinor, Menaphos, and Farming reputation gains are multiplied by 5.
- Archaeology lore pages are 30% more common.

### T3 — Voidwalker
- The abyssal conduit gives unlimited teleports to destinations covered by many common teleport jewellery items in unlocked regions.
- Skilling can produce void shards.
- Each void shard contains a clue scroll plus one additional reward roll from its League reward pool.
Passive tier effects:
- Applicable skillcape and master-skillcape perks become passive at level 99, except Defence; master perks apply even without level 120.
- Monster kills have a 10% chance to award 8 common or uncommon Invention materials.
- Dungeoneering token gain is multiplied by 3, including Elite Dungeons.

### T4 — Transmutation
- The Deities' Transmuter enables two transmutation spells while carried.
- Alchemical Divergence converts up to 10 resources to a lower tier.
- Alchemical Convergence converts up to 10 resources to a higher tier.
- The transmutation spells have no level requirement.
- Each transmuted item awards 10 base Magic XP before League multipliers.
- The spells automatically recast over time on a stack of noted resources.
- A toggle can bank the noted transmutation products.
- Using a resource on the Transmuter shows its conversion result.
Passive tier effects:
- League XP multiplier is 12x.
- Selected region drops are 4x as common.
- All toolbelt items are unlocked.
- Monster kills have a 20% chance to award 12 common or uncommon Invention materials.
- God Wars Dungeon and Heart of Gielinor encounters require no killcount.
- Ascension Keystones are not required to fight the Legiones.
- Keys to the Crossing are not required to fight the Magister.

### T5 — Devout
- The Devout Yak familiar has 32 inventory slots.
- The familiar can note/unnote items and open the bank from anywhere.
- Ethereal storage scrolls repeat the previous unnote action.
- Stat-boosting familiars award 10 base XP in their matching skill when you gain XP in it, at most once every 6 seconds.
- Summoning scrolls are not consumed.
- Familiar spell-point costs are reduced to 10% of normal.
- Combat familiar damage scales with Summoning level, reaching up to 500% bonus damage at level 99.
Passive tier effects:
- Selected region drops are 6x as common.
- The Sage can swap between already-unlocked spellbooks and prayer books.
- Soul Reaper assignments can be chosen.
- Monster kills have a 20% chance to award 20 common or uncommon Invention materials.
- Augmented items gain item XP 4x faster.
- Dungeoneering token gain is multiplied by 5, including Elite Dungeons.

## Active blessings

Path encoding: `1=Order, 2=Balance, 3=Chaos`

### t1 — Adrenaline Junkie
- Maximum adrenaline is increased by 50%.
- Adrenaline generation is increased by 50%.
Passive step effects:
- 50% chance to save combat runes, rolled separately per rune type.
- 50% chance to save ammunition in combat.
- 50% chance to save ectoplasm and necrotic runes used by abilities/incantations.
- Activating a tier-1 blessing grants one blessing reset.

### t2 — Abyssal Cinders
- Attacks deal 15% ability damage as bonus damage on hit.
- Hits have a 5% chance to trigger Inferno of Zamorak for additional single-target damage.
Passive step effects:
- Dive is automatically unlocked.
- Attack range is increased by one game square, capped at 10 squares.

### t3 — Eternal Sustenance
- Food is not consumed when eaten.
- Eating food costs no adrenaline.
Passive step effects:
- 75% chance to save combat runes, ammunition, ectoplasm, and necrotic runes.
- Movement-ability cooldowns are reduced to 4.2 seconds except Barge and Greater Barge.
- Nature's rune pouch is granted and can hold four rune types.

### god1 — Demon's Mark (derived)
- Accuracy is always calculated using the target's weakness.
Passive step effects:
- Activating the first God-tier blessing grants one blessing reset.
- Araxxi, Rise of the Six, and Vorago rotations can be chosen.

### t4 — True Equilibrium
- For each distinct blessing path represented across tiers 1-6, gain a stack of offensive and defensive stats.
- Each stack grants base ability damage, armour, life points, critical chance, critical damage, and Prayer bonus; one/two/three unique paths grant one/two/three stacks.
Passive step effects:
- All War's Wares rewards are unlocked.
- Maximum adrenaline is increased by 25%.

### Dynamic blessing effect

- **True Equilibrium** currently has **2 stacks**: `{'base_ability_damage': 150, 'armour': 100, 'life_points': 1000, 'critical_strike_chance_percent': 10, 'critical_strike_damage_percent': 15.0, 'prayer_bonus': 10}`

## Changes

- Tasks: **+0** · LP: **+0**

## Current task sprint

- Need: **15 tasks**
- Precomputed sprint: **15 tasks** (15 Grade A, 0 Grade B)
- Action-time estimate excluding travel: **550 sec**
- Prep: oak log, knife, bronze bolts/materials, weapon with a special attack, 25 ashes, potato, bread ingredients, milk, cake ingredients
- [819] **Fletch an oak shortbow (unstrung).** — Grade A · ~15s · bank
- [822] **Fletch 50 bronze bolts.** — Grade A · ~30s · bank
- [980] **Perform a special attack.** — Grade A · ~10s · anywhere
- [844] **Scatter 25 ashes of any kind.** — Grade A · ~25s · anywhere
- [212] **Eat a baked potato.** — Grade A · ~30s · bank_or_range
- [838] **Make some bread.** — Grade A · ~45s · bank_or_range
- [288] **Mine a gem rock at the Al Kharid mine.** — Grade A · ~45s · al_kharid
- [294] **Use any of the magic carpets in the desert.** — Grade A · ~60s · desert
- [35] **Catch some shrimp in the fishing spot to the east of Lumbridge Swamp.** — Grade A · ~30s · lumbridge
- [51] **Churn some butter.** — Grade A · ~45s · lumbridge
- [54] **Use the range in Lumbridge Castle to bake a cake.** — Grade A · ~60s · lumbridge
- [217] **Return a free item to any store.** — Grade A · ~20s · shop
- [285] **Search the Grand Gold Chest in room 1 of Pyramid Plunder in Sophanem.** — Grade A · ~45s · sophanem_pyramid_plunder
- [286] **Search the Grand Gold Chest in room 2 of Pyramid Plunder in Sophanem.** — Grade A · ~60s · sophanem_pyramid_plunder
- [112] **Enter the Cooks' Guild.** — Grade A · ~30s · varrock

## Recommendation coverage

- Timed Grade-A tasks: **16**
- Timed Grade-B inferred candidates: **92**
- Metadata sources: `{'manual_override': 19, 'none': 709, 'text_inference': 164}`

## Data health

- Overall: **healthy**
- WikiSync: **fresh** · 2026-09-02T00:33:12.994Z
- Task catalog: **fresh_unchanged** · 1152 tasks
- HiScores: **fetched_optional** (optional)

> Always apply the active League effects above before normal RS3 mechanics.
