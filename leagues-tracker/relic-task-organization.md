# T6 Relic Task Organization

Generated from the unfinished-task map at 2026-09-03T22:37:56.340Z. Current baseline: 299 completed tasks, 12170 LP.

This file is deliberately **pre-math**. It organizes tasks by system and completion shape, identifies which relics plausibly attack each group's bottlenecks, and marks groups that must be decomposed before compatibility percentages are assigned.

## Rules

- Task-centered analysis: relics are compared against task groups and representative singular tasks, not tasks assigned to a single relic.
- Two orthogonal labels: domain/system and completion shape.
- Group compatibility is qualitative only at this stage: primary, supporting, edge-only, usually-neutral.
- Composite/RNG/equipment/meta tasks must be decomposed before numeric scoring.
- Existing relics Golden Touch, Divine Druid, Voidwalker, Transmutation and Devout are the baseline; candidate value is incremental.

## Broad groups

| Group | Unfinished | Accessible now | Unfinished LP | Accessible LP | Subgroups |
|---|---:|---:|---:|---:|---:|
| Progression | 72 | 72 | 14,350 | 14,350 | 29 |
| Combat | 165 | 79 | 24,150 | 13,750 | 3 |
| Equipment & acquisition | 100 | 53 | 13,220 | 7,430 | 3 |
| Production | 67 | 45 | 6,760 | 3,820 | 12 |
| Clues | 41 | 41 | 3,720 | 3,720 | 4 |
| Access / meta / one-offs | 110 | 48 | 6,380 | 3,210 | 3 |
| Gathering | 76 | 36 | 7,720 | 2,840 | 9 |
| Farming | 37 | 19 | 3,480 | 1,660 | 4 |
| Magic systems | 36 | 18 | 3,270 | 1,600 | 5 |
| Relic-neutral / bespoke | 54 | 24 | 4,490 | 1,130 | 1 |
| Activities | 18 | 9 | 1,870 | 1,030 | 1 |
| Slayer | 7 | 6 | 1,100 | 900 | 3 |
| Projects & construction | 12 | 10 | 1,160 | 730 | 1 |
| Collections & RNG | 12 | 5 | 1,880 | 590 | 1 |
| Other skills | 36 | 12 | 2,350 | 560 | 5 |
| Archaeology | 10 | 4 | 1,310 | 270 | 4 |

## Completion shapes

- **atomic** — One main completion event or short fixed chain.
- **counted** — Repeated homogeneous action/resource count.
- **threshold** — Level, XP, currency, reputation or score threshold.
- **rng** — Completion dominated by probabilistic acquisition.
- **composite** — Bundle of distinct requirements; must decompose.
- **access** — Quest, unlock, travel or access gate.

## Group-to-relic map

`Primary` means the relic generally attacks the subgroup's dominant bottleneck. `Supporting` means partial but meaningful help. `Edge-only` means inspect the singular task before scoring.

### Access / meta / one-offs

#### Area task set

- Scope: **44** unfinished / **24** accessible now; **3,570 LP** total / **1,870 LP** accessible.
- Shapes: composite 44.
- Primary: —
- Supporting: —
- Edge-only: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- **Must decompose individually before numeric scoring.**
- Note: Area task sets are composite wrappers; compatibility is inherited from their unfinished component achievements.
- Anchors:
  - [21] Complete the task set: Elite Varrock. — 200 LP — accessible — composite
  - [26] Complete the task set: Beginner Lumbridge. — 30 LP — accessible — composite
  - [419] Complete the task set: Elite Fremennik. — 200 LP — locked — composite

#### Quest / miniquest

- Scope: **15** unfinished / **7** accessible now; **490 LP** total / **190 LP** accessible.
- Shapes: access 15.
- Primary: —
- Supporting: —
- Edge-only: —
- Usually neutral: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- Anchors:
  - [23] Complete the quest: New Foundations. — 30 LP — accessible — access
  - [228] Complete the quest: Witch's House. — 10 LP — accessible — access
  - [499] Complete the quest: Osseous Rex. — 80 LP — locked — access

#### Travel / interaction / unlock

- Scope: **51** unfinished / **17** accessible now; **2,320 LP** total / **1,150 LP** accessible.
- Shapes: atomic 9, access 42.
- Primary: —
- Supporting: —
- Edge-only: Crystal Grace, Antiquarian
- Note: Most are relic-neutral. Voidwalker teleport coverage is already baseline and should absorb much of the travel advantage.
- Anchors:
  - [272] Unlock all the prayers from the Praesul Codex. — 400 LP — accessible — access
  - [229] Sit down with Tiffy in Falador park. — 10 LP — accessible — atomic
  - [511] Unlock the 'double Surge' or 'double Escape' ability upgrade. — 200 LP — locked — access

### Activities

#### Minigame / activity

- Scope: **18** unfinished / **9** accessible now; **1,870 LP** total / **1,030 LP** accessible.
- Shapes: atomic 14, access 2, threshold 1, rng 1.
- Primary: —
- Supporting: —
- Edge-only: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- **Must decompose individually before numeric scoring.**
- Note: Minigames are mechanically heterogeneous; group only for organization, then inspect representative activities individually.
- Anchors:
  - [252] Unlock the Royale Cannon from the Artisans' Workshop reward shop. — 200 LP — accessible — access
  - [45] Complete world 25 in Shattered Worlds. — 30 LP — accessible — atomic
  - [535] Search the rare chest in the Asuran Arsenal Heist in 6 minutes or less. — 200 LP — locked — rng

### Archaeology

#### Excavation / progression

- Scope: **1** unfinished / **1** accessible now; **80 LP** total / **80 LP** accessible.
- Shapes: atomic 1.
- Primary: Antiquarian
- Supporting: Endless Harvest, Survivalist
- Edge-only: —
- Note: Antiquarian is a modular three-power system, not merely Archaeology QoL; choose loadout per task family.
- Anchors:
  - [1211] Uncover the depths of the Moonrise digsite. — 80 LP — accessible — atomic

#### Mysteries

