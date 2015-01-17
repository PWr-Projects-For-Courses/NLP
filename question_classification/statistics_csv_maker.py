import os
import pickle
import scipy.stats
import numpy


def determineWinner(net_evals, base_evals):
    t, p = scipy.stats.ttest_rel(net_evals, base_evals)
    if p/2 < confidence_level:
        if t > 0:
            return '"NN"'
        return '"B"'
    else:
        return '"-"'

res_files = [ os.path.join("results", f) for f in os.listdir("results")
              if f.endswith(".obj")]

out_file = "results_stat.csv"

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
        res_map[fold].append((eval_obj.getWeightedFMeasure(), iter_no))


with open(out_file, "w") as csv_file:
    csv_file.write("folds;netFscore;baseFscore;win;\n")
    for fold in net_res.keys():
        csv_file.write(str(fold)+";")

        net_evals = [tup[0] for tup in sorted(net_res[fold], key=lambda tup: tup[1])]
        num_net_evals = numpy.array(net_evals)
        net_mean = numpy.mean(num_net_evals)
        net_stddev = numpy.std(num_net_evals)
        csv_file.write(str(net_mean) + "+-" + str(net_stddev) + ";")

        base_evals = [tup[0] for tup in sorted(base_res[fold], key=lambda tup: tup[1])]
        num_base_evals = numpy.array(base_evals)
        base_mean = numpy.mean(num_base_evals)
        base_stddev = numpy.std(num_base_evals)
        csv_file.write(str(base_mean) + "+-" + str(base_stddev) + ";")

        csv_file.write(determineWinner(net_evals, base_evals) + ";\n")
