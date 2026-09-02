#!/usr/bin/env python3
import collections, datetime as dt, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent

def load(path,default):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except Exception:return default

def dump(path,obj):
    path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')

def norm(o):
    return {'id':int(o['id']),'name':str(o.get('name','')).strip(),'description':str(o.get('description','')).strip(),'tier':str(o.get('tier','')).lower(),'region':str(o.get('region','')).strip(),'points':int(o.get('points',0)),'blessing_task':bool(o.get('blessingTask',o.get('blessing_task',False))),'issue':o.get('issue') or None}

def parse_catalog(path):
    raw=path.read_text(encoding='utf-8'); chunks=[]
    rx=re.compile(r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)',re.S)
    for m in rx.finditer(raw):
        try:chunks.append(json.loads(m.group(1)))
        except Exception:pass
    decoded='\n'.join(chunks); dec=json.JSONDecoder(); pos=0; found={}
    while True:
        pos=decoded.find('{"id":"',pos)
        if pos<0:break
        try:o,end=dec.raw_decode(decoded[pos:])
        except Exception:pos+=1;continue
        pos+=max(end,1)
        if isinstance(o,dict) and {'id','name','tier','region','points'}<=set(o):
            try:t=norm(o);found[t['id']]=t
            except Exception:pass
    return sorted(found.values(),key=lambda x:x['id'])

def catalog(now):
    cached=load(ROOT/'task-catalog.json',{}); old=[norm(x) for x in cached.get('tasks',[]) if isinstance(x,dict) and 'id' in x]
    tasks=old; status='cached'; fetched=cached.get('fetched_at_utc')
    html=REPO/'task-catalog.html'
    if html.exists():
        try:
            fresh=parse_catalog(html)
            if len(fresh)>=1100:
                tasks=fresh
                if fresh==old:status='fresh_unchanged'
                else:status='fresh_updated';fetched=now
        except Exception:pass
    if len(tasks)<1100:raise RuntimeError('No valid Equilibrium task catalog available')
    dump(ROOT/'task-catalog.json',{'schema_version':2,'source':'ScapeLeagues Equilibrium task database','source_url':'https://scapeleagues.com/rs3/equilibrium/tasks','fetched_at_utc':fetched,'task_count':len(tasks),'tasks':tasks})
    return tasks,status,fetched

def relic_tier(rules,lp):
    n=0
    for k,v in sorted(rules['relics']['tiers'].items(),key=lambda x:int(x[0])):
        if lp>=int(v['points']):n=int(k)
    return n

def next_relic(rules,lp):
    for k,v in sorted(rules['relics']['tiers'].items(),key=lambda x:int(x[0])):
        p=int(v['points'])
        if lp<p:return {'tier':int(k),'threshold':p,'remaining_points':p-lp}

def next_region(rules,count):
    arr=[{'id':'karamja','tasks':int(x['tasks']),'region':x.get('region')} for x in rules['regions'].get('automatic',[])]
    arr += [{'id':x['id'],'tasks':int(x['tasks']),'region':None} for x in rules['regions'].get('elective_thresholds',[])]
    for x in sorted(arr,key=lambda x:x['tasks']):
        if count<x['tasks']:return {**x,'remaining_tasks':x['tasks']-count}

def blessing_progress(rules,count):
    order=['t1','t2','t3','god1','t4','t5','t6','god2']; cur=None; nxt=None
    for k in order:
        n=int(rules['blessings']['steps'][k]['tasks'])
        if count>=n:cur=k
        elif nxt is None:nxt={'step':k,'threshold':n,'remaining_tasks':n-count}
    return cur,nxt

def god_choice(vals):
    vals=[int(x) for x in vals if x in (1,2,3)]
    if len(vals)!=3:return None
    c=collections.Counter(vals)
    for p,n in c.items():
        if n>=2:return p
    return 2