- Scope: **5** unfinished / **0** accessible now; **960 LP** total / **0 LP** accessible.
- Shapes: atomic 5.
- Primary: Antiquarian
- Supporting: Endless Harvest, Survivalist
- Edge-only: —
- Note: Antiquarian is a modular three-power system, not merely Archaeology QoL; choose loadout per task family.
- Edge case: Some mysteries are gated by fixed lore/access steps that throughput relics do not compress.
- Anchors:
  - [1012] Solve the Archaeology mystery: Mysterious City. — 400 LP — locked — atomic

#### Relics / monolith

- Scope: **1** unfinished / **1** accessible now; **80 LP** total / **80 LP** accessible.
- Shapes: atomic 1.
- Primary: Antiquarian
- Supporting: Endless Harvest, Survivalist
- Edge-only: —
- Note: Antiquarian is a modular three-power system, not merely Archaeology QoL; choose loadout per task family.
- Anchors:
  - [120] Harness the power of three relics at once. — 80 LP — accessible — atomic

#### Restoration / collections

- Scope: **3** unfinished / **2** accessible now; **190 LP** total / **110 LP** accessible.
- Shapes: atomic 2, composite 1.
- Primary: Antiquarian
- Supporting: Endless Harvest, Survivalist
- Edge-only: —
- Note: Antiquarian is a modular three-power system, not merely Archaeology QoL; choose loadout per task family.
- Anchors:
  - [1209] Complete the 'Museum - Guthixian I' and 'Museum - Guthixian II' collections. — 80 LP — accessible — composite
  - [1213] Bring a restored bloodwine artefact to Anya. — 30 LP — accessible — atomic
  - [688] Restore an artefact from the Daemonheim digsite. — 80 LP — locked — atomic

### Clues

#### Completion counts

- Scope: **16** unfinished / **16** accessible now; **1,240 LP** total / **1,240 LP** accessible.
- Shapes: atomic 16.
- Primary: Clue Connoisseur
- Supporting: —
- Edge-only: —
- Note: Treat Voidwalker clue acquisition as baseline, not candidate value.
- Edge case: Extra casket does not count as an extra clue completion.
- Anchors:
  - [995] Complete 75 elite clue scrolls. — 200 LP — accessible — atomic
  - [870] Complete 25 easy clue scrolls. — 30 LP — accessible — atomic

#### Infrastructure / other clue

- Scope: **1** unfinished / **1** accessible now; **10 LP** total / **10 LP** accessible.
- Shapes: atomic 1.
- Primary: Clue Connoisseur
- Supporting: —
- Edge-only: —
- Note: Treat Voidwalker clue acquisition as baseline, not candidate value.
- Anchors:
  - [868] Store the items required for an emote clue in a Treasure Trail hidey-hole. — 10 LP — accessible — atomic

#### Rare clue rewards

- Scope: **1** unfinished / **1** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: rng 1.
- Primary: Clue Connoisseur
- Supporting: —
- Edge-only: —
- Note: Treat Voidwalker clue acquisition as baseline, not candidate value.
- Edge case: Still RNG; extra casket + max rolls changes probability, not certainty.
- Anchors:
  - [1145] Obtain a dye, or a piece of Third-age or Second-age gear from a clue scroll. — 400 LP — accessible — rng

#### Reward collection logs

- Scope: **23** unfinished / **23** accessible now; **2,070 LP** total / **2,070 LP** accessible.
- Shapes: atomic 23.
- Primary: Clue Connoisseur
- Supporting: —
- Edge-only: —
- Note: Treat Voidwalker clue acquisition as baseline, not candidate value.
- Anchors:
  - [948] Collect 75 unique items for the hard clue rewards collection log. — 200 LP — accessible — atomic
  - [873] Collect 10 unique items for the general clue rewards collection log. — 10 LP — accessible — atomic

### Collections & RNG

#### Collection / rare acquisition

- Scope: **12** unfinished / **5** accessible now; **1,880 LP** total / **590 LP** accessible.
- Shapes: rng 7, composite 3, atomic 2.
- Primary: —
- Supporting: —
- Edge-only: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- **Must decompose individually before numeric scoring.**
- Note: Identify the source of the RNG first: boss drop, skilling rare, breeding, shop/currency, etc.
- Anchors:
  - [471] Obtain a crystal geode from a crystal tree. — 200 LP — accessible — rng
  - [891] Open 20 igneous geodes. — 30 LP — accessible — rng
  - [1010] Purchase the 'Very Good Baiter' title. — 400 LP — locked — atomic

### Combat

#### Boss / combat completion

- Scope: **122** unfinished / **60** accessible now; **14,820 LP** total / **8,710 LP** accessible.
- Shapes: atomic 120, counted 2.
- Primary: Perkfection
- Supporting: Antiquarian
- Edge-only: Assassin's Insight
- Note: Perkfection is broad but modest; do not read its 20% perk-proc modifier as +20% DPS. Numeric stage should sensitivity-test combat time saving.
- Edge case: Assassin only applies where a real Slayer assignment grants the helmet effect.
- Anchors:
  - [1162] Defeat Amascut, the Devourer. — 400 LP — accessible — atomic
  - [227] Kill a goblin raider boss in the Goblin Village. — 10 LP — accessible — atomic
  - [1265] Defeat Solak, Guardian of the Grove while completing the listed achievements. — 400 LP — locked — atomic

#### Mastery / challenge

- Scope: **24** unfinished / **16** accessible now; **6,640 LP** total / **4,560 LP** accessible.
- Shapes: atomic 6, counted 5, composite 13.
- Primary: Perkfection
- Supporting: Antiquarian
- Edge-only: Assassin's Insight
- **Must decompose individually before numeric scoring.**
- Note: Perkfection is broad but modest; do not read its 20% perk-proc modifier as +20% DPS. Numeric stage should sensitivity-test combat time saving.
- Edge case: Assassin only applies where a real Slayer assignment grants the helmet effect.
- Edge case: Mastery bundles often contain mechanical/survival requirements that raw DPS does not reduce.
- Anchors:
  - [126] Defeat the Arch-Glacor in hard mode. — 400 LP — accessible — atomic
  - [655] Complete all TzTok-Jad Combat Mastery achievements. — 80 LP — accessible — composite
  - [789] Complete all Araxxi Combat Mastery achievements. — 400 LP — locked — composite

