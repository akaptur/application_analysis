from glob import glob
import re
from subprocess import Popen, PIPE
from itertools import repeat
import pdb
import json

working_file = '/tmp/tempfile.txt'

def code_input():
    data = json.load(open('appdata.json'))
    return data

def remove_line(working_file):
    lines = ''.join(open(working_file).readlines()[1:])
    open(working_file, 'w').write(lines)

def put_in_working_file(data):
    open(working_file, 'w').write(data.encode('ascii', 'replace'))

def build_re_match():
    separator = r'''\W*'''
    canon = separator
    for i in range(1, 101):
        if i % 15 == 0:
           canon += 'fizzbuzz'
        elif i % 3 == 0:
           canon += 'fizz'
        elif i % 5 == 0:
           canon += 'buzz'
        else:
           canon += str(i)
        canon += separator
    canon += '$'
    return canon

def no_fizzbuzz():
    separator = r'''\W*'''
    wrong = separator
    for i in range(1, 101):
        if i % 3 == 0 or i % 5 == 0:
            wrong += '(fizz|buzz)'
        else:
            wrong += str(i)
        wrong += separator
    wrong += '$'
    return wrong

def wrong_range():
    canon = build_re_match()
    new_endpoint = canon.rfind('buzz')
    wrong = canon[:new_endpoint]
    wrong += '$'
    return wrong

patterns = {'success': build_re_match(),
            'logic_error': no_fizzbuzz(),
            'range_error': wrong_range()}

def try_fizzbuzz(fizzbuzz):
    """Tries a fizzbuzz with many languages and edits
    Returns working language or None"""
    languages = ['python', 'ruby', 'node']
    data = dict(zip(languages,repeat(0)) + zip(patterns.keys(),repeat(0)))
    put_in_working_file(fizzbuzz)
    for i in range(3):
        for lang in languages:
            print 'trying to run with', lang, 'with', i, 'lines removed'
            print open(working_file).read()
            match = try_working_file(lang)
            if match:
                print 'match'
                data[lang] = 1
                data[match] = 1
                return data
        remove_line(working_file)
    return data

def try_working_file(lang):
    p = Popen([lang, working_file], stdout=PIPE, stderr=PIPE)
    return success_with_patterns(p.stdout.read())

def success_with_patterns(fizzbuzz_output):
    return success(fizzbuzz_output, **patterns)

def success(fizzbuzz_output, **patterns):
    for result, matcher in patterns.iteritems():
        if re.match(matcher, fizzbuzz_output, re.IGNORECASE):
            return result
    return None

def build_feature_set():
    app_data = code_input()
    feature_set = {}
    for app in app_data:
        feature_set[app['id']] = try_fizzbuzz(app['data']['fizzbuzz'])
    return feature_set

def verbose_build():
    app_data = code_input()
    outputs = {}
    for app in app_data:
        print app.keys()
        print app['data'].keys()
        print '---'
        print 'attempting', app['id']
        print app['data']['fizzbuzz']
        print '---'
        outputs[app['id']] = try_fizzbuzz(app['data']['fizzbuzz'])
        print outputs


if __name__ == '__main__':
    verbose_build()