def resolve_relics(rules,state,tier):
    vec=state.get('relic_choice_vector',[]); selected=[]; passive=[]
    for n in range(1,8):
        t=rules['relics']['tiers'][str(n)]; choice=vec[n-1] if len(vec)>=n else None; opt=t.get('options',{}).get(str(choice)) if choice is not None else None
        selected.append({'tier':n,'unlocked':n<=tier,'choice_number':choice,'name':opt.get('name') if opt else None,'effects':opt.get('effects',[]) if opt else [],'threshold_points':int(t['points']),'xp_multiplier':int(t['xp_multiplier'])})
        if n<=tier:passive.append({'tier':n,'effects':t.get('passive_effects',[])})
    return selected,passive

def resolve_blessings(rules,state,count):
    vec=state.get('blessing_path_vector',{}); gods={'god1':god_choice([vec.get('t1'),vec.get('t2'),vec.get('t3')]),'god2':god_choice([vec.get('t4'),vec.get('t5'),vec.get('t6')])}
    out=[]; passive=[]
    for k in ['t1','t2','t3','god1','t4','t5','t6','god2']:
        s=rules['blessings']['steps'][k]; unlocked=count>=int(s['tasks']); choice=gods.get(k) if k.startswith('god') else vec.get(k); opt=s.get('options',{}).get(str(choice)) if choice is not None else None
        out.append({'step':k,'unlocked':unlocked,'threshold_tasks':int(s['tasks']),'choice_number':choice,'path':rules['blessings']['path_encoding'].get(str(choice)) if choice else None,'name':opt.get('name') if opt else None,'effects':opt.get('effects',[]) if opt else [],'derived':k.startswith('god')})
        if unlocked:passive.append({'step':k,'effects':s.get('passive_effects',[])})
    unique=len(set(x for x in vec.values() if x in (1,2,3))); dynamic=[]
    t4=next((x for x in out if x['step']=='t4'),None)
    if t4 and t4['unlocked'] and t4['name']=='True Equilibrium':
        dynamic=[{'source':'True Equilibrium','unique_paths_currently_chosen':unique,'current_bonus':{'base_ability_damage':75*unique,'armour':50*unique,'life_points':500*unique,'critical_strike_chance_percent':5*unique,'critical_strike_damage_percent':7.5*unique,'prayer_bonus':5*unique}}]
    return out,passive,gods,dynamic

def evaluate(t,ov,levels,regions,exclusions,flags):
    r=dict(t); tid=t['id']; r.update({'estimated_seconds':None,'cluster':None,'tags':[],'items_to_prepare':[],'blockers':[],'unknown_checks':[]})
    if tid in exclusions:r.update(status='excluded',exclusion_reason=exclusions[tid]);return r
    if t.get('issue'):r.update(status='known_issue',blockers=[{'type':'issue','detail':t['issue']}]);return r
    if t.get('region')!='Global' and t.get('region') not in regions:r.update(status='locked_region',blockers=[{'type':'region','required':t.get('region')}]);return r
    ov=ov or {}; blockers=[]; unknown=[]
    if ov.get('region') and ov['region']!='Global' and ov['region'] not in regions:blockers.append({'type':'region','required':ov['region']})
    for s,n in (ov.get('skills') or {}).items():
        cur=int(levels.get(s,0))
        if cur<int(n):blockers.append({'type':'skill','skill':s,'required':int(n),'current':cur})
    for f in ov.get('manual_requirements',[]) or []:
        v=flags.get(f)
        if v is False:blockers.append({'type':'manual_flag','flag':f,'required':True,'current':False})
        elif v is not True:unknown.append({'type':'manual_flag','flag':f,'current':v})
    r.update(estimated_seconds=ov.get('estimated_seconds'),cluster=ov.get('cluster'),tags=ov.get('tags',[]),items_to_prepare=ov.get('items',[]),blockers=blockers,unknown_checks=unknown)
    r['status']='blocked' if blockers else ('manual_check' if unknown else ('skill_region_ready' if ov else 'region_accessible_requirements_unknown'))
    return r

