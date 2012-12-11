# Assumptions: a read only maps to one amplicon (not overlapping with another).

import sys

def encode_methyl(char):
    if char == 'z':
        # unmethylated
        return 0
    elif char == 'Z':
        # methylated
        return 1
    else:
        exit('strange methyl state ' + char)

def pretty_state(state):
    return ''.join([str(x) for x in state])

def compare_state(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    if len1 == len2:
        return cmp(s1, s2)
    else:
        return cmp(len1, len2)

# cpg_sites are encoded and lists of pairs of (pos, methyl)
class Read(object):
    def __init__(self, amplicon, cpg_sites):
        self.amplicon = amplicon
        self.cpg_sites = cpg_sites

def main():
    if len(sys.argv) < 2:
        exit('input file not specified')

    filename = sys.argv[1]

    reads = {}

    with open(filename) as file:
        next(file) # skip the header
        for line in file:
            parts = line.split()
            read_id, strand, amplicon, pos, methyl = parts[0:5]
            methyl = encode_methyl(methyl)
            pos = int(pos)
            if read_id in reads:
                reads[read_id].cpg_sites.append((pos, methyl))
            else:
                reads[read_id] = Read(amplicon, [(pos, methyl)])

    # list of tuples (amplicon, sorted_cpg_sites)
    methyl_states = []
    for read in reads.values():
        methyl_states.append((read.amplicon, tuple(sorted(read.cpg_sites))))

    # amplicon -> cpg_sites -> count
    methyl_state_counts = {}
    for amplicon, cpg_sites in methyl_states:
        if amplicon in methyl_state_counts:
            this_amplicon = methyl_state_counts[amplicon]
            if cpg_sites in this_amplicon:
                this_amplicon[cpg_sites] += 1
            else:
                this_amplicon[cpg_sites] = 1
        else:
            methyl_state_counts[amplicon] = { cpg_sites : 1 }

    result = []
    for amplicon in methyl_state_counts:
        for cpg_sites, count in methyl_state_counts[amplicon].items():
            start_pos = cpg_sites[0][0]
            end_pos = cpg_sites[-1][0]
            binary = pretty_state([cpg[1] for cpg in cpg_sites])
            result.append((amplicon, start_pos, end_pos, binary, count))


    print('\t'.join(["<Chr/amplicon ID>", "<Base position start/CpG start>",
          "<Base position end/CpG end>", "<Methylation pattern>", "<count>"]))

    for amplicon, start, end, binary, count in sorted(result):
        print('\t'.join([amplicon, str(start), str(end), binary, str(count)]))

if __name__ == '__main__':
    main()
