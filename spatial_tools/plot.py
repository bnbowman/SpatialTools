
#import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
    
matplotlib.use("Agg")

def sort(d1, d2):
    keys = sorted(list(set(list(d1.keys()) + list(d2.keys()))))
    x, y = [0] * len(keys), [0] * len(keys)

    for idx, key in enumerate(keys):
        x[idx] = d1[key]
        y[idx] = d2[key]

    return (keys, x, y)

def plot(output, d1, d2):
    ids, x, y = sort(d1, d2)

    comparison_csv = os.path.join(output, "comparison.csv")
    with open(comparison_csv, "w") as handle:
        handle.write("RTS,DRAGEN,DNDv2\n")
        for id1, x1, y1 in zip(ids, x, y):
            handle.write("{},{},{}\n".format(id1,x1,y1))

    results = sm.OLS(y, sm.add_constant(x)).fit()

    summary = os.path.join(output, "summary.txt")
    with open(summary, "w") as handle:
        handle.write(str(results.summary()))

    plt.scatter(x, y)
    plt.title("Barcoded UMI Analysis Method Comparison")
    plt.xlabel("DRAGEN Spatial Analysis UMI Count")
    plt.ylabel("DND v2 UMI Count")

    x_plot = np.linspace(0,1,100)
    plt.plot(x_plot, x_plot*results.params[0] + results.params[1])
    output_file = os.path.join(output, "plot.png")
    plt.savefig(output_file, bbox_inches="tight")
    plt.show()
