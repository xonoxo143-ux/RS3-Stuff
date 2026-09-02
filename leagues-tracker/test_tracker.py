#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tracker',ROOT/'tracker.py')
tracker=importlib.util.module_from_spec(spec);spec.loader.exec_module(tracker)
rules=json.loads((ROOT/'league-rules.json').read_text())
state=json.loads((ROOT/'player-state.json').read_text())
assert [x['tasks'] for x in rules['regions']['elective_thresholds']]==[150,275,400]
assert state['relic_choice_vector'][:5]==[2,3,3,2,3]
resolved,_=tracker.resolve_relics(rules,state,5)
assert [x['name'] for x in resolved[:5]]==['Golden Touch','Divine Druid','Voidwalker','Transmutation','Devout']
blessings,_,gods,dynamic=tracker.resolve_blessings(rules,state,12)
chosen={x['step']:x['name'] for x in blessings if x['unlocked']}
assert chosen['t1']=='Adrenaline Junkie'
assert chosen['t2']=='Abyssal Cinders'
assert chosen['t3']=='Eternal Sustenance'
assert chosen['god1']=="Demon's Mark"
assert chosen['t4']=='True Equilibrium'
assert gods['god1']==3
assert dynamic and dynamic[0]['unique_paths_currently_chosen']==2
assert tracker.relic_tier(rules,8870)==5
assert tracker.next_region(rules,253)['tasks']==275
assert tracker.next_region(rules,253)['remaining_tasks']==22
print('tracker tests passed')
