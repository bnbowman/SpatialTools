
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

def sort(d1, d2):
    keys = sorted(list(set(list(d1.keys()) + list(d2.keys()))))
    x, y = [0] * len(keys), [0] * len(keys)

    for idx, key in enumerate(keys):
        x_val = d1[key]
        y_val = d2[key]

        #if x_val > 1000 and y_val == 0:
        #    x_val = 0

        x[idx] = x_val
        y[idx] = y_val

    return (keys, x, y)

def plot(d1, d2):
    ids, x, y = sort(d1, d2)

    #for id1, x1, y1 in zip(ids, x, y):
    #    print("{},{},{}".format(id1,x1,y1))

    results = sm.OLS(y, sm.add_constant(x)).fit()

    print(results.summary())

    plt.scatter(x, y)
    plt.title("Barcoded UMI Analysis Method Comparison")
    plt.xlabel("DRAGEN Spatial Analysis UMI Count")
    plt.ylabel("DND v2 UMI Count")

    x_plot = np.linspace(0,1,100)
    plt.plot(x_plot, x_plot*results.params[0] + results.params[1])

    plt.show()
