from glob import glob
import re
from subprocess import Popen, PIPE
from itertools import repeat
import pdb

working_file = '/tmp/tempfile.txt'

def code_input():
    return glob('*.txt')

def remove_line(working_file):
    lines = ''.join(open(working_file).readlines()[1:])
    open(working_file, 'w').write(lines)

put_file_in_working_file = lambda: open(working_file, 'w').write(open(filename).read())

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
    return wrong

def wrong_range():
    canon = build_re_match()
    new_endpoint = canon.rfind('buzz')
    return canon[:new_endpoint]

patterns = {'success': build_re_match(),
            'logic_error': no_fizzbuzz()
            'range_error': wrong_range()}

def try_fizzbuzz(filename):
    """Tries a fizzbuzz with many languages and edits
    Returns working language or None"""
    languages = ['python', 'ruby', 'node']
    put_file_in_working_file()
    for i in range(3):
        for lang in languages:
            print 'trying to run with', lang, 'with', i, 'lines removed'
            print open(working_file).read()
            match = try_working_file(lang)
                print 'match'
                return lang, match
        remove_line(working_file)
    return None, None

def try_working_file(lang):
    p = Popen([lang, working_file], stdout=PIPE, stderr=PIPE)
    return success_with_patterns(p.stdout.read())

def success_with_patterns(fizzbuzz_output):
    return success(fizzbuzz_output, patterns)

def success(fizzbuzz_output, **patterns):
    for result, matcher in patterns.iteritems():
        if re.match(matcher, fizzbuzz_output, re.IGNORECASE):
            return result
    return None

if __name__ == '__main__':
    code_files = code_input()
    outputs = []
    for filename in code_files:
        print '---'
        print 'attempting', filename
        print open(filename).read()
        print '---'
        outputs.append(try_fizzbuzz(filename))
        print outputs
        # pdb.set_trace()