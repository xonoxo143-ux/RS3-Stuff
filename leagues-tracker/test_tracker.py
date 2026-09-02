#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("tracker", ROOT / "tracker.py")
tracker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tracker)

from task_intelligence import infer_task, merge_metadata

rules = json.loads((ROOT / "league-rules.json").read_text())
state = json.loads((ROOT / "player-state.json").read_text())

# Canonical progression rules: never reintroduce the old 175/300/450 values.
assert [x["tasks"] for x in rules["regions"]["elective_thresholds"]] == [150, 275, 400]
assert tracker.next_region(rules, 260)["tasks"] == 275
assert tracker.next_region(rules, 260)["remaining_tasks"] == 15
assert tracker.relic_tier(rules, 9120) == 5
assert tracker.next_relic(rules, 9120)["tier"] == 6
assert tracker.next_relic(rules, 9120)["remaining_points"] == 2880

# Compact relic encoding resolves to the actual active set.
assert state["relic_choice_vector"][:5] == [2, 3, 3, 2, 3]
resolved, _ = tracker.resolve_relics(rules, state, 5)
assert [x["name"] for x in resolved[:5]] == [
    "Golden Touch",
    "Divine Druid",
    "Voidwalker",
    "Transmutation",
    "Devout",
]

# Blessing paths and derived God tier.
blessings, _, gods, dynamic = tracker.resolve_blessings(rules, state, 12)
chosen = {x["step"]: x["name"] for x in blessings if x["unlocked"]}
assert chosen["t1"] == "Adrenaline Junkie"
assert chosen["t2"] == "Abyssal Cinders"
assert chosen["t3"] == "Eternal Sustenance"
assert chosen["god1"] == "Demon's Mark"
assert chosen["t4"] == "True Equilibrium"
assert gods["god1"] == 3
assert dynamic and dynamic[0]["unique_paths_currently_chosen"] == 2

# Future blessing-vector slots must not inflate True Equilibrium before unlock.
future_state = json.loads(json.dumps(state))
future_state["blessing_path_vector"]["t5"] = 1
future_state["blessing_path_vector"]["t6"] = 1
_, _, _, future_dynamic = tracker.resolve_blessings(rules, future_state, 12)
assert future_dynamic[0]["unique_paths_currently_chosen"] == 2

# Inference stays conservative: one-click wording can be suggested, complex wording cannot.
quick = infer_task(
    {
        "id": 1,
        "name": "Enter the Cooks' Guild.",
        "description": "Enter the Cooks' Guild in Varrock.",
    }
)
assert quick["estimated_seconds"] == 30
assert quick["cluster"] == "varrock"
assert quick["source"] == "text_inference"

complex_task = infer_task(
    {
        "id": 2,
        "name": "Complete a hard clue scroll.",
        "description": "Complete a hard clue scroll.",
    }
)
assert complex_task["estimated_seconds"] is None

# Manual metadata always overrides inference and becomes Grade A.
merged = merge_metadata(
    {"id": 3, "name": "Use a bank.", "description": "Use a bank in Lumbridge."},
    {
        "estimated_seconds": 10,
        "cluster": "bank",
        "skills": {"Cooking": 1},
        "tags": ["verified"],
    },
)
assert merged["source"] == "manual_override"
assert merged["confidence"] == 1.0
assert merged["estimated_seconds"] == 10
assert merged["cluster"] == "bank"

# Evaluator correctly separates verified, inferred, blocked, unknown-manual, and excluded tasks.
levels = {"Cooking": 67, "Mining": 77}
regions = {"Global", "Misthalin", "Desert"}
flags = {"fort_workshop_unlocked": None}

verified = tracker.evaluate(
    {"id": 10, "name": "Use a bank.", "description": "", "tier": "easy", "region": "Global", "points": 10, "blessing_task": False, "issue": None},
    {"estimated_seconds": 10, "cluster": "bank"},
    levels,
    regions,
    {},
    flags,
)
assert verified["status"] == "verified_ready"
assert verified["recommendation_grade"] == "A"

inferred = tracker.evaluate(
    {"id": 11, "name": "Enter Varrock.", "description": "", "tier": "easy", "region": "Misthalin", "points": 10, "blessing_task": False, "issue": None},
    None,
    levels,
    regions,
    {},
    flags,
)
assert inferred["status"] == "inferred_candidate"
assert inferred["recommendation_grade"] == "B"

blocked = tracker.evaluate(
    {"id": 12, "name": "Mine a rock.", "description": "", "tier": "easy", "region": "Desert", "points": 10, "blessing_task": False, "issue": None},
    {"estimated_seconds": 30, "skills": {"Mining": 80}},
    levels,
    regions,
    {},
    flags,
)
assert blocked["status"] == "blocked"
assert blocked["blockers"][0]["gap"] == 3

manual = tracker.evaluate(
    {"id": 13, "name": "Use the Fort bank.", "description": "", "tier": "easy", "region": "Misthalin", "points": 10, "blessing_task": False, "issue": None},
    {"estimated_seconds": 10, "manual_requirements": ["fort_workshop_unlocked"]},
    levels,
    regions,
    {},
    flags,
)
assert manual["status"] == "manual_check"

excluded = tracker.evaluate(
    {"id": 95, "name": "Croesus.", "description": "", "tier": "hard", "region": "Global", "points": 80, "blessing_task": False, "issue": None},
    None,
    levels,
    regions,
    {95: "excluded"},
    flags,
)
assert excluded["status"] == "excluded"

# State-validator fixtures must not depend on the user's current live region choices.
one_slot_state = json.loads(json.dumps(state))
one_slot_state["regions"]["elective"] = ["Desert"]
health = tracker.validate_state(rules, one_slot_state, 260, 5, 12, [])
assert health["status"] == "healthy"
assert health["expected_elective_slots"] == 1
assert health["recorded_elective_regions"] == 1

two_slot_state = json.loads(json.dumps(state))
two_slot_state["regions"]["elective"] = ["Desert", "Asgarnia"]
health = tracker.validate_state(rules, two_slot_state, 275, 5, 12, [])
assert health["status"] == "healthy"
assert health["expected_elective_slots"] == 2
assert health["recorded_elective_regions"] == 2

print("tracker tests passed")