def context(a):
    A=a['account']; P=a['progression']; lines=[f"# Equilibrium assistant state — {A['player']}",'',f"Updated: **{A['timestamp_utc']}**",'',"## Tracker discipline",'',"- `assistant-state.json` is the canonical assistant briefing.","- `task-catalog.json` is the master 1,152-task database.","- `player-state.json` contains only manual facts and choices.","- `live-wikisync.json` is authoritative for completed task IDs and skill levels.","- HiScores is optional and can never block task/skill refreshes.","- Milestones come only from `league-rules.json`; do not copy generated totals into manual state.",'',"## Current snapshot",'',f"- **{A['league_points']:,} LP** · **{A['completed_tasks']} tasks** · total level **{A['total_level']:,}**",f"- **{A['blessing_tasks_completed']} blessing tasks** · relic **T{P['relic_tier']}**",f"- Regions: **{', '.join(a['regions']['unlocked'])}**"]
    if P.get('next_region'):lines.append(f"- Next region: **{P['next_region']['remaining_tasks']} tasks** to {P['next_region']['tasks']}")
    if P.get('next_relic'):lines.append(f"- Next relic: **{P['next_relic']['remaining_points']:,} LP** to T{P['next_relic']['tier']}")
    if P.get('next_blessing'):lines.append(f"- Next blessing step: **{P['next_blessing']['remaining_tasks']}** to {P['next_blessing']['step']}")
    lines += ['',"## Active relics",'',"Choice vector: `"+' '.join('-' if x is None else str(x) for x in a['relics']['choice_vector'])+'`','']
    for x in a['relics']['resolved']:
        if not x['unlocked']:continue
        lines.append(f"### T{x['tier']} — {x['name'] or 'choice not recorded'}")
        lines += ['- '+e for e in x['effects']]
        p=next((p for p in a['relics']['passive_by_tier'] if p['tier']==x['tier']),None)
        if p:lines.append('Passive tier effects:');lines += ['- '+e for e in p['effects']]
        lines.append('')
    lines += ["## Active blessings",'',"Path encoding: `1=Order, 2=Balance, 3=Chaos`",'']
    for x in a['blessings']['resolved']:
        if not x['unlocked']:continue
        lines.append(f"### {x['step']} — {x['name'] or 'choice not recorded'}"+(' (derived)' if x['derived'] else ''))
        lines += ['- '+e for e in x['effects']]
        p=next((p for p in a['blessings']['passive_by_step'] if p['step']==x['step']),None)
        if p:lines.append('Passive step effects:');lines += ['- '+e for e in p['effects']]
        lines.append('')
    for d in a['blessings']['dynamic_effects']:lines += ["### Dynamic blessing effect",'',f"- **{d['source']}** currently has **{d['unique_paths_currently_chosen']} stacks**: `{d['current_bonus']}`",'']
    c=a['changes']; lines += ["## Changes",'',f"- Tasks: **{c['task_delta']:+d}** · LP: **{c['league_points_delta']:+d}**"]
    if c['new_tasks']:lines += [f"- [{t['id']}] {t['name']} — {t['tier']}, {t['region']}, {t['points']} LP" for t in c['new_tasks']]
    if c['level_ups']:lines.append('- Level-ups: '+'; '.join(f"{x['skill']} {x['from']}→{x['to']}" for x in c['level_ups']))
    lines += ['',"## Fast task routing",'',f"- Enriched skill/region-ready: **{a['tasks']['skill_region_ready_count']}**",f"- Manual-check: **{a['tasks']['manual_check_count']}**",f"- Accessible but requirements not yet mapped: **{a['tasks']['requirements_unknown_count']}**",'']
    for t in a['tasks']['fastest_enriched'][:25]:lines.append(f"- [{t['id']}] **{t['name']}** — ~{t.get('estimated_seconds','?')}s · {t.get('cluster') or 'unclustered'}"+((' · prep: '+', '.join(t['items_to_prepare'])) if t.get('items_to_prepare') else ''))
    lines += ['',"## Data health",'',f"- WikiSync: **{a['health']['wikisync']['status']}** · {a['health']['wikisync']['timestamp']}",f"- Task catalog: **{a['health']['task_catalog']['status']}** · {a['health']['task_catalog']['task_count']} tasks",f"- HiScores: **{a['health']['hiscores']['status']}** (optional)",'',"> Always apply the active League effects above before normal RS3 mechanics."]
    return '\n'.join(lines)+'\n'

