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
            eval_set.extend(folds[0])
            for fold in folds[1:]:
                training_set.extend(fold)
        train(training_set)
        evaluate(eval_set, folds_number, i)


def main(args=[]):
    #print get_class_folds(3, range(10))

    out = []
    def foo(x):
        out.append(x)
    crossvalidate(
        {
            1: range(10),
            2: range(10, 18),
            3: range(20, 32)
        },
        3,
        1,
        lambda x: foo("TRAIN: "+str(x)),
        lambda x, f, i: foo("EVAL: "+str(x)),
    )
    print "\n".join(out) # nie chcialo mi sie robic fixture, czytajac wynik stwierdzam, ze jest ok

if __name__ == '__main__':
    main()