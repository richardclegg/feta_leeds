import numpy as np
import math
import matplotlib.pyplot as plt
from collections import defaultdict

# Set up figure

fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(6,7), sharex=True)

plt.xlabel('Iteration number corresponding to changepoint', fontsize=16)
plt.xticks(fontsize=12)
ax[0].tick_params(axis='y', which='major', labelsize=12)
ax[1].tick_params(axis='y', which='major', labelsize=12)
ax[0].set_ylabel('RMSE (# iterations)', fontsize=16)

ax[1].set_ylabel('Estimated changepoint time', fontsize=16)

linetype = defaultdict(lambda:'-')
# linetype["['1.2', '1.0']"]='--'
# linetype["['1.0', '1.2']"]= '--'
# linetype["['1.0', '0.8']"]= '--'
# linetype["['0.8', '1.0']"]= '--'
linetype["['1.0', '0.9']"]='--'
linetype["['0.9', '1.0']"]='--'

mtype = defaultdict(lambda:'o')
mtype["['1.2', '1.0']"]='^'
mtype["['1.0', '0.9']"]='s'
mtype["['1.0', '1.2']"]='D'

thicc = defaultdict(lambda: 1)
thicc["['1.2', '1.0']"]= 3
thicc["['1.0', '1.2']"]= 3
thicc["['1.0', '0.8']"]= 3
thicc["['0.8', '1.0']"]= 3
thicc["['0.9', '1.1']"]= 3
thicc["['1.1', '0.9']"]= 3

alphas = defaultdict(lambda: 0.5)
alphas["['1.2', '1.0']"]= 1
alphas["['1.0', '1.2']"]= 1
alphas["['1.0', '0.8']"]= 1
alphas["['0.8', '1.0']"]= 1

fillalphas=defaultdict(lambda: 0.3)
fillalphas["['1.2', '1.0']"]= 0.5
fillalphas["['1.0', '1.2']"]= 0.5

params = [['0.9','1.0'],['1.0','0.9'],['1.2','1.0'],['1.0','1.2']]
experiments=10

colourz = defaultdict(lambda: 'blue')
colourz["['1.0', '0.9']"]= '#ff7f0e'
colourz["['0.9', '1.0']"]= '#1f77b4'
colourz["['1.0', '1.2']"]= '#d62728'
colourz["['1.2', '1.0']"]= '#2ca02c'

truevals = range(100,1100,100)

for comb in params:

    MLEtable = np.zeros((10,experiments),dtype=float)

    for ex in range(experiments):
        file = "degreepower"+comb[0]+"-"+comb[1]+"-1000results"+str(ex)+".dat"
        lines=[]
        with open(file,'r') as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                lines.append(line)
        data = " ".join(lines).strip('[').strip(']')
        paramstring = data.split('][')
        params = [[float(r.strip()) for r in row.strip().split()] for row in paramstring]

        for i in range(10):
            MLEtable[i,ex]= (np.argmax(params[i])+1)*10

    means = np.array([sum(row)/experiments for row in MLEtable])
    sds = np.array([math.sqrt(sum((MLEtable[i,:] - means[i])**2)/experiments) for i in range(10)])
    mse = [math.sqrt(sum((truevals[j] - MLEtable[j,:])**2)/experiments) for j in range(10)]
    kse = [max(abs(truevals[j]-MLEtable[j,:])) for j in range(10)]
    symerror= np.array([sd/2.0 for sd in sds])
    if comb == ['1.0', '0.9'] or comb == ['1.2', '1.0']:
        ax[1].fill_between(truevals,means-symerror,means+symerror,alpha=fillalphas[str(comb)], color=colourz[str(comb)], label=comb[0]+" to "+comb[1])
        ax[1].plot(truevals,means, color=colourz[str(comb)])

    ax[0].plot(truevals,mse, marker=mtype[str(comb)], linestyle=linetype[str(comb)], linewidth=thicc[str(comb)], alpha=alphas[str(comb)], label=comb[0]+" to "+comb[1])

ax[1].plot(truevals,truevals, linestyle='--', color='black')
ax[1].legend(loc='upper left')
ax[0].legend(loc='upper left')
plt.tight_layout()
plt.show()

fig.savefig("DP1000_diff_markers.pdf")
