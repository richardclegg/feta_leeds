import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import matplotlib as mpl

file = "Enron10IntervalBARandTri.txt"

tA = 997747200
tB = 1024099200
times = [int(np.round(t)) for t in np.linspace(tA, tB, 11)]
midpoints = [(times[i] + times[i+1])/2 for i in range(10)]
stamps = [dt.datetime.fromtimestamp(int(l)) for l in midpoints]

BA = []
Rand = []
Tri = []

with open(file,'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        # Ignore the lines starting with "Processing events as links..."
        if "Processing" in line:
            continue
        if "Max" in line:
            continue
        parts = line.split()
        if "Degree" in parts[1]:
            BA.append(float(parts[0]))
            continue
        if "Random" in parts[1]:
            Rand.append(float(parts[0]))
            continue
        if "Triangle" in parts[1]:
            Tri.append(float(parts[0]))

BA=np.array(BA)
Rand=np.array(Rand)
Tri=np.array(Tri)

fig, ax = plt.subplots()

x_major_lct = mpl.dates.AutoDateLocator(minticks=2,maxticks=10, interval_multiples=True)
x_fmt = mpl.dates.AutoDateFormatter(x_major_lct)

ax.fill_between(stamps,0.001,BA,color='blue', alpha=0.7, label='BA')
ax.fill_between(stamps,BA,BA + Tri,color='green', alpha=0.7, label='Triangle Closure')
ax.fill_between(stamps,BA+Tri,BA+Rand+Tri, color='red', alpha=0.7, label='Random')

ax.tick_params(axis='x', which='major', labelsize=12)
ax.tick_params(axis='y', which='major', labelsize=12)

ax.xaxis.label.set_fontsize(16)
ax.yaxis.label.set_fontsize(16)

ax.set_xlabel("Time")
ax.set_ylabel("Model proportion in best mix")

#plt.legend(loc='lower right', fontsize='large')

plt.xticks(rotation=40)

plt.tight_layout()
plt.show()

fig.savefig("EnronMixtures.pdf", bbox_inches='tight')
