import numpy as np
import math
import matplotlib.pyplot as plt
from textwrap import wrap

# set up figure
fig = plt.figure()
ax = plt.axes()
plt.xticks(fontsize=12)
ax.tick_params(axis='y', which='major', labelsize=12)
ax.xaxis.label.set_fontsize(12)
ax.yaxis.label.set_fontsize(12)
plt.xlabel('Mixture Parameter $\\beta$', fontsize=16)
plt.ylabel('Error (RMSE)', fontsize=16)
ax.set_ylim([0,0.1])

# set up parameter space
links = ["1","3","5"]
colours={}
colours['1']='red'
colours['3']='blue'
colours['5']='green'
linetype={}
linetype['1000']="--"
linetype['10000']='-'
params = np.linspace(0.0, 1.0, num=11)
noparams = len(params)
experiments = 10

for link in links:
    for size in ["1000", "10000"]:
        MLEtable = np.zeros((noparams,experiments),dtype=float)
        for i in range(noparams):
            param = round(params[i],1)
            file = "BARank"+size+"-"+link+"-results"+str(param)+".dat"
            with open(file,'r') as f:
                lines = f.read().splitlines()
                MLEtable[i,:] = [float(r.split()[1].strip()) for r in [lines[k] for k in range(len(lines)-10, len(lines))]]
                f.close()

        means = [sum(row)/experiments for row in MLEtable]
        sds = [math.sqrt(sum((MLEtable[i,:] - means[i])**2)/experiments) for i in range(noparams)]

        mse = [math.sqrt(sum((params[j] - MLEtable[j,:])**2)/experiments) for j in range(noparams)]
        kse = [max(abs(params[j]-MLEtable[j,:])) for j in range(noparams)]

        ax.plot(params,mse, marker='o', linestyle=linetype[size], label=link+" links, "+size+" nodes",linewidth=float(link),color=colours[link])

plt.tight_layout(h_pad=0)
plt.legend(loc='upper right')
plt.show()
fig.savefig("RPBACombined.pdf")
