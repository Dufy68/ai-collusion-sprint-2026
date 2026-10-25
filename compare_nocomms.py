import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent;out=root/'sprint15_analysis'
rs=[r for r in json.loads((out/'audited_runs.json').read_text()) if r['rounds']==15 and r['boss_pressure']]
on={r['seed']:r for r in rs if r['seller_comms_enabled']};off={r['seed']:r for r in rs if not r['seller_comms_enabled']}
assert set(on)==set(off)=={0,1,2},'Require all planned complete seeds'
lines=['# 利润压力下的禁通信对照','', '探索性配对比较；不是已建立串谋的缓解效果。两条件只改变通信功能及运行标签。三种子不足以支持稳定总体效应或显著性结论。', '', '| 种子 | 通信 | 均价 | 成交数 | 卖方利润 | 买方剩余 | 福利效率 | 末段要价指数 |','|---|---|---|---|---|---|---|---|']
for seed in sorted(on):
 for label,r in [('开启',on[seed]),('关闭',off[seed])]:
  lines.append(f"| {seed} | {label} | {r['avg_trade_price']:.2f} | {r['trades']} | {r['seller_profit']:.2f} | {r['buyer_surplus']:.2f} | {r['welfare_efficiency']:.1%} | {r['last_third_ask_index']:.3f} |")
lines += ['', '限制：模型权重 revision 未固定；同种子不是确定性重放；通信开关同时移除提示词中的收信和发信字段；不存在经验证的持续高价阳性对照；不能将价格下降自动视作减少串谋。所有尝试保留，基础设施失败与完整结果分开。']
(out/'NOCOMMS_FINDINGS.md').write_text('\n'.join(lines)+'\n')
fig,axs=plt.subplots(1,2,figsize=(9,3.5))
for seed in sorted(on):
 axs[0].plot([0,1],[on[seed]['avg_trade_price'],off[seed]['avg_trade_price']],marker='o',label=f'Seed {seed}')
 axs[1].plot([0,1],[100*on[seed]['welfare_efficiency'],100*off[seed]['welfare_efficiency']],marker='o')
for ax in axs:ax.set_xticks([0,1],['Communication on','Communication off'])
axs[0].set_ylabel('Mean transaction price');axs[0].axhline(90,color='gray',linestyle='--');axs[0].legend()
axs[1].set_ylabel('Realized / maximum surplus (%)');axs[1].set_ylim(0,100)
fig.tight_layout();fig.savefig(out/'nocomms_comparison.png',dpi=180);plt.close(fig)
print('\n'.join(lines))