#### Repeated kills

- Scope: **19** unfinished / **3** accessible now; **2,690 LP** total / **480 LP** accessible.
- Shapes: counted 19.
- Primary: Perkfection
- Supporting: Antiquarian
- Edge-only: Assassin's Insight
- Note: Perkfection is broad but modest; do not read its 20% perk-proc modifier as +20% DPS. Numeric stage should sensitivity-test combat time saving.
- Edge case: Assassin only applies where a real Slayer assignment grants the helmet effect.
- Anchors:
  - [59] Defeat 50 tormented demons. — 200 LP — accessible — counted
  - [336] Slay a combination of 500 corrupted or devourer creatures. — 80 LP — accessible — counted
  - [410] Defeat 20 Acheron mammoths. — 200 LP — locked — counted

### Equipment & acquisition

#### Equip / obtain

- Scope: **96** unfinished / **49** accessible now; **12,340 LP** total / **6,550 LP** accessible.
- Shapes: atomic 96.
- Primary: —
- Supporting: —
- Edge-only: Perkfection, Assassin's Insight, Clue Connoisseur, Production Master, Superheated, Survivalist, Endless Harvest, Animal Wrangler, Nature's Network, Crystal Grace, Antiquarian
- **Must decompose individually before numeric scoring.**
- Note: The equip click is trivial; score the acquisition chain (drop, shop, crafting, clue, skill requirement) instead.
- Anchors:
  - [128] Equip an Ek-ZekKil. — 400 LP — accessible — atomic
  - [225] Equip a defender. — 30 LP — accessible — atomic
  - [718] Equip an eldritch crossbow. — 400 LP — locked — atomic

#### Masterwork equipment

- Scope: **2** unfinished / **2** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: atomic 2.
- Primary: Production Master
- Supporting: Superheated
- Edge-only: Survivalist, Endless Harvest
- **Must decompose individually before numeric scoring.**
- Note: Production Master collapses special Masterwork processing; Superheated helps ore/bar/ordinary Smithing but not folding/assembly.
- Anchors:
  - [1140] Equip a full set of masterwork armour. — 400 LP — accessible — atomic
  - [253] Equip a piece of masterwork melee armour. — 200 LP — accessible — atomic

#### Upgrade chain

- Scope: **2** unfinished / **2** accessible now; **280 LP** total / **280 LP** accessible.
- Shapes: atomic 2.
- Primary: —
- Supporting: —
- Edge-only: Perkfection, Assassin's Insight, Clue Connoisseur, Production Master, Superheated, Survivalist, Endless Harvest, Animal Wrangler, Nature's Network, Crystal Grace, Antiquarian
- **Must decompose individually before numeric scoring.**
- Note: The equip click is trivial; score the acquisition chain (drop, shop, crafting, clue, skill requirement) instead.
- Anchors:
  - [796] Upgrade a set of Death Skull equipment to tier 90. — 200 LP — accessible — atomic
  - [1199] Upgrade a havensilver weapon to tier 60. — 80 LP — accessible — atomic

### Farming

#### Animals / breeding

- Scope: **6** unfinished / **0** accessible now; **870 LP** total / **0 LP** accessible.
- Shapes: atomic 2, threshold 1, composite 1, rng 2.
- Primary: Animal Wrangler
- Supporting: —
- Edge-only: Nature's Network
- Anchors:
  - [528] Breed a shiny dinosaur. — 400 LP — locked — rng

#### Growth / check

- Scope: **5** unfinished / **3** accessible now; **200 LP** total / **140 LP** accessible.
- Shapes: atomic 5.
- Primary: Nature's Network
- Supporting: —
- Edge-only: —
- Note: Nature's Network directly deletes crop growth time.
- Anchors:
  - [58] Fully grow a magic tree in Lumbridge. — 80 LP — accessible — atomic
  - [613] Check a grown banana tree on Karamja. — 30 LP — accessible — atomic
  - [440] Check a grown papaya tree inside Tree Gnome Stronghold. — 30 LP — locked — atomic

#### Harvesting

- Scope: **21** unfinished / **12** accessible now; **2,010 LP** total / **1,200 LP** accessible.
- Shapes: atomic 11, counted 10.
- Primary: Nature's Network
- Supporting: Endless Harvest
- Edge-only: —
- Anchors:
  - [251] Harvest some starbloom flowers from the flower patch south of Falador. — 200 LP — accessible — atomic
  - [295] Harvest a rose at Het's Oasis. — 10 LP — accessible — atomic
  - [514] Harvest a dragonfruit plant in the cactus patch in the north of Anachronia. — 200 LP — locked — atomic

#### Planting

- Scope: **5** unfinished / **4** accessible now; **400 LP** total / **320 LP** accessible.
- Shapes: counted 2, atomic 3.
- Primary: Nature's Network
- Supporting: —
- Edge-only: —
- Edge case: No public proof that one herb seed 'counting as ten' advances the generic League planting-action counter ten times; score that counter bonus as zero until tested.
- Anchors:
  - [1042] Plant an avocado seed in a bush patch. — 200 LP — accessible — atomic
  - [204] Plant seeds in any farming patch 10 times. — 10 LP — accessible — counted
  - [555] Plant a mushroom seed in the mushroom patch in Isafdar. — 80 LP — locked — atomic

### Gathering

#### Fishing atomic

- Scope: **10** unfinished / **3** accessible now; **750 LP** total / **260 LP** accessible.
- Shapes: atomic 10.
- Primary: —
- Supporting: Animal Wrangler, Survivalist, Endless Harvest
- Edge-only: Superheated, Antiquarian
- Anchors:
  - [1049] Catch a cavefish. — 200 LP — accessible — atomic
  - [306] Catch a catfish. — 30 LP — accessible — atomic
  - [1259] Catch a crystal urchin at the Prifddinas Waterfall. — 200 LP — locked — atomic

