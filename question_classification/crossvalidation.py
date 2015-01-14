'''
This won't use any neural network-related stuff. This just iterates over dataset with given folds,
'''
from itertools import product
import random


def get_class_folds(folds_number, class_data):
    '''
    :param folds_number: int
    :param class_data: list(X)
    :return: list(list(X))
    '''
    out = [ [] for i in xrange(folds_number) ]
    idx = 0
    data = list(class_data)
    random.shuffle(data)
    for instance in data:
        out[idx].append(instance)
        idx = (idx +1) % folds_number
    return out

def crossvalidate(all_data, folds_number, iter_count, train, evaluate):
    '''
    :param all_data: Same structure as output of get_all_data_grouped_by_class (see experiments module; tree leaves are of type X)
    :param folds_number: int
    :param iter_count: int
    :param train: function(list(X) -> None); called on testing subset (of size len(all_data)/folds_number)
    :param evaluate: function(list(X) -> None); called on evaluation subset (of size (folds_number-1)*len(all_data)/folds_number)
    :return: None
    '''
    for i in xrange(iter_count):
        folds_per_class = { c: get_class_folds(folds_number, d) for c, d in all_data.iteritems() }
        training_set = []
        eval_set = []
        for clazz, folds in folds_per_class.iteritems():
            training_set.extend(folds[0])
            for fold in folds[1:]:
                eval_set.extend(fold)
        train(training_set)
        evaluate(eval_set, folds_number, i)


def main(args=[]):
    assert get_class_folds(3, range(10)) == [ [0, 3, 6, 9], [1, 4, 7], [2, 5, 8] ]

    out = []
    def foo(c, x):
        out.append(c, x)
    crossvalidate(
        {
            1: range(10),
            2: range(10, 18),
            3: range(20, 32)
        },
        3,
        lambda c, x: foo("TRAIN: "+str(x)),
        lambda c, x: foo("EVAL: "+str(x)),
    )
    print "\n".join(out) # nie chcialo mi sie robic fixture, czytajac wynik stwierdzam, ze jest ok