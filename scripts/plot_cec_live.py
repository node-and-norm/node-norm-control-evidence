"""Reproduce descriptive figure and plotted table from the frozen report."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
r = json.loads((ROOT/'experiments/jev-cec/execution-v1/live-001/report.json').read_text())
out = ROOT/'docs/figures'
out.mkdir(exist_ok=True)
rows=[]
for p in ('1','2','3'):
    m=r['passes'][p]['overall']
    rows.append([int(p),m['matches'],m['valid_determinations']-m['matches'],m['scheduled_determinations']-m['valid_determinations']])
with (out/'cec-live-counts.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['pass','matches','mismatches','unavailable']);w.writerows(rows)
plt.rcParams.update({'font.size':11,'svg.hashsalt':'cec-live-001'})
fig,ax=plt.subplots(figsize=(10,4.8))
colors=['#52699c','#c58b37','#dddddd'];labels=['Matches authored reference','Disagrees with reference','Unavailable: invalid response']
for j,row in enumerate(rows):
    left=0
    for k,v in enumerate(row[1:]):
        ax.barh(j,v,left=left,color=colors[k],edgecolor='white',hatch='///' if k==2 else None,label=labels[k] if j==0 else None)
        if v: ax.text(left+v/2,j,str(v),ha='center',va='center',color='white' if k==0 else '#161616',weight='bold')
        left+=v
ax.set(yticks=range(3),yticklabels=['Pass 1 (primary)','Pass 2','Pass 3'],xlim=(0,36),xticks=range(0,37,6),xlabel='Scheduled determinations per pass (36)')
ax.invert_yaxis();ax.spines[['top','right']].set_visible(False)
ax.set_title('CEC Jev: agreement must be read alongside coverage',loc='left',pad=18,weight='bold')
ax.legend(loc='upper left',bbox_to_anchor=(0,-.22),frameon=False,ncol=1,fontsize=10)
fig.text(.02,.025,'12 public synthetic packets × 3 questions. Repeated passes are dependent.\nAgreement with an AI-authored reference; no independent accuracy estimate.',fontsize=10)
fig.subplots_adjust(left=.19,right=.97,top=.84,bottom=.37)
fig.savefig(out/'cec-live-overview.png',dpi=180)
fig.savefig(out/'cec-live-overview.svg',metadata={'Date':None})
