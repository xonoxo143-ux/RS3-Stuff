# Equilibrium assistant state — 112321

Updated: **2026-09-02T00:24:47.677Z**

## Tracker discipline

- `assistant-state.json` is the canonical assistant briefing.
- `task-catalog.json` is the master 1,152-task database.
- `player-state.json` contains only manual facts and choices.
- `live-wikisync.json` is authoritative for completed task IDs and skill levels.
- HiScores is optional and can never block task/skill refreshes.
- Milestones come only from `league-rules.json`; do not copy generated totals into manual state.

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

- Tasks: **+7** · LP: **+250**
- [810] Drink a strength potion. — easy, Global, 10 LP
- [811] Make an attack potion. — easy, Global, 10 LP
- [812] Make a necromancy potion. — easy, Global, 10 LP
- [915] Equip a full set of blue dragonhide armour. — medium, Global, 30 LP
- [916] Equip a full set of red dragonhide armour. — medium, Global, 30 LP
- [986] Equip a full set of black dragonhide armour. — hard, Global, 80 LP
- [987] Equip a full set of royal dragonhide armour. — hard, Global, 80 LP
- Level-ups: Ranged 28→52; Magic 74→76; Fletching 67→69

## Fast task routing

- Enriched skill/region-ready: **16**
- Manual-check: **3**
- Accessible but requirements not yet mapped: **433**

- [980] **Perform a special attack.** — ~10s · anywhere · prep: weapon with a special attack
- [819] **Fletch an oak shortbow (unstrung).** — ~15s · bank · prep: oak log, knife
- [217] **Return a free item to any store.** — ~20s · shop
- [844] **Scatter 25 ashes of any kind.** — ~25s · anywhere · prep: 25 ashes
- [112] **Enter the Cooks' Guild.** — ~30s · varrock
- [35] **Catch some shrimp in the fishing spot to the east of Lumbridge Swamp.** — ~30s · lumbridge
- [212] **Eat a baked potato.** — ~30s · bank_or_range · prep: potato
- [822] **Fletch 50 bronze bolts.** — ~30s · bank · prep: bronze bolts/materials
- [51] **Churn some butter.** — ~45s · lumbridge · prep: milk
- [285] **Search the Grand Gold Chest in room 1 of Pyramid Plunder in Sophanem.** — ~45s · sophanem_pyramid_plunder
- [288] **Mine a gem rock at the Al Kharid mine.** — ~45s · al_kharid
- [838] **Make some bread.** — ~45s · bank_or_range · prep: bread ingredients
- [54] **Use the range in Lumbridge Castle to bake a cake.** — ~60s · lumbridge · prep: cake ingredients
- [286] **Search the Grand Gold Chest in room 2 of Pyramid Plunder in Sophanem.** — ~60s · sophanem_pyramid_plunder
- [294] **Use any of the magic carpets in the desert.** — ~60s · desert
- [287] **Search the Grand Gold Chest in room 3 of Pyramid Plunder in Sophanem.** — ~75s · sophanem_pyramid_plunder

## Data health

- WikiSync: **fresh** · 2026-09-02T00:24:47.677Z
- Task catalog: **fresh_updated** · 1152 tasks
- HiScores: **fetched_optional** (optional)

> Always apply the active League effects above before normal RS3 mechanics.
