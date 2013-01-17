import json
import pdb

def get_apps():
    apps = json.load(open('appdata.json'))
    return apps

def count_links(app):
    links = app['data']['links'].split('\n')
    return len(links)

def has_github(app):
    return any('github.com' in elem for elem in app['data']['links'].split('\n'))

def has_stackoverflow(app):
    return any('stackoverflow.com' in elem for elem in app['data']['links'])

def has_code_link(app):
    code_q, code_ans = app['data']['questions'][0]
    if 'http' in code_ans:
        return True
    else:
        return any(tld in code_ans for tld in ['.org', '.net', '.com', '.ly'])

def combined_answer_length(app):
    '''Combined length of answers, excluding code question.'''
    return sum(len(ans) for [question, ans] in app['data']['questions'][1:])

def says_learn(app):
    why_hs, ans = app['data']['questions'][-1]
    return 'learn' in why_hs


def all_link_data(app):
    not_factors = ['all_link_data', 'get_apps', 'loop']
    factors = [(name, func) for (name, func) in globals().items() if callable(func) and name not in not_factors]
    data = dict((name, func(app)) for (name, func) in factors)
    return data

def loop():
    apps = get_apps()
    feature_set = {}
    for app in apps:
        feature_set[app['id']] = all_link_data(app)
    return feature_set

if __name__ == '__main__':
    apps = get_apps()
    for app in apps:
        data = all_link_data(app)
        print data
        raw_input()