#### Fishing quantity / action

- Scope: **12** unfinished / **9** accessible now; **1,070 LP** total / **590 LP** accessible.
- Shapes: counted 12.
- Primary: Animal Wrangler
- Supporting: Survivalist, Endless Harvest
- Edge-only: Superheated, Antiquarian
- Note: Superheated/Bait and Switch are side-skill synergies if Cooking is simultaneously valuable.
- Edge case: Distinguish item-quantity tasks from 'catch N times' action counters. Bonus fish are confirmed useful for fish-quantity tasks, not every action counter.
- Anchors:
  - [1045] Catch 150 rocktail. — 200 LP — accessible — counted
  - [184] Catch any fish 200 times. — 30 LP — accessible — counted
  - [1046] Catch 200 sailfish. — 200 LP — locked — counted

#### Hunter atomic / RNG

- Scope: **8** unfinished / **5** accessible now; **810 LP** total / **570 LP** accessible.
- Shapes: atomic 8.
- Primary: Animal Wrangler
- Supporting: —
- Edge-only: —
- Edge case: 5x loot helps loot-mark objectives, but rare-spawn availability can remain the dominant bottleneck.
- Anchors:
  - [1053] Catch a dragon impling. — 200 LP — accessible — atomic
  - [1182] Catch a jackalope. — 10 LP — accessible — atomic
  - [582] Catch a crystal impling. — 200 LP — locked — atomic

#### Hunter quantity

- Scope: **11** unfinished / **4** accessible now; **750 LP** total / **170 LP** accessible.
- Shapes: counted 11.
- Primary: Animal Wrangler
- Supporting: —
- Edge-only: —
- Edge case: 5x loot helps loot-mark objectives, but rare-spawn availability can remain the dominant bottleneck.
- Anchors:
  - [855] Catch 1,000 Hunter creatures. — 80 LP — accessible — counted
  - [851] Catch 25 implings of any kind. — 30 LP — accessible — counted
  - [586] Catch 30 crystal skillchompas in Isafdar. — 200 LP — locked — counted

#### Hunter special / BGH

- Scope: **9** unfinished / **3** accessible now; **1,300 LP** total / **310 LP** accessible.
- Shapes: atomic 9.
- Primary: Animal Wrangler
- Supporting: —
- Edge-only: —
- Edge case: 5x loot helps loot-mark objectives, but rare-spawn availability can remain the dominant bottleneck.
- Anchors:
  - [1191] Take down a giant dashing kebbit in big game hunter. — 200 LP — accessible — atomic
  - [1192] Use a clockwork box trap to catch a grenwall in a kebbit encounter. — 30 LP — accessible — atomic
  - [527] Complete a big game encounter with 3 creatures active. — 400 LP — locked — atomic

#### Mining atomic

- Scope: **2** unfinished / **2** accessible now; **40 LP** total / **40 LP** accessible.
- Shapes: atomic 2.
- Primary: —
- Supporting: Survivalist, Endless Harvest
- Edge-only: —
- Note: Usually only one successful gather is required, so compatibility can be mechanically real but numerically tiny.
- Anchors:
  - [887] Mine some ore with a rune pickaxe. — 30 LP — accessible — atomic
  - [288] Mine a gem rock at the Al Kharid mine. — 10 LP — accessible — atomic

#### Mining quantity

- Scope: **14** unfinished / **7** accessible now; **1,720 LP** total / **730 LP** accessible.
- Shapes: counted 14.
- Primary: Survivalist
- Supporting: Endless Harvest
- Edge-only: —
- Note: Transmutation is already baseline and reduces the value of raw tier-specific ore acquisition.
- Edge case: Survivalist bonus resources count toward quantity tasks; do not transfer that rule to action-count wording.
- Anchors:
  - [1037] Mine 70 banite ore. — 200 LP — accessible — counted
  - [1197] Mine 20 havensilver ore. — 10 LP — accessible — counted
  - [479] Mine 25 platinum ore south of Piscatoris Fishing Colony. — 200 LP — locked — counted

#### Woodcutting atomic

- Scope: **3** unfinished / **1** accessible now; **480 LP** total / **80 LP** accessible.
- Shapes: atomic 3.
- Primary: —
- Supporting: Survivalist, Endless Harvest
- Edge-only: Superheated, Antiquarian
- Edge case: Resource-count and action-count wording must be separated; Always Adze/Superheated mainly add Firemaking value rather than faster Woodcutting completion.
- Anchors:
  - [20] Chop down the Edgeville elder tree. — 80 LP — accessible — atomic
  - [470] Chop an elder tree until it no longer has logs remaining in Kandarin. — 200 LP — locked — atomic

#### Woodcutting quantity / action

- Scope: **7** unfinished / **2** accessible now; **800 LP** total / **90 LP** accessible.
- Shapes: counted 6, atomic 1.
- Primary: —
- Supporting: Survivalist, Endless Harvest
- Edge-only: Superheated, Antiquarian
- Edge case: Resource-count and action-count wording must be separated; Always Adze/Superheated mainly add Firemaking value rather than faster Woodcutting completion.
- Anchors:
  - [167] Chop any tree 1000 times. — 80 LP — accessible — counted
  - [1181] Cut creeping ivy 20 times. — 10 LP — accessible — atomic
  - [480] Chop 50 eternal magic logs. — 200 LP — locked — counted

### Magic systems

#### Necromancy rituals

- Scope: **4** unfinished / **2** accessible now; **510 LP** total / **110 LP** accessible.
- Shapes: atomic 4.
- Primary: Crystal Grace
- Supporting: Perkfection
- Edge-only: —
- Anchors:
  - [85] Conjure an undead army at the City of Um ritual site. — 80 LP — accessible — atomic
  - [74] Conjure a phantom guardian at the City of Um ritual site. — 30 LP — accessible — atomic
  - [416] Perform a Powerful Necroplasm ritual at the Ungael ritual site. — 200 LP — locked — atomic

