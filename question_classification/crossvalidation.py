'''
This won't use any neural network-related stuff. This just iterates over dataset with given folds,
'''
from itertools import product

def get_class_folds(folds_number, class_data):
    '''
    :param folds_number: int
    :param class_data: list(X)
    :return: list(list(X))
    '''
    out = [ [] for i in xrange(folds_number) ]
    idx = 0
    for instance in class_data:
        out[idx].append(instance)
        idx = (idx +1) % folds_number
    return out

def crossvalidate(all_data, folds_number, train, evaluate):
    '''
    :param all_data: Same structure as output of get_all_data_grouped_by_class (see experiments module; tree leaves are of type X)
    :param folds_number: int
    :param train: function(list(X) -> None); called on testing subset (of size len(all_data)/folds_number)
    :param evaluate: function(list(X) -> None); called on evaluation subset (of size (folds_number-1)*len(all_data)/folds_number)
    :return: None
    '''
    keys = list(all_data.keys())
    folds_per_class = { c: get_class_folds(folds_number, all_data[c]) for c in keys }
    configs = product(*map(lambda x: range(len(folds_per_class[x])), keys))
    for config in configs:
        print "config:", config
        map_config = dict(zip(keys, config))
        training_set = []
        eval_set = []
        for clazz in keys:
            for fold_no in range(len(folds_per_class[clazz])):
                extended = training_set if (fold_no == map_config[clazz]) else eval_set
                extended.extend(folds_per_class[clazz][fold_no])
        train(training_set)
        evaluate(eval_set)


def main(args=[]):
    assert get_class_folds(3, range(10)) == [ [0, 3, 6, 9], [1, 4, 7], [2, 5, 8] ]

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
        lambda x: foo("TRAIN: "+str(x)),
        lambda x: foo("EVAL: "+str(x)),
    )
    print "\n".join(out) # nie chcialo mi sie robic fixture, czytajac wynik stwierdzam, ze jest ok