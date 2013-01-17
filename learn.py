import random

def app_factors(app):
    """app -> {'factor' : 4}"""

def app_result_dict(app):
    """apps -> {id : 3}
    where 5 is admit
    0 is delete
    """

def merge_feature_sets(*feature_sets):
    """Merges dictionaries of feature dictionaries for apps
    dictionaries really ought to have all the same applications - throws an error if not

    >>> merge_feature_sets({1:{'tall':1, 'heavy':0}, 3:{'tall':1, 'heavy':1}}, {1:{'fast':0}, 3:{'fast':1}})
    {1: {'heavy': 0, 'tall': 1, 'fast': 0}, 3: {'heavy': 1, 'tall': 1, 'fast': 1}}
    """
    if len(feature_sets) == 1:
        return feature_sets[0]
    if any(fs.keys() != fs.keys() for fs in feature_sets[1:]):
        raise Exception("feature sets should have the same applications in them")
    for fs in feature_sets:
        if any(fs.values()[0].keys() != features.keys() for app_id, features in fs.iteritems()):
            raise Exception("Each feature set dict ought to have the same feature data for each app")
    combined = {app_id:{} for app_id in feature_sets[0].keys()}
    for fs in feature_sets:
        for app, features in fs.iteritems():
            for feature, value in features.iteritems():
                combined[app][feature] = value
    return combined

class Classifier(object):
    def __init__(self, feature_set, answers):
        self.feature_names = feature_set.values()[0].keys()
        self.app_ids = feature_set.keys()
        self.feature_set = feature_set
        self.answers = answers
        self.best_weights = self.randomize_weights()
        self.best_weights_score = -10000

    def randomize_weights(self):
        self.weights = {feature_name: (random.random() * 2 - 1) for feature_name in self.feature_names}
        return self.weights

    def perturb_weights(self, amount=.1):
        for weight in self.weights:
            self.weights += (random.random * 2 - 1) * amount

    def reset_weights_to_best(self):
        self.weights = {k:v for k,v in self.best_weights.iteritems()}

    def try_weights(self):
        app_totals = {app_id: 0 for app_id in self.app_ids}
        for app_id in self.app_ids:
            for feature, value in self.feature_set[app_id].iteritems():
                app_totals[app_id] += self.weights[feature] * value
        print 'predictive scores:', app_totals
        threshold = 0
        print self.app_ids
        guesses = {app_id : (1 if app_totals[app_id] > threshold else -1) for app_id in self.app_ids}
        print 'guesses:', guesses
        print 'real:   ', self.answers
        scores = [(1 if self.answers[app_id] == guesses[app_id] else 0) for app_id in self.app_ids]
        print 'scores:', scores
        score = sum(scores)
        if self.best_weights_score < score:
            print 'new best:', score
            self.best_weights = self.weights
            self.best_weights_score = score
        return score

def test():

    test_result_dict = {1:1, 2:1, 3:1, 4:1, 5:-1, 6:-1, 7:-1, 8:-1}
    test_feature_set_one = dict(zip(range(1,9), ({'age': x} for x in [4,5,6,23,5,22,23,24])))
    test_feature_set_two = dict(zip(range(1,9), ({'smart': x} for x in [1,1,1,0,0,0,1,1])))
    test_feature_set_three = dict(zip(range(1,9), ({'glasses': x} for x in [1,1,1,0,0,0,1,1])))

    print test_result_dict

    test_feature_set = merge_feature_sets(test_feature_set_one, test_feature_set_two, test_feature_set_three)
    c = Classifier(test_feature_set, test_result_dict)

    c.randomize_weights()
    while True:
        print c.try_weights()
        print c.randomize_weights()
        print c.best_weights, c.best_weights_score
        raw_input()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    test()