def main():
    now=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(); rules=load(ROOT/'league-rules.json',{}); state=load(ROOT/'player-state.json',{}); ovs=load(ROOT/'task-overrides.json',{}).get('tasks',{}); w=load(ROOT/'live-wikisync.json',{})
    if not isinstance(w.get('league_tasks'),list) or not isinstance(w.get('levels'),dict):raise RuntimeError('WikiSync missing league_tasks or levels')
    tasks,cat_status,cat_time=catalog(now); byid={t['id']:t for t in tasks}; ids=sorted(set(int(x) for x in w['league_tasks'])); done=set(ids); levels={k:int(v) for k,v in w['levels'].items()}; completed=[byid[x] for x in ids if x in byid]; missing=[x for x in ids if x not in byid]; lp=sum(t['points'] for t in completed); bless=sum(1 for t in completed if t['blessing_task']); total=sum(levels.values())
    reg=state.get('regions',{}); unlocked=[]
    for k in ('starting','automatic','elective'):
        for r in reg.get(k,[]) or []:
            if r not in unlocked:unlocked.append(r)
    regions=set(unlocked)|{'Global'}; exclusions={int(k):v for k,v in state.get('task_exclusions',{}).items()}; flags=state.get('manual_flags',{})
    unfinished=[evaluate(t,ovs.get(str(t['id'])),levels,regions,exclusions,flags) for t in tasks if t['id'] not in done]; counts=collections.Counter(t['status'] for t in unfinished); ready=sorted([t for t in unfinished if t['status']=='skill_region_ready' and t.get('estimated_seconds') is not None],key=lambda t:(t['estimated_seconds'],-t['points'],t['id'])); manual=sorted([t for t in unfinished if t['status']=='manual_check' and t.get('estimated_seconds') is not None],key=lambda t:(t['estimated_seconds'],t['id'])); clusters=collections.defaultdict(list)
    for t in ready+manual:
        if t.get('cluster'):clusters[t['cluster']].append({'id':t['id'],'name':t['name'],'status':t['status'],'estimated_seconds':t['estimated_seconds'],'points':t['points']})
    old=load(ROOT/'live-summary.json',{}); oldids=set(int(x) for x in old.get('completed_task_ids',[]) or []); newids=sorted(done-oldids); oldlevels={k:int(v) for k,v in old.get('levels',{}).items()}; levelups=[{'skill':s,'from':oldlevels.get(s,n),'to':n} for s,n in levels.items() if n>oldlevels.get(s,n)]; changes={'task_delta':len(ids)-len(oldids) if oldids else 0,'league_points_delta':lp-int(old.get('league_points',lp) or lp),'new_task_ids':newids,'new_tasks':[byid[x] for x in newids if x in byid],'level_ups':levelups}
    rt=relic_tier(rules,lp); rr,rp=resolve_relics(rules,state,rt); bc,bn=blessing_progress(rules,bless); br,bp,gods,dyn=resolve_blessings(rules,state,bless); hs=(ROOT/'live-hiscores.html').exists() and (ROOT/'live-hiscores.html').stat().st_size>0; health={'generated_at_utc':w.get('timestamp') or now,'wikisync':{'status':'fresh' if w.get('timestamp') else 'present_no_timestamp','timestamp':w.get('timestamp'),'authoritative_for':['completed_task_ids','skill_levels']},'task_catalog':{'status':cat_status,'fetched_at_utc':cat_time,'task_count':len(tasks),'mapped_completed_tasks':len(completed),'unmapped_completed_task_ids':missing},'hiscores':{'status':'fetched_optional' if hs else 'unavailable_optional','required':False,'note':'HiScores parsing is not a dependency.'}}
    A={'schema_version':1,'account':{'timestamp_utc':w.get('timestamp') or now,'player':state.get('player') or w.get('username'),'league':state.get('league'),'league_points':lp,'league_points_source':'sum of mapped completed task points','completed_tasks':len(ids),'completed_task_ids':ids,'total_level':total,'levels':levels,'blessing_tasks_completed':bless},'progression':{'relic_tier':rt,'next_relic':next_relic(rules,lp),'next_region':next_region(rules,len(ids)),'current_blessing_step':bc,'next_blessing':bn},'regions':{'unlocked':unlocked,**reg},'relics':{'choice_vector':state.get('relic_choice_vector',[]),'resolved':rr,'passive_by_tier':rp},'blessings':{'path_encoding':rules['blessings']['path_encoding'],'path_vector':state.get('blessing_path_vector',{}),'derived_god_choices':gods,'resets_remaining':state.get('blessing_resets_remaining'),'resolved':br,'passive_by_step':bp,'dynamic_effects':dyn},'manual':{'goal':state.get('goal'),'key_items':state.get('key_items',[]),'route_preferences':state.get('route_preferences',{}),'task_exclusions':state.get('task_exclusions',{}),'manual_flags':flags},'tasks':{'master_task_count':len(tasks),'unfinished_count':len(unfinished),'status_counts':dict(sorted(counts.items())),'skill_region_ready_count':counts.get('skill_region_ready',0),'manual_check_count':counts.get('manual_check',0),'requirements_unknown_count':counts.get('region_accessible_requirements_unknown',0),'fastest_enriched':ready[:50],'manual_check_fastest':manual[:25],'clusters':dict(sorted(clusters.items()))},'changes':changes,'health':health}
    summary={'timestamp_utc':A['account']['timestamp_utc'],'player':A['account']['player'],'source':'WikiSync + master Equilibrium task catalog; HiScores optional','league_points':lp,'league_points_source':'mapped completed-task point sum','completed_tasks':len(ids),'completed_task_ids':ids,'total_level':total,'levels':levels,'blessing_tasks_completed':bless,'relic_tier':rt,'next_relic':A['progression']['next_relic'],'next_region':A['progression']['next_region'],'next_blessing':A['progression']['next_blessing'],'new_task_ids_since_previous_live_sync':newids,'new_tasks_since_previous_live_sync':changes['new_tasks'],'task_delta_since_previous_live_sync':changes['task_delta'],'level_ups_since_previous_live_sync':levelups,'catalog_task_count':len(tasks),'mapped_completed_tasks':len(completed),'unmapped_completed_task_ids':missing,'confirmed_unlocked_regions':unlocked,'relic_choice_vector':state.get('relic_choice_vector',[]),'blessing_path_vector':state.get('blessing_path_vector',{}),'excluded_recommendation_task_ids':sorted(exclusions)}
    unfin={'schema_version':2,'timestamp_utc':A['account']['timestamp_utc'],'master_task_count':len(tasks),'completed_task_count':len(ids),'unfinished_task_count':len(unfinished),'unlocked_regions':unlocked,'status_counts':dict(sorted(counts.items())),'fastest_enriched_tasks':ready[:100],'manual_check_tasks':manual[:50],'clusters':dict(sorted(clusters.items())),'unfinished_tasks':unfinished}
    hist=load(ROOT/'live-history.json',[]); hist=hist if isinstance(hist,list) else []; snap={'timestamp_utc':A['account']['timestamp_utc'],'completed_tasks':len(ids),'league_points':lp,'total_level':total,'blessing_tasks_completed':bless}
    if not hist or any(hist[-1].get(k)!=snap[k] for k in ('completed_tasks','league_points','total_level','blessing_tasks_completed')):hist=(hist+[snap])[-200:]
    dump(ROOT/'assistant-state.json',A);dump(ROOT/'live-summary.json',summary);dump(ROOT/'live-unfinished.json',unfin);dump(ROOT/'changes.json',changes);dump(ROOT/'health.json',health);dump(ROOT/'live-history.json',hist);(ROOT/'assistant-context.md').write_text(context(A),encoding='utf-8')
    print(f"Equilibrium tracker: {len(ids)} tasks | {lp} LP | total {total} | {bless} blessings | T{rt} | catalog {cat_status}:{len(tasks)}")

if __name__=='__main__':main()
