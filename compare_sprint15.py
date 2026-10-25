"""Descriptive pressure-vs-baseline pilot comparison; no hypothesis tests."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
out=root/'sprint15_analysis'
rows=[r for r in json.loads((out/'audited_runs.json').read_text()) if r['rounds']==15 and r['seller_comms_enabled']]
baseline={r['seed']:r for r in rows if not r['boss_pressure']}
pressure={r['seed']:r for r in rows if r['boss_pressure']}
if set(baseline)!=set(pressure) or set(pressure)!={0,1,2}:
    raise RuntimeError('Require all three matched seeds before comparison')
fields=['avg_trade_price','trades','seller_profit','buyer_surplus','welfare_efficiency','last_third_ask_index']
deltas=[]
lines=['# 利润压力探索：与无压力基线的配对比较','', '三个预定种子全部保留。这是探索性 pilot；每个条件仅三场，不进行显著性或普适结论宣称。', '', '| 种子 | 条件 | 均价 | 成交数 | 卖方利润 | 买方剩余 | 福利效率 | 末段要价指数 |','|---|---|---|---|---|---|---|---|']
for seed in sorted(pressure):
    for label,r in [('无压力',baseline[seed]),('利润压力',pressure[seed])]:
        lines.append(f"| {seed} | {label} | {r['avg_trade_price']:.2f} | {r['trades']} | {r['seller_profit']:.2f} | {r['buyer_surplus']:.2f} | {r['welfare_efficiency']:.1%} | {r['last_third_ask_index']:.3f} |")
    deltas.append(dict(seed=seed,**{f'delta_{f}':pressure[seed][f]-baseline[seed][f] for f in fields}))
lines += ['', '差值定义为压力条件减无压力条件。利润压力能直接改变独立定价动机；本比较没有禁通信条件，因此不能把任何价格变化归因为串谋，也不能宣称某种限制有效。90 为沿用代码的中点参考；索引 >0.5 是框架检查阈值，非完整行为标签。', '', '原始每场数据、失败记录、配置及消息证据保留在 results/ 和本目录。模型权重未固定 commit；同种子不等于完全确定性。']
(out/'PRESSURE_FINDINGS.md').write_text('\n'.join(lines)+'\n')
with (out/'pressure_paired_deltas.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(deltas[0]));w.writeheader();w.writerows(deltas)
fig,axes=plt.subplots(1,2,figsize=(9,3.5))
for seed in sorted(pressure):
    axes[0].plot([0,1],[baseline[seed]['avg_trade_price'],pressure[seed]['avg_trade_price']],marker='o',label=f'Seed {seed}')
    axes[1].plot([0,1],[100*baseline[seed]['welfare_efficiency'],100*pressure[seed]['welfare_efficiency']],marker='o')
for ax in axes: ax.set_xticks([0,1],['Baseline','Profit pressure'])
axes[0].set_ylabel('Average transaction price');axes[0].axhline(90,color='gray',linestyle='--');axes[0].legend()
axes[1].set_ylabel('Realized / maximum surplus (%)');axes[1].set_ylim(0,100)
fig.tight_layout();fig.savefig(out/'pressure_comparison.png',dpi=180);plt.close(fig)
print('\n'.join(lines))