#### Prayer

- Scope: **9** unfinished / **4** accessible now; **380 LP** total / **150 LP** accessible.
- Shapes: atomic 8, counted 1.
- Primary: —
- Supporting: Crystal Grace
- Edge-only: Antiquarian
- Note: Crystal Grace matters when the task burden is Prayer XP from bones; simply activating/using a prayer is effectively relic-neutral.
- Anchors:
  - [277] Bury some frost dragon bones. — 80 LP — accessible — atomic
  - [230] Pray to Bandos's remains. — 10 LP — accessible — atomic
  - [465] Use the Piety Prayer. — 80 LP — locked — atomic

#### Rune production

- Scope: **7** unfinished / **3** accessible now; **600 LP** total / **310 LP** accessible.
- Shapes: atomic 2, counted 4, access 1.
- Primary: Crystal Grace
- Supporting: —
- Edge-only: —
- Edge case: Triple rune output is not automatically triple Runecrafting XP.
- Anchors:
  - [349] Craft some soul runes. — 200 LP — accessible — atomic
  - [906] Craft some combination runes. — 30 LP — accessible — atomic
  - [529] Craft 500 time runes. — 200 LP — locked — counted

#### Runespan

- Scope: **7** unfinished / **7** accessible now; **630 LP** total / **630 LP** accessible.
- Shapes: atomic 7.
- Primary: —
- Supporting: —
- Edge-only: —
- Usually neutral: Crystal Grace
- Note: Rune-output multipliers do not accelerate Runespan siphoning objectives.
- Anchors:
  - [11] Navigate the Runespan using a greater conjuration platform. — 200 LP — accessible — atomic
  - [4] Siphon from a fire essling in the Runespan. — 10 LP — accessible — atomic

#### Spell access / casting

- Scope: **9** unfinished / **2** accessible now; **1,150 LP** total / **400 LP** accessible.
- Shapes: atomic 8, access 1.
- Primary: —
- Supporting: —
- Edge-only: Crystal Grace
- Edge case: Some spells remain individually quest-gated despite broad spell unlock wording.
- Anchors:
  - [353] Cast Ice Barrage in the desert. — 200 LP — accessible — atomic
  - [406] Cast Spellbook Swap from the Lunar spellbook. — 200 LP — locked — atomic

### Other skills

#### Agility

- Scope: **17** unfinished / **7** accessible now; **710 LP** total / **300 LP** accessible.
- Shapes: atomic 10, counted 6, threshold 1.
- Primary: —
- Supporting: —
- Edge-only: —
- Usually neutral: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- Note: League movement cooldown passive makes Shadow's Grace largely redundant; Goldenhawk boots are already baseline.
- Anchors:
  - [638] Collect 10 Agility Arena tickets from the Brimhaven Agility Arena. — 80 LP — accessible — threshold
  - [223] Complete a lap of the Burthorpe Agility course. — 10 LP — accessible — atomic
  - [496] Complete the Anachronia agility course in under 7 minutes. — 80 LP — locked — atomic

#### Divination

- Scope: **4** unfinished / **0** accessible now; **320 LP** total / **0 LP** accessible.
- Shapes: atomic 2, composite 2.
- Primary: —
- Supporting: —
- Edge-only: Antiquarian
- Note: Divine Druid enriched springs are already baseline.
- Anchors:
  - [467] Help the Archivist recover all core memory data in the Hall of Memories. — 200 LP — locked — composite

#### Dungeoneering

- Scope: **1** unfinished / **0** accessible now; **10 LP** total / **0 LP** accessible.
- Shapes: atomic 1.
- Primary: —
- Supporting: —
- Edge-only: Perkfection, Antiquarian
- Note: Mostly indirect combat help; T5 token multiplier is already baseline.
- Anchors:
  - [663] Complete a frozen floor in Daemonheim. — 10 LP — locked — atomic

#### Summoning

- Scope: **6** unfinished / **3** accessible now; **340 LP** total / **30 LP** accessible.
- Shapes: atomic 5, access 1.
- Primary: —
- Supporting: —
- Edge-only: —
- Usually neutral: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- Note: Divine Druid/Devout already provide the major Summoning advantages.
- Anchors:
  - [291] Create a spirit kalphite pouch at the obelisk south west of Pollnivneach. — 10 LP — accessible — atomic
  - [418] Summon a pack mammoth. — 200 LP — locked — atomic

#### Thieving

- Scope: **8** unfinished / **2** accessible now; **970 LP** total / **230 LP** accessible.
- Shapes: atomic 7, rng 1.
- Primary: —
- Supporting: —
- Edge-only: —
- Usually neutral: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- Note: Golden Touch already supplies the dominant Thieving automation/success benefits; Antiquarian Thieving relic powers largely overlap.
- Anchors:
  - [1216] Pick all pockets, open all chests and crack all safes in the Vault of Hereditas Heist before searching the rare chest. — 200 LP — accessible — rng
  - [238] Use the Telekinetic Grab spell to steal some wine of Zamorak from the captured temple south of Goblin Village. — 30 LP — accessible — atomic
  - [580] Have 4 elven clans suspect you of thieving at the same time. — 200 LP — locked — atomic

### Production

#### Construction materials

- Scope: **1** unfinished / **1** accessible now; **10 LP** total / **10 LP** accessible.
- Shapes: atomic 1.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Note: Material batching matters more than the single Fort plank task itself.
- Anchors:
  - [105] Make a plank yourself on the sawmill in Fort Forinthry. — 10 LP — accessible — atomic

#### Cooking atomic

- Scope: **11** unfinished / **8** accessible now; **440 LP** total / **390 LP** accessible.
- Shapes: atomic 11.
- Primary: —
- Supporting: Production Master
- Edge-only: Superheated, Antiquarian
- Note: Most are one action or short ingredient chains; evaluate individually.
- Anchors:
  - [132] Bake a summer pie in the Cooking Guild from scratch. — 200 LP — accessible — atomic
  - [838] Make some bread. — 10 LP — accessible — atomic
  - [449] Create the listed gnome cocktails. — 30 LP — locked — atomic

