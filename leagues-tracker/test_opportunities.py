#!/usr/bin/env python3
import json
from pathlib import Path

from opportunity_detector import all_skills_requirement, explicit_level_requirement, number_signature

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


# Family parsing should group numbered task ladders without grouping trivial text.
t1, n1 = number_signature("Search the Grand Gold Chest in room 1 of Pyramid Plunder in Sophanem.")
t2, n2 = number_signature("Search the Grand Gold Chest in room 2 of Pyramid Plunder in Sophanem.")
assert t1 == t2 and n1 == [1] and n2 == [2]
assert number_signature("Kill 10 rats")[0] is None

# Direct level tasks should parse, ordinary action tasks should not become level tasks.
assert explicit_level_requirement("Reach level 99 in the Necromancy skill.") == ("Necromancy", 99)
assert explicit_level_requirement("Open 10 metamorphic geodes.") is None
assert explicit_level_requirement("Equip a full set of graahk hunter gear.") is None

# All-skill ladders must use the actual lowest relevant skill, not prior milestone tasks.
all_req = all_skills_requirement(
    "Reach at least level 50 in all non-elite skills.",
    {"Attack": 70, "Farming": 22, "Invention": 5},
)
assert all_req["lowest_skill"] == "Farming"
assert all_req["lowest_level"] == 22
assert all_req["gap"] == 28

summary = load("live-summary.json")
opps = load("opportunities.json")
completed = {int(x) for x in summary.get("completed_task_ids", [])}

assert opps.get("schema_version") == 3
assert isinstance(opps.get("top"), list)
for task in opps["top"]:
    assert int(task["id"]) not in completed, f"Completed task leaked into opportunities: {task['id']}"
    assert task["reasons"], f"Opportunity has no evidence: {task['id']}"
    assert task["opportunity_score"] > 0
    assert 0 <= task["confidence"] <= 1

assistant = load("assistant-state.json")
assert "forgotten_finish_opportunities" in assistant
assert assistant["forgotten_finish_opportunities"]["count"] == opps["count"]

print(f"Opportunity detector OK: {opps['count']} suspects, {len(opps['top'])} surfaced")
