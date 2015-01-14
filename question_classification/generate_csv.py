import os
import pickle

res_files = [ os.path.join("results", f) for f in os.listdir("results")
              if f.endswith(".obj")]

out_file = "results.csv"

with open(out_file, "w") as csv_file:
    csv_file.write("alg;folds;iter;recall;precision;accuracy;Fscore;\n")
    for res in res_files:
        splat = os.path.basename(res).split(".")
        csv_file.write('"' + splat[1] + '";' + splat[0] + ";" + splat[2] + ";")
        with open(res, "r") as res_file:
            eval_obj = pickle.load(res_file)
            csv_file.write(str(eval_obj).replace(".", ",") + "\n")
