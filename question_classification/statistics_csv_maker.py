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


def mean_and_stddev(data):
    numpy_data = numpy.array(data)
    mean = numpy.mean(numpy_data)
    stddev = numpy.std(numpy_data)
    return (mean, stddev)

def create_F_csv(out_file, get_values, first_line=None):
    with codecs.open(out_file, "w", "utf8") as csv_file:
        if not first_line is None:
            csv_file.write(str(first_line)+"\n")
        csv_file.write(u"Rozmiar zbioru treningowego;F-miara sieci;Odchylenie;F-miara bazy;Odchylenie;Statystycznie lepszy\n")
        winners = defaultdict(lambda : 0)
        for fold in net_res.keys():
            csv_file.write("{:.2%}%".format(100*(fold-1.0)/fold).replace(".", ",")+";")

            net_evals=get_values(net_res, fold)
            net_mean, net_stddev = mean_and_stddev(net_evals)
            csv_file.write("{:.4}".format(net_mean).replace(".", ",") + ";" + "{:.4}".format(net_stddev).replace(".", ",") + ";")

            base_evals = get_values(base_res, fold)
            base_mean, base_stddev = mean_and_stddev(base_evals)
            csv_file.write("{:.4}".format(base_mean).replace(".", ",") + ";" + "{:.4}".format(base_stddev).replace(".", ",") + ";")
            winner = determineWinner(net_evals, base_evals)
            winners[winner] += 1
            csv_file.write(winner + "\n")
        csv_file.write("\n")
        csv_file.write(u"Liczba „zwycięstw” sieci;"+str(winners["NN"])+"\n")
        csv_file.write(u"Liczba „zwycięstw” bazy;"+str(winners["B"])+"\n")
        csv_file.write(u"Liczba porównań nieokreślonych;"+str(winners["-"])+"\n")

def create_total_F_csv(out_file):
    create_F_csv(out_file, lambda x, fold: [tup[0].getWeightedFMeasure() for tup in sorted(x[fold], key=lambda tup: tup[1])])

def get_class_values_factory(clazz):
    def get_values(classifier_results, fold):
        out = []
        for tup in sorted(classifier_results[fold], key=lambda tup: tup[1]):
            for class_result in tup[0].evals:
                if class_result.clazz==clazz:
                    out.append(class_result.getFMeasure())
        return out
    return get_values()

def create_class_F_csv(clazz, out_file):
    create_F_csv(out_file, get_class_values_factory(clazz), clazz)

def create_class_summary_for_fold(out_file, fold):
    net_per_class = defaultdict(lambda : {"a": [], "p": [], "r": [], "f": []})  # {class -> {a/p/r/f -> list(float)}}; a - accuracy, etc
    base_per_class = defaultdict(lambda : {"a": [], "p": [], "r": [], "f": []})  # {class -> {a/p/r/f -> list(float)}}; a - accuracy, etc
    def save_result(result, target):
        target[result.clazz]["a"] += [ result.getAccuracy() ]
        target[result.clazz]["p"] += [ result.getPrecision() ]
        target[result.clazz]["r"] += [ result.getRecall() ]
        target[result.clazz]["f"] += [ result.getFMeasure() ]
        target["total"]["a"] += [ result.getAccuracy() ]
        target["total"]["p"] += [ result.getPrecision() ]
        target["total"]["r"] += [ result.getRecall() ]
        target["total"]["f"] += [ result.getFMeasure() ]
    def do_gather(eval_tuples, target):
        for eval, i in eval_tuples:
            for result in eval.evals:
                save_result(result, target)
    do_gather(net_res[fold], net_per_class)
    do_gather(base_res[fold], base_per_class)
    with codecs.open(out_file, "w", "utf8") as csv:
        csv.write(";".join(["Class", "Classifier", "Accuracy", "", "Precision", "", "Recall", "", "F", ""]))
        csv.write("\n")
        csv.write(";".join(["", "", "Mean", "StdDev", "Mean", "StdDev", "Mean", "StdDev", "Mean", "StdDev"]))
        csv.write("\n")
        for clazz in classes+["total"]:
            row = (clazz, u"NN") +\
                  mean_and_stddev(net_per_class[clazz]["a"]) + \
                  mean_and_stddev(net_per_class[clazz]["p"]) + \
                  mean_and_stddev(net_per_class[clazz]["r"]) + \
                  mean_and_stddev(net_per_class[clazz]["f"])
            csv.write("{};{};{:.4};{:.4};{:.4};{:.4};{:.4};{:.4};{:.4};{:.4}".format(*row).replace(".", ","))
            csv.write("\n")
            row = ("B", ) + \
                  mean_and_stddev(net_per_class[clazz]["a"]) + \
                  mean_and_stddev(net_per_class[clazz]["p"]) + \
                  mean_and_stddev(net_per_class[clazz]["r"]) + \
                  mean_and_stddev(net_per_class[clazz]["f"])
            csv.write(";{};{:.4};{:.4};{:.4};{:.4};{:.4};{:.4};{:.4};{:.4}".format(*row).replace(".", ","))
            csv.write("\n")

if __name__=="__main__":
    pass
    # out_file = "results_stat.csv"
    # create_total_F_csv(out_file)
    # for clazz in classes:
    #     create_class_F_csv(clazz, clazz+".csv")
    create_class_summary_for_fold("classes.csv", 10)