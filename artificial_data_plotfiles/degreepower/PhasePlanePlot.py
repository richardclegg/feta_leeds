import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.colors as colors
import pandas as pd

file = "PhasePlaneMLEs.txt"
noParams = 13

RMSEmatrix = np.zeros((noParams, noParams), dtype=float)
PEmatrix = np.zeros((noParams, noParams), dtype=float)

def getindex(param):
    index = int(round((param-0.8)*10))
    return index

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

with open(file,'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        parts = line.split()
        param1, param2 = float(parts[0]), float(parts[1])
        MLEs = 4500 + 10*np.array([float(x) for x in parts[2].split(',')])
        RMSE = np.sqrt(1.0/len(MLEs) * sum((MLEs - 5000)**2))
        RMSEmatrix[getindex(param1),getindex(param2)]=RMSE

RMSEmatrix = pd.DataFrame(RMSEmatrix, columns = [str(round(par,1)) for par in np.linspace(0.8, 2.0, num=13)])
PEmatrix = pd.DataFrame(PEmatrix, columns = [str(round(par,1)) for par in np.linspace(0.8, 2.0, num=13)])

plt.figure(figsize=(6,7))

ax = sns.heatmap(RMSEmatrix, cmap="YlGnBu", norm=MidpointNormalize(midpoint=20),
                 yticklabels=[str(round(par,1)) for par in np.linspace(0.8, 2.0, num=13)],
                 cbar_kws={'label': 'RMS error (number of iterations)',
                           'orientation': 'horizontal'})

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)
cbar.set_label('RMS error (number of iterations)', fontsize=16)
ax.set_ylabel('Degree power exponent \n pre-changepoint',fontsize=16, wrap=True)
ax.set_xlabel('Degree power exponent \n post-changepoint',fontsize=16, wrap=True)
#plt.title('Detection of changepoint time in degree power models')

plt.tight_layout()
plt.show
fig.savefig('DP_rescaled_heatplot.pdf')
