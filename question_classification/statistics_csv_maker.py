#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import codecs
from collections import defaultdict
import os
import pickle
import scipy.stats
import numpy
from question_classification.config import classes


def determineWinner(net_evals, base_evals):
    t, p = scipy.stats.ttest_rel(net_evals, base_evals)
    if p/2 < confidence_level:
        if t > 0:
            return 'NN'
        return 'B'
    else:
        return '-'

res_files = [ os.path.join("results", f) for f in os.listdir("results")
              if f.endswith(".obj")]



confidence_level = 0.05

net_res = {} #fold -> list of tuple (res, iterNo)
base_res = {}

all_res = {"net": net_res, "base": base_res}

for res in res_files:
    splat = os.path.basename(res).split(".")
    alg = splat[1]
    fold = int(splat[0])
    iter_no = int(splat[2])
    with open(res, "r") as res_file:
        eval_obj = pickle.load(res_file)
        res_map = all_res[alg]
        if fold not in res_map:
            res_map[fold] = []
        res_map[fold].append((eval_obj, iter_no))



def create_csv(out_file, get_values, first_line=None):
    with codecs.open(out_file, "w", "utf8") as csv_file:
        if not first_line is None:
            csv_file.write(str(first_line)+"\n")
        csv_file.write(u"Rozmiar zbioru treningowego;F-miara sieci;Odchylenie;F-miara bazy;Odchylenie;Statystycznie lepszy\n")
        winners = defaultdict(lambda : 0)
        for fold in net_res.keys():
            csv_file.write("{:.2}%".format((fold-1.0)/fold).replace(".", ",")+";")

            net_evals=get_values(net_res, fold)
            num_net_evals = numpy.array(net_evals)
            net_mean = numpy.mean(num_net_evals)
            net_stddev = numpy.std(num_net_evals)
            csv_file.write("{:.4}".format(net_mean).replace(".", ",") + ";" + "{:.4}".format(net_stddev).replace(".", ",") + ";")

            base_evals = get_values(base_res, fold)
            num_base_evals = numpy.array(base_evals)
            base_mean = numpy.mean(num_base_evals)
            base_stddev = numpy.std(num_base_evals)
            csv_file.write("{:.4}".format(base_mean).replace(".", ",") + ";" + "{:.4}".format(base_stddev).replace(".", ",") + ";")
            winner = determineWinner(net_evals, base_evals)
            winners[winner] += 1
            csv_file.write(winner + "\n")
        csv_file.write("\n")
        csv_file.write(u"Liczba „zwycięstw” sieci;"+str(winners["NN"])+"\n")
        csv_file.write(u"Liczba „zwycięstw” bazy;"+str(winners["B"])+"\n")
        csv_file.write(u"Liczba porównań nieokreślonych;"+str(winners["-"])+"\n")

def create_total_csv(out_file):
    create_csv(out_file, lambda x, fold: [tup[0].getWeightedFMeasure() for tup in sorted(x[fold], key=lambda tup: tup[1])])

def create_class_csv(clazz, out_file):
    def get_values(x, fold):
        out = []
        for tup in sorted(x[fold], key=lambda tup: tup[1]):
            for class_result in tup[0].evals:
                if class_result.clazz==clazz:
                    out.append(class_result.getFMeasure())
        return out
    create_csv(out_file, get_values, clazz)

if __name__=="__main__":
    pass
    out_file = "results_stat.csv"
    create_total_csv(out_file)
    for clazz in classes:
        create_class_csv(clazz, clazz+".csv")