#### Cooking bulk

- Scope: **1** unfinished / **1** accessible now; **80 LP** total / **80 LP** accessible.
- Shapes: counted 1.
- Primary: Production Master
- Supporting: Superheated, Antiquarian
- Edge-only: —
- Note: Superheated/Bait and Switch matter when the fish can be caught and cooked in the same route.
- Anchors:
  - [837] Cook 1,000 fish. — 80 LP — accessible — counted

#### Crafting atomic

- Scope: **3** unfinished / **1** accessible now; **290 LP** total / **80 LP** accessible.
- Shapes: access 1, atomic 2.
- Primary: —
- Supporting: Production Master
- Edge-only: —
- Edge case: Only score recipes actually on PM's supported activity list; one-off recipes have limited compression.
- Anchors:
  - [636] Craft a bolas. — 80 LP — accessible — atomic
  - [583] Craft an attuned crystal teleport seed. — 200 LP — locked — access

#### Firemaking

- Scope: **8** unfinished / **6** accessible now; **710 LP** total / **620 LP** accessible.
- Shapes: counted 7, atomic 1.
- Primary: Superheated
- Supporting: Antiquarian
- Edge-only: Endless Harvest, Survivalist
- Note: Antiquarian uses Always Adze when Firemaking is paired with Woodcutting.
- Anchors:
  - [1058] Burn 100 magic logs — 200 LP — accessible — counted
  - [174] Burn any logs 200 times. — 30 LP — accessible — counted
  - [763] Burn 20 blisterwood logs. — 80 LP — locked — counted

#### Fletching atomic

- Scope: **5** unfinished / **3** accessible now; **760 LP** total / **360 LP** accessible.
- Shapes: atomic 5.
- Primary: —
- Supporting: Production Master
- Edge-only: —
- Note: One-action recipes receive little time compression; +6 boost/access can matter more than batching.
- Anchors:
  - [1031] Fletch an eternal magic wood box. — 200 LP — accessible — atomic
  - [960] Fletch some broad arrows or bolts. — 80 LP — accessible — atomic
  - [533] Fletch any type of Elder God arrow. — 200 LP — locked — atomic

#### Fletching bulk

- Scope: **14** unfinished / **11** accessible now; **1,670 LP** total / **1,240 LP** accessible.
- Shapes: counted 14.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Anchors:
  - [1025] Fletch 200 magic stocks. — 200 LP — accessible — counted
  - [822] Fletch 50 bronze bolts. — 10 LP — accessible — counted
  - [1029] Fletch 1,000 eternal magic shafts. — 200 LP — locked — counted

#### Herblore atomic

- Scope: **7** unfinished / **3** accessible now; **750 LP** total / **70 LP** accessible.
- Shapes: atomic 7.
- Primary: —
- Supporting: Production Master
- Edge-only: —
- Note: Usually a one-off recipe, so batching may save essentially nothing beyond access/portable effects.
- Anchors:
  - [877] Make a 4-dose potion. — 30 LP — accessible — atomic
  - [363] Create a Guthix rest potion. — 10 LP — accessible — atomic
  - [1024] Make a spiritual prayer potion. — 200 LP — locked — atomic

#### Herblore bulk

- Scope: **7** unfinished / **4** accessible now; **820 LP** total / **220 LP** accessible.
- Shapes: counted 7.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Edge case: Divine Druid already batch-cleans matching herbs and saves secondaries; clean-herb tasks get little incremental PM value.
- Anchors:
  - [809] Make 1,000 potions of any kind. — 80 LP — accessible — counted
  - [876] Make 30 prayer potions. — 30 LP — accessible — counted
  - [1009] Make 25 powerburst potions. — 200 LP — locked — counted

#### Normal Smithing atomic

- Scope: **5** unfinished / **4** accessible now; **350 LP** total / **270 LP** accessible.
- Shapes: atomic 5.
- Primary: Superheated
- Supporting: Survivalist, Endless Harvest
- Edge-only: —
- Edge case: Production Master does not accelerate ordinary Smithing.
- Anchors:
  - [1033] Smith a primal ore box. — 200 LP — accessible — atomic
  - [1198] Smith a havensilver weapon. — 10 LP — accessible — atomic
  - [404] Smith a piece of bane equipment to +4 in Rellekka. — 80 LP — locked — atomic

#### Normal Smithing bulk

- Scope: **3** unfinished / **3** accessible now; **480 LP** total / **480 LP** accessible.
- Shapes: counted 3.
- Primary: Superheated
- Supporting: Survivalist, Endless Harvest
- Edge-only: —
- Edge case: Production Master does not accelerate ordinary Smithing.
- Anchors:
  - [1034] Smith 10,000 armour spikes. — 200 LP — accessible — counted
  - [830] Smith 100 of any metal weapon or armour piece. — 80 LP — accessible — counted

#### Smelting

- Scope: **2** unfinished / **0** accessible now; **400 LP** total / **0 LP** accessible.
- Shapes: counted 2.
- Primary: Superheated
- Supporting: Survivalist, Endless Harvest
- Edge-only: —
- Anchors:
  - [578] Aid Lady Trahaearn in removing some corruption by smelting 100 corrupted ore. — 200 LP — locked — counted

### Progression

#### Archaeology progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Antiquarian
- Supporting: Endless Harvest, Survivalist
- Edge-only: —
- Anchors:
  - [1061] Reach level 99 in the Archaeology skill. — 200 LP — accessible — threshold

#### Attack progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: —
- Supporting: Perkfection
- Edge-only: Assassin's Insight, Antiquarian
- Anchors:
  - [1062] Reach level 99 in the Attack skill. — 200 LP — accessible — threshold

#### Combat-level milestone

- Scope: **1** unfinished / **1** accessible now; **200 LP** total / **200 LP** accessible.
- Shapes: threshold 1.
- Primary: —
- Supporting: Perkfection, Assassin's Insight, Antiquarian
- Edge-only: —
- **Must decompose individually before numeric scoring.**
- Anchors:
  - [146] Reach maximum combat level. — 200 LP — accessible — threshold

