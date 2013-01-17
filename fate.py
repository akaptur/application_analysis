import evaluate_fizzbuzzes
import some_factors
import learn
import json
import pdb

def get_apps():
    apps = json.load(open('appdata.json'))
    return apps


if __name__ == '__main__':
    apps = get_apps()
    outcome = dict((app['id'], app['admitted']) for app in apps)

    fizzbuzz = evaluate_fizzbuzzes.build_feature_set()
    other_factors = some_factors.loop()

    big_feature_set = learn.merge_feature_sets(fizzbuzz, other_factors)
    print big_feature_set
    print outcome

    c = learn.Classifier(big_feature_set, outcome)
    while True:
        c.try_weights()
        print c.randomize_weights()
        print c.best_weights, c.best_weights_score
        raw_input()

