import codecs
import os
from pybrain import TanhLayer, SoftmaxLayer
from pybrain.datasets import ClassificationDataSet, SupervisedDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from question_classification.config import classes, feats
from question_classification.crossvalidation import crossvalidate
from question_classification.model import Record
from question_classification.testing_procedure import data_root, evaluate


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

def gather_experiments_results(folds):
    net_placeholder = [None]
    results = []
    def train(training_data):
        training_set = ClassificationDataSet(len(feats), nb_classes=len(classes))
        for inst in training_data:
            training_set.appendLinked(inst.features(), [inst.class_idx()])
        net_placeholder[0] = buildNetwork(
            training_set.indim,
            int((training_set.indim + training_set.outdim)/2),
            training_set.outdim, bias=True,
            hiddenclass=TanhLayer,
            outclass=SoftmaxLayer
        )
        trainer = BackpropTrainer(
            net_placeholder[0], training_set, momentum=0.75, verbose=True, learningrate=0.05
        )
        trainer.trainUntilConvergence(maxEpochs=100, validationProportion=0.1)
    def do_evaluate(eval_data):
        eval_set = SupervisedDataSet(len(feats), 1)
        for inst in eval_data:
            eval_set.appendLinked(inst.features(), [inst.class_idx()])
        results.append(evaluate(net_placeholder[0], eval_set))
    crossvalidate(get_all_data_grouped_by_class(), folds, train, do_evaluate)
    return results

def main(args=[]):
    print gather_experiments_results(2)