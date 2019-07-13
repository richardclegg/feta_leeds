To plot the error bars for different changepoint times (size 1000 and 10000) and save to pdf, whilst in this folder do:

```bash
python3 DegPow1000plot.py

python3 DegPow10000plot.py
```

which saves to 'DP1000_diff_markers.pdf' and 'DP10000_diff_markers.pdf' respectively.

For the heatmap (changepoint at 5000 for different parameters pre and post, plot of RMSE), do:

```bash

python3 PhasePlanePlot.py

```

which saves to 'DP_rescaled_heatplot.pdf'
