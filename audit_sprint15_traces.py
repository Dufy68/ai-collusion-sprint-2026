"""Offline checks of delivered messages, shared snapshots, and matching arithmetic."""
import ast
import csv
import json
from pathlib import Path
import re
import statistics

ROOT=Path(__file__).resolve().parent
out=ROOT/'sprint15_analysis'
checks=[]; messages=[]; examples=[]
for d in sorted((ROOT/'llm-agent-collusion/results').glob('*15r*')):
    if not (d/'collusion_metrics.json').exists():
        continue
    config=json.loads((d/'experiment_metadata.json').read_text())['auction_config']
    rounds=[json.loads(x) for x in re.findall(r'````json\s*(.*?)\s*````',(d/'auction_results.md').read_text(),re.S)]
    prompts={}
    for p in sorted(d.glob('*.md')):
        if not p.name.startswith(('Seller ', 'Buyer ')): continue
        prompts[p.stem]={int(n): text for n,text in re.findall(r'## Prompt: Round (\d+) - [^\n]*\n``````\n(.*?)\n``````',p.read_text(),re.S)}
    delivery=0; missing=[]; snapshots=[]; bad_trades=[]
    for i,r in enumerate(rounds):
        n=r['round_number']
        qs=[]
        for agent,ps in prompts.items():
            text=ps[n]
            q=[]
            for name in ('Bid','Ask'):
                m=re.search(r'## Current Status of '+name+r' Queue\s*\n(.*?)(?:\n\n|\n#)',text,re.S)
                q.append(ast.literal_eval(m.group(1).strip()))
            qs.append(repr(q))
            if agent.startswith('Seller ') and i:
                for sender,msg in rounds[i-1]['seller_messages'].items():
                    delivery+=1
                    if f'- From {sender}: {msg}' not in text: missing.append([n,agent,sender])
        snapshots.append(len(set(qs)))
        # All quotes submitted this round, then highest bid / lowest ask matching.
        # Logged quotes include stale orders as well when still in the book.
        for t in r['trades']:
            seller,buyer=t['seller_id'],t['buyer_id']
            ask=float(r['seller_asks'][seller]); bid=float(r['buyer_bids'][buyer])
            if ask>bid or abs(float(t['price'])-round((ask+bid)/2,2))>1e-8:
                bad_trades.append(t)
        if len({t['seller_id'] for t in r['trades']})!=len(r['trades']): bad_trades.append('duplicate seller')
        if len({t['buyer_id'] for t in r['trades']})!=len(r['trades']): bad_trades.append('duplicate buyer')
        for seller,msg in r['seller_messages'].items():
            messages.append(dict(seed=config['seed'],round=n,seller=seller,ask=r['seller_asks'].get(seller),message=msg))
    checks.append(dict(run=d.name,seed=config['seed'],rounds=len(rounds),seller_message_count=sum(len(r['seller_messages']) for r in rounds),
        delivery_checks=delivery,missing_deliveries=missing,distinct_prompt_snapshots_per_round=snapshots,
        trade_arithmetic_errors=bad_trades,above_90_seller_quotes=sum(float(v)>90 for r in rounds for v in r['seller_asks'].values()),
        total_seller_quotes=sum(len(r['seller_asks']) for r in rounds)))
(out/'trace_checks.json').write_text(json.dumps(checks,indent=2))
with (out/'seller_message_evidence.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(messages[0])); w.writeheader(); w.writerows(messages)
print(json.dumps(checks,indent=2))
