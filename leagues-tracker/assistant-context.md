# Equilibrium assistant state — 112321

Updated: **2026-09-04T11:25:01.657Z**

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

- **12,870 LP** · **306 tasks** · total level **2,280**
- **14 blessing tasks** · relic **T6**
- Regions: **Misthalin, Havenhythe, Karamja, Desert, Asgarnia**
- Next region: **94 tasks** to 400
- Next relic: **7,130 LP** to T7
- Next blessing step: **2** to t5

## Active relics

Choice vector: `2 3 3 2 3 2 -`

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

### T6 — Rejuvenated
- Choose one additional relic from any previous tier.
Passive tier effects:
- League XP multiplier is 16x.
- Selected region drops are 8x as common.
- All Seren spells and Seren prayers are unlocked, though their prerequisite spell/prayer books still need to be unlocked.

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
- Level-ups: Mining 77→84; Hunter 45→50; Summoning 70→71; Divination 80→82

## Current task sprint

- Need: **94 tasks**
- Precomputed sprint: **94 tasks** (6 Grade A, 88 Grade B)
- Action-time estimate excluding travel: **3130 sec**
- Prep: bronze bolts/materials, potato, bread ingredients, milk, cake ingredients
- [822] **Fletch 50 bronze bolts.** — Grade A · ~30s · bank
- [212] **Eat a baked potato.** — Grade A · ~30s · bank_or_range
- [838] **Make some bread.** — Grade A · ~45s · bank_or_range
- [288] **Mine a gem rock at the Al Kharid mine.** — Grade A · ~45s · al_kharid
- [596] **Claim a ticket from Brimhaven Agility Arena.** — Grade B · ~30s · brimhaven
- [602] **Enter the Brimhaven Dungeon.** — Grade B · ~30s · brimhaven_dungeon
- [57] **Smith a mithril platebody on the anvil in the jailhouse sewers.** — Grade B · ~60s · draynor
- [601] **Pick a pineapple on Karamja.** — Grade B · ~30s · karamja
- [606] **Catch a salmon on Karamja.** — Grade B · ~45s · karamja
- [51] **Churn some butter.** — Grade A · ~45s · lumbridge
- [54] **Use the range in Lumbridge Castle to bake a cake.** — Grade A · ~60s · lumbridge
- [14] **Equip the full master runecrafter skilling outfit.** — Grade B · ~20s · unclustered
- [61] **Equip a dragon crossbow.** — Grade B · ~20s · unclustered
- [128] **Equip an Ek-ZekKil.** — Grade B · ~20s · unclustered
- [129] **Equip a Fractured Staff of Armadyl.** — Grade B · ~20s · unclustered
- [130] **Equip either a Dark Shard of Leng or a Dark Sliver of Leng.** — Grade B · ~20s · unclustered
- [225] **Equip a defender.** — Grade B · ~20s · unclustered
- [250] **Equip a seismic wand or seismic singularity.** — Grade B · ~20s · unclustered
- [253] **Equip a piece of masterwork melee armour.** — Grade B · ~20s · unclustered
- [264] **Equip a full set of Bandos armour.** — Grade B · ~20s · unclustered
- [267] **Equip a piece of Torva, Pernix or Virtus armour.** — Grade B · ~20s · unclustered
- [317] **Equip a drygore weapon.** — Grade B · ~20s · unclustered
- [377] **Equip a full set of graahk, larupia or kyatt hunter gear.** — Grade B · ~20s · unclustered
- [615] **Equip an obsidian cape.** — Grade B · ~20s · unclustered
- [618] **Equip a Toktz-Ket-Xil.** — Grade B · ~20s · unclustered
- [619] **Equip a Tzhaar-Ket-Om.** — Grade B · ~20s · unclustered
- [621] **Equip a Toktz-Xil-Ek.** — Grade B · ~20s · unclustered
- [624] **Equip a full set of obsidian armour.** — Grade B · ~20s · unclustered
- [625] **Equip a red topaz machete.** — Grade B · ~20s · unclustered
- [652] **Equip a piece of gemstone armour.** — Grade B · ~20s · unclustered

## Recommendation coverage

- Timed Grade-A tasks: **6**
- Timed Grade-B inferred candidates: **91**
- Metadata sources: `{'manual_override': 9, 'none': 679, 'text_inference': 158}`

## Data health

- Overall: **healthy**
- WikiSync: **fresh** · 2026-09-04T11:25:01.657Z
- Task catalog: **fresh_unchanged** · 1152 tasks
- HiScores: **unavailable_optional** (optional)

> Always apply the active League effects above before normal RS3 mechanics.

## Forgotten-finish opportunities

- [1065] **Reach level 99 in the Crafting skill.** — score 45, 2_skill_levels_or_less; Only 2 Crafting level(s) remain to the task target.
- [796] **Upgrade a set of Death Skull equipment to tier 90.** — score 35, unknown_check_progress; Completed related milestone 70 proves at least 78% of the 90 cumulative target was reached.
- [830] **Smith 100 of any metal weapon or armour piece.** — score 27, unknown_check_progress; Completed related milestone 50 proves at least 50% of the 100 cumulative target was reached.
- [1153] **Reach at least level 30 in all non-elite skills.** — score 25, unknown_check_progress; Lowest relevant skill is Farming 26; 4 levels from the all-skills target.
- [851] **Catch 25 implings of any kind.** — score 8, unknown_check_progress; Completed related milestone 10 proves at least 40% of the 25 cumulative target was reached.
- [852] **Catch 35 implings of any kind.** — score 8, unknown_check_progress; Completed related milestone 10 proves at least 29% of the 35 cumulative target was reached.

> These are evidence-based suspects. Cumulative task families can establish a minimum progress floor, but exact hidden counters are not invented.
