
import os
from collections import defaultdict

import statsmodels.api as sm
import numpy as np
import scipy.stats as sp
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

class RtsAnalyzer(object):
    PRECISION = 4

    def __init__(self, output, rts, quant_limit):
        self.output = output
        self.rts = rts
        self.quant_limit = quant_limit

    @classmethod
    def sort(self, d1, d2):
        keys = sorted(list(set(list(d1.keys()) + list(d2.keys()))))
        x, y = list(), list()

        for idx, key in enumerate(keys):
            try:
                x_val = d1[key]
                y_val = d2[key]
            except KeyError:
                continue

            x.append(x_val)
            y.append(y_val)

        return (keys, x, y)

    def write_counts(self, ids, x, y, filename="comparison.csv"):
        csv = os.path.join(self.output, filename)
        with open(csv, "w") as handle:
            handle.write("RTS,DRAGEN,DNDv2\n")
            for id1, x1, y1 in zip(ids, x, y):
                handle.write("{},{},{}\n".format(id1,x1,y1))

    def write_summary(self, ols, filename="summary.txt"):
        summary = os.path.join(self.output, filename)
        with open(summary, "w") as handle:
            handle.write(str(ols.summary()))

    def plot(self, x, y, ols=None, filename="plot.png"):
        plt.scatter(x, y)
        plt.title("Barcoded UMI Analysis Method Comparison")
        plt.xlabel("DRAGEN Spatial Analysis UMI Count")
        plt.ylabel("DND v2 UMI Count")

        x_plot = np.linspace(0,1,100)
        if ols is not None:
            plt.plot(x_plot, x_plot*ols.params[0] + ols.params[1])
        
        output_file = os.path.join(self.output, filename)
        plt.savefig(output_file, bbox_inches="tight")
        #plt.show()

    def calculate_threshold(self, ids, counts):
        ctrls = [id for id in ids if self.rts.is_control(id)]
        counts = [max(1, counts[id]) for id in ctrls if id in counts]
        #print(len(ctrls), ctrls)
        #print(len(counts), counts)
        if len(counts) <= 1:
            return 0.0
        mean = sp.gmean(counts)
        std = sp.gstd(counts)
        #print(mean, std, mean * (std**2))
        threshold = mean * (std**2)
        if self.quant_limit is not None and self.quant_limit > 0.0:
            return max(threshold, self.quant_limit)
        return threshold

    def counts_by_gene(self, probes_by_gene, counts):
        probe_counts = defaultdict(float)
        probe_totals = defaultdict(int)

        for gene, ids in probes_by_gene.items():
            for id in ids:
                try:
                    count = counts[id]
                except KeyError:
                    continue

                if count is None or count == 0:
                    continue
                probe_counts[gene] += 1
                probe_totals[gene] += count

        avgs = dict()
        for gene, count in probe_counts.items():
            if count > 0:
                avgs[gene] = round(probe_totals[gene] / count, self.PRECISION)

        return avgs

    def genes_present(self, counts_by_gene, threshold):
        return [gene for gene, count in counts_by_gene.items() if count > threshold]

    def write_gene_analysis(self, thresh1, thresh2, genes1, genes2, filename="gene_results.txt"):
        results = os.path.join(self.output, filename)

        diff = abs(len(genes1) - len(genes2))
        shared = set(genes1).intersection(set(genes2))

        frac_diff = 100.0
        frac_shared = 0.0
        if min(len(genes1), len(genes2)) > 0:
            frac_diff = round(diff / float(max(len(genes1), len(genes2))), self.PRECISION)
            frac_shared = round(len(shared) / float(max(len(genes1), len(genes2))), self.PRECISION)

        with open(results, "w") as handle:
            handle.write("Metric,DRAGEN,DNDv2\n")
            handle.write("Threshold,{},{}\n".format(thresh1, thresh2))
            handle.write("Genes,{},{}\n".format(len(genes1), len(genes2)))
            handle.write("FractionGenesDiff,{}\n".format(frac_diff))
            handle.write("GenesShared,{}\n".format(len(shared)))
            handle.write("FractionGenesShared,{}\n".format(frac_shared))

    def run(self, d1, d2):
        # First we sort and write the raw results
        ids, x, y = self.sort(d1, d2)
        self.write_counts(ids,x, y)

        # Skip analysis if we don't have enough data for statistic significance
        if min(len(x), len(y)) < 8:
            return

        # Then we run our OLS regression on them
        ols = sm.OLS(y, sm.add_constant(x)).fit()
        self.write_summary(ols)

        # Finally we plot the results graphically
        self.plot(x, y, ols)

        if self.rts.has_controls():
            by_gene = self.rts.probes_by_gene()

            d1_avgs = self.counts_by_gene(by_gene, d1)
            d1_thresh = self.calculate_threshold(ids, d1)
            d1_genes = self.genes_present(d1_avgs, d1_thresh)

            d2_avgs = self.counts_by_gene(by_gene, d2)
            d2_thresh = self.calculate_threshold(ids, d2)
            d2_genes = self.genes_present(d2_avgs, d2_thresh)
            
            #print(len(by_gene), len(d1_avgs), d1_thresh, len(d1_genes))
            #print(len(by_gene), len(d2_avgs), d2_thresh, len(d2_genes))

            self.write_gene_analysis(d1_thresh, d2_thresh, d1_genes, d2_genes)
