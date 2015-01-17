import codecs
import os
import pickle
from pybrain import TanhLayer, SoftmaxLayer
from pybrain.datasets import ClassificationDataSet, SupervisedDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from question_classification.config import classes, feats
from question_classification.crossvalidation import crossvalidate
from question_classification.model import Record
from question_classification.testing_procedure import data_root, evaluate, evaluate_base


def get_all_data_grouped_by_class():
    '''
    Records have no EAT!
    :return: dict(class_name -> list(Record)
    '''
    out = {}
    for c in classes:
        class_data = []
        with codecs.open(os.path.join(data_root, c+".txt"), 'r', 'utf8') as f:
            lines = f.readlines()
            idx = 0
            for line in lines:
                class_data.append(Record(c+"-"+str(idx), line, c, None))
        out[c] = class_data
    return out

def gather_experiments_results(folds, iter_count):
    net_placeholder = [None]
    def train(training_data):
        training_set = ClassificationDataSet(len(feats), nb_classes=len(classes))
        for inst in training_data:
            training_set.appendLinked(inst.features(), [inst.class_idx()])
        training_set._convertToOneOfMany([0, 1])
        net_placeholder[0] = buildNetwork(
            training_set.indim,
            int((training_set.indim + training_set.outdim)/2),
            training_set.outdim, bias=True,
            hiddenclass=TanhLayer,
            outclass=SoftmaxLayer
        )
        trainer = BackpropTrainer(
            net_placeholder[0], training_set, momentum=0.75, verbose=False, learningrate=0.05
        )
        trainer.trainUntilConvergence(maxEpochs=100, validationProportion=0.1)

    def do_evaluate(eval_data, folds_number, iter_number):
        eval_set = SupervisedDataSet(len(feats), 1)
        for inst in eval_data:
            eval_set.appendLinked(inst.features(), [inst.class_idx()])
        res = evaluate(net_placeholder[0], eval_set)
        with open(os.path.join("results", str(folds_number) + ".net." + str(iter_number) + ".obj"), "w") as f:
            pickle.dump(res, f)
        res = evaluate_base(eval_set)
        with open(os.path.join("results", str(folds_number) + ".base." + str(iter_number) + ".obj"), 'w') as f:
            pickle.dump(res, f)
        print res
    crossvalidate(get_all_data_grouped_by_class(), folds, iter_count, train, do_evaluate)

def main(args=[]):
    gather_experiments_results(2, 20)
    gather_experiments_results(3, 20)
    gather_experiments_results(4, 20)
    gather_experiments_results(5, 20)
    gather_experiments_results(6, 20)
    gather_experiments_results(7, 20)
    gather_experiments_results(8, 20)
    gather_experiments_results(9, 20)
    gather_experiments_results(10, 20)

if __name__ == '__main__':
    main()