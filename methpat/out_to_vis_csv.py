import sys
from itertools import groupby

def pattern_list(pattern):
    result = []
    for char in pattern:
        if char == '1':
            result.append('True')
        elif char == '-':
            result.append('Missing')
        else:
            result.append('False')
    return result

def make_header(num_methyl_sites):
    methyl_headers = ','.join(map(str, range(1, num_methyl_sites + 1)))
    return 'Amplicon,Chr,Start,End,{},Mag'.format(methyl_headers)
    
in_file = open(sys.argv[1])

try:
    next(in_file)
except StopIteration as e:
    exit()

def get_amplicon_name(line):
    return line.split()[0]

for amplicon_name, amplicon_group in groupby(in_file, get_amplicon_name):
    first_line = True
    with open(amplicon_name + '.csv', 'w') as out_file:
        for line in amplicon_group:
            fields = line.split('\t')
            amplicon, chr, start, end, pattern, mag = fields[0:6]
            pat_list = pattern_list(pattern)
            if first_line:
                out_file.write(make_header(len(pat_list)) + '\n')
                first_line = False
            out_file.write((','.join([amplicon, chr, start, end] + pat_list + [mag])) + '\n')