#### Constitution progression

- Scope: **1** unfinished / **1** accessible now; **200 LP** total / **200 LP** accessible.
- Shapes: threshold 1.
- Primary: —
- Supporting: Perkfection
- Edge-only: Assassin's Insight, Antiquarian
- Anchors:
  - [1125] Obtain 50 million Constitution XP. — 200 LP — accessible — threshold

#### Construction progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Anchors:
  - [1063] Reach level 99 in the Construction skill. — 200 LP — accessible — threshold

#### Cooking progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: Production Master
- Supporting: —
- Edge-only: Superheated, Antiquarian
- Anchors:
  - [1064] Reach level 99 in the Cooking skill. — 200 LP — accessible — threshold

#### Crafting progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Anchors:
  - [1065] Reach level 99 in the Crafting skill. — 200 LP — accessible — threshold

#### Cross-skill milestones

- Scope: **9** unfinished / **9** accessible now; **1,550 LP** total / **1,550 LP** accessible.
- Shapes: threshold 9.
- Primary: —
- Supporting: —
- Edge-only: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Production Master, Perkfection
- **Must decompose individually before numeric scoring.**
- Note: Evaluate only the skills still below each threshold. Current low skills make these highly account-state dependent.
- Anchors:
  - [152] Reach maximum total level. — 400 LP — accessible — threshold
  - [1153] Reach at least level 30 in all non-elite skills. — 30 LP — accessible — threshold

#### Defence progression

- Scope: **1** unfinished / **1** accessible now; **200 LP** total / **200 LP** accessible.
- Shapes: threshold 1.
- Primary: —
- Supporting: Perkfection
- Edge-only: Assassin's Insight, Antiquarian
- Anchors:
  - [1127] Obtain 50 million Defence XP. — 200 LP — accessible — threshold

#### Divination progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: —
- Supporting: —
- Edge-only: Antiquarian
- Anchors:
  - [1067] Reach level 99 in the Divination skill. — 200 LP — accessible — threshold

#### Dungeoneering progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: —
- Supporting: —
- Edge-only: Perkfection, Antiquarian
- Anchors:
  - [1068] Reach level 99 in the Dungeoneering skill. — 200 LP — accessible — threshold

#### Farming progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Nature's Network
- Supporting: —
- Edge-only: —
- Anchors:
  - [1069] Reach level 99 in the Farming skill. — 200 LP — accessible — threshold

#### Firemaking progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Superheated
- Supporting: Antiquarian
- Edge-only: Endless Harvest, Survivalist
- Anchors:
  - [1070] Reach level 99 in the Firemaking skill. (Where arson is its own reward.) — 200 LP — accessible — threshold

#### Fishing progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: Animal Wrangler
- Supporting: Endless Harvest, Survivalist
- Edge-only: Superheated, Antiquarian
- Anchors:
  - [1071] Reach level 99 in the Fishing skill. — 200 LP — accessible — threshold

#### Fletching progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Anchors:
  - [1072] Reach level 99 in the Fletching skill. — 200 LP — accessible — threshold

#### Flexible 200m XP

- Scope: **1** unfinished / **1** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 1.
- Primary: —
- Supporting: —
- Edge-only: Production Master, Superheated, Nature's Network, Animal Wrangler, Antiquarian, Endless Harvest, Survivalist, Assassin's Insight, Crystal Grace, Perkfection
- **Must decompose individually before numeric scoring.**
- Note: Choose the fastest candidate-assisted skill; do not average across skills.
- Anchors:
  - [1143] Obtain 200 million XP in any single skill. — 400 LP — accessible — threshold

#### Herblore progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Production Master
- Supporting: —
- Edge-only: —
- Note: Divine Druid is already baseline and materially overlaps resource/cleaning efficiency.
- Anchors:
  - [1073] Reach level 99 in the Herblore skill. — 200 LP — accessible — threshold

#### Hunter progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: Animal Wrangler
- Supporting: —
- Edge-only: —
- Anchors:
  - [1075] Reach level 99 in the Hunter skill. — 200 LP — accessible — threshold

#### Magic progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: —
- Supporting: Perkfection
- Edge-only: Assassin's Insight, Antiquarian
- Anchors:
  - [1077] Reach level 99 in the Magic skill. — 200 LP — accessible — threshold

#### Mining progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Survivalist
- Supporting: Endless Harvest
- Edge-only: —
- Anchors:
  - [1078] Reach level 99 in the Mining skill. — 200 LP — accessible — threshold

#### Necromancy progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: Crystal Grace
- Supporting: Perkfection
- Edge-only: Antiquarian
- Anchors:
  - [1102] Reach level 120 in the Necromancy skill. — 200 LP — accessible — threshold

#### Prayer progression

- Scope: **1** unfinished / **1** accessible now; **200 LP** total / **200 LP** accessible.
- Shapes: threshold 1.
- Primary: Crystal Grace
- Supporting: —
- Edge-only: Antiquarian
- Anchors:
  - [1114] Obtain 50 million Prayer XP. — 200 LP — accessible — threshold

#### Ranged progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: —
- Supporting: Perkfection
- Edge-only: Assassin's Insight, Antiquarian
- Anchors:
  - [1081] Reach level 99 in the Ranged skill. — 200 LP — accessible — threshold

#### Runecrafting progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: —
- Supporting: —
- Edge-only: Crystal Grace
- Edge case: Crystal Grace raises rune output, not proven XP per essence; do not give blanket XP multiplier.
- Anchors:
  - [1082] Reach level 99 in the Runecrafting skill. — 200 LP — accessible — threshold

#### Slayer progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Assassin's Insight
- Supporting: Perkfection, Antiquarian
- Edge-only: —
- Anchors:
  - [1083] Reach level 99 in the Slayer skill. — 200 LP — accessible — threshold

