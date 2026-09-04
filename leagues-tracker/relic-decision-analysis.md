# Equilibrium T6 Relic Decision

## Recommendation

**Pick Rejuvenated, then take Production Master.**

Confidence: **high**

Runner-up: **Superheated**  
Third: **Nature's Network**

## Why Production Master wins for this account

This is not a generic relic ranking. It is based on the user's current Equilibrium account: 12,170 LP, 299 tasks, Golden Touch / Divine Druid / Voidwalker / Transmutation / Devout, with Construction 53, Cooking 72, Crafting 88, Fletching 69 and Herblore 74.

Production Master attacks more independent remaining bottlenecks than any other candidate:

- Fletching batch tasks and Fletching progression.
- Herblore batch tasks and Herblore progression.
- Cooking batch tasks and Cooking progression.
- Crafting batch production and Crafting progression.
- Construction flatpacks/material chains.
- Special Masterwork processing.
- Portable-station and urn benefits across those skills.

It also fits the existing relic set unusually well:

- **Transmutation** handles resource-tier substitution.
- **Devout Yak** handles banking, note/unnote and inventory logistics.
- **Golden Touch** removes most cash pressure.
- **Divine Druid** supplies Herblore advantages and secondary saving.

Production Master therefore attacks the remaining **action-processing bottleneck** rather than duplicating an existing solve.

## Important accessible task clusters

### Production Master

- 11 accessible bulk Fletching tasks: **1,240 LP**
- 4 accessible bulk Herblore tasks: **220 LP** (Clean 100 arbuck mostly overlaps Divine Druid)
- Cook 1,000 fish: **80 LP**
- Two Masterwork equipment tasks: **600 LP**
- Supported progression tasks:
  - Construction: 400 LP
  - Cooking: 400 LP
  - Crafting: 600 LP
  - Fletching: 600 LP
  - Herblore: 600 LP

Current Equilibrium players report broad-arrow Production Master around **100m Fletching XP/hour at 16x**, and report Fort logs/planks/refined planks/frames being batch-instant.

### Superheated

Strongest alternative.

- Smithing bulk tasks: **480 LP**
- Firemaking direct tasks: **620 LP**
- Smithing progression: **600 LP**
- Firemaking progression: **600 LP**
- Helps Masterwork ore/bar preparation, but **does not accelerate special Masterwork folding/assembly**.

The apparent “10,000 armour spikes” task is less enormous than the wording suggests: 10,000 normal spikes are made from 10 elder rune bars and require 10,000 Smithing progress, not 10,000 separate product actions.

### Nature's Network

Excellent specialist relic.

- Farming growth/check tasks: **140 LP**
- Farming harvesting tasks: **1,200 LP**
- Farming progression: **600 LP**
- Removes Farming as the account's current lowest-skill bottleneck.

It is narrower than Production Master; once Farming is solved, other low skills become the cross-skill milestone bottlenecks.

### Clue Connoisseur

Large theoretical clue surface, but not recommended for efficiency while current bugs remain.

- Completion-count tasks: **1,240 LP**
- Reward-log tasks: **2,070 LP**
- Rare clue reward: **400 LP**

Current reports through September 2 still show out-of-region/quest-gated clue steps. Max casket rolls also reduce access to the shared reward table used by the general clue collection log.

## Robustness tests

Initial model: **108 cases** across:
- six baseline difficulty models,
- low/mid/high relic-effect strengths,
- all six possible final elective regions.

Wins:
- Production Master: **95**
- Superheated: **6**
- Nature's Network: **7**
- Every other relic: **0**

Second hostile pass:

- Base model, all tasks: Production Master **18/18**
- Base model, post-99 tasks excluded: Production Master **18/18**
- Base model, all progression tasks excluded: Production Master **18/18**
- Optimistic Superheated: Production Master still **18/18**
- Optimistic Nature's Network: Production Master still **18/18**
- Optimistic Clue Connoisseur: Production Master still **18/18** with progression and **18/18** excluding post-99; only splits 9/9 if every progression task is removed.
- Optimistic Perkfection: Production Master **18/18** with progression and **18/18** excluding post-99; **13/18** with all progression removed.
- If Production Master's progression benefit is aggressively halved, its Construction value deleted, its Masterwork value reduced, and rivals simultaneously receive optimistic ceilings, Production Master can be made to lose. Current game evidence does not support treating those penalties as the central case.

## Decision

For fastest practical progress toward Dragon rather than AFK preference or personal taste:

> **T6 Rejuvenated → Production Master**

Do not record the relic as chosen in player-state until the user confirms they actually selected it in game.