#### Smithing progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Superheated
- Supporting: Survivalist, Endless Harvest
- Edge-only: —
- Anchors:
  - [1084] Reach level 99 in the Smithing skill. — 200 LP — accessible — threshold

#### Strength progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: —
- Supporting: Perkfection
- Edge-only: Assassin's Insight, Antiquarian
- Anchors:
  - [1085] Reach level 99 in the Strength skill. — 200 LP — accessible — threshold

#### Summoning progression

- Scope: **2** unfinished / **2** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: threshold 2.
- Primary: —
- Supporting: —
- Edge-only: —
- Anchors:
  - [1086] Reach level 99 in the Summoning skill. — 200 LP — accessible — threshold

#### Woodcutting progression

- Scope: **3** unfinished / **3** accessible now; **600 LP** total / **600 LP** accessible.
- Shapes: threshold 3.
- Primary: Survivalist
- Supporting: Endless Harvest
- Edge-only: Antiquarian, Superheated
- Anchors:
  - [1088] Reach level 99 in the Woodcutting skill. — 200 LP — accessible — threshold

### Projects & construction

#### Build / upgrade / repair

- Scope: **12** unfinished / **10** accessible now; **1,160 LP** total / **730 LP** accessible.
- Shapes: access 1, atomic 10, composite 1.
- Primary: —
- Supporting: Production Master
- Edge-only: —
- **Must decompose individually before numeric scoring.**
- Note: Score material-production and Construction-level gates separately from fixed build/repair interactions.
- Anchors:
  - [25] Upgrade the guardhouse in Fort Forinthry to Tier 3. — 200 LP — accessible — atomic
  - [22] Use the bank in the workshop at Fort Forinthry. — 10 LP — accessible — access
  - [525] Fully upgrade the Town Hall in the base camp on Anachronia. — 400 LP — locked — composite

### Relic-neutral / bespoke

#### Bespoke one-off

- Scope: **54** unfinished / **24** accessible now; **4,490 LP** total / **1,130 LP** accessible.
- Shapes: composite 3, atomic 45, threshold 3, counted 3.
- Primary: —
- Supporting: —
- Edge-only: —
- Usually neutral: Endless Harvest, Survivalist, Animal Wrangler, Superheated, Nature's Network, Assassin's Insight, Crystal Grace, Antiquarian, Clue Connoisseur, Production Master, Perkfection
- Note: No general relic relationship. Keep as singular tasks and only reopen if a hidden prerequisite becomes a route bottleneck.
- Anchors:
  - [355] Craft a Zaros godsword, Seren godbow or staff of Sliske. — 200 LP — accessible — atomic
  - [100] Have Elsie tell you a story. — 10 LP — accessible — atomic
  - [478] Throw 100,000,000 gold coins into the Whirlpool at the Deep Sea Fishing platform. — 400 LP — locked — counted

### Slayer

#### Assignment / special

- Scope: **2** unfinished / **1** accessible now; **210 LP** total / **10 LP** accessible.
- Shapes: atomic 2.
- Primary: Assassin's Insight
- Supporting: Perkfection, Antiquarian
- Edge-only: —
- Edge case: Assassin combat bonus only applies to confirmed assignment-compatible targets; use whitelist, not blanket boss credit.
- Anchors:
  - [599] Be assigned a Slayer task in Shilo Village. — 10 LP — accessible — atomic
  - [699] Complete a slayer task from Mandrith. — 200 LP — locked — atomic

#### Assignment-count milestones

- Scope: **4** unfinished / **4** accessible now; **490 LP** total / **490 LP** accessible.
- Shapes: atomic 1, counted 3.
- Primary: Assassin's Insight
- Supporting: Perkfection, Antiquarian
- Edge-only: —
- Edge case: Assassin combat bonus only applies to confirmed assignment-compatible targets; use whitelist, not blanket boss credit.
- Anchors:
  - [858] Complete 50 Slayer tasks. — 200 LP — accessible — counted
  - [856] Complete 5 Slayer tasks. — 10 LP — accessible — atomic

#### Slayer collection / drops

- Scope: **1** unfinished / **1** accessible now; **400 LP** total / **400 LP** accessible.
- Shapes: atomic 1.
- Primary: Assassin's Insight
- Supporting: Perkfection, Antiquarian
- Edge-only: —
- Edge case: Assassin combat bonus only applies to confirmed assignment-compatible targets; use whitelist, not blanket boss credit.
- Anchors:
  - [1018] Obtained a collection of unique drops from Slayer monsters located within Asgarnia & Misthalin. — 400 LP — accessible — atomic

## Global edge-case rules before percentages

- **Quantity vs action counters:** bonus resources/fish can shorten quantity tasks, but never assume they shorten wording such as “catch/chop N times.”
- **Masterwork:** Production Master compresses special Masterwork processing. Superheated helps upstream ore/bar/ordinary Smithing only.
- **Normal Smithing:** Production Master gets no normal-Smithing speed credit; Superheated is the direct accelerator.
- **Runecrafting:** Crystal Grace rune-output multiplication is not an XP multiplier. Runespan objectives are separate.
- **Clues:** Clue Connoisseur's extra casket does not count as another clue completion.
- **Assassin's Insight:** use confirmed Slayer-eligible targets only; no blanket boss compatibility.
- **Perkfection:** broad combat compatibility is not broad +20% DPS. Numeric scoring must sensitivity-test realistic incremental combat savings.
- **Nature's Network planting counter:** seed-as-ten counter behavior remains unverified; numeric counter bonus stays zero until tested.
- **Antiquarian:** treat as a configurable three-power secondary system and select the best loadout per task/group rather than assigning it a fixed Archaeology-only identity.
- **Composite tasks:** area task sets, mastery bundles, cross-skill milestones, gear acquisition chains, and RNG collections are wrappers; score their remaining components, not their title.

## Next analysis stage

For each subgroup, choose representative anchor tasks, decompose their remaining burden into components, and assign relic compatibility percentages only after the component weights are understood. Propagate percentages to sibling tasks only where wording and mechanics are equivalent.
