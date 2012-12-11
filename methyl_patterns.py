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

def main():
    if len(sys.argv) < 2:
        exit('input file not specified')

    filename = sys.argv[1]

    read_states = {}

    with open(filename) as file:
        next(file) # skip the header
        for line in file:
            parts = line.split()
            read_id = parts[0]
            methyl = encode_methyl(parts[4])
            if read_id in read_states:
                read_states[read_id].append(methyl)
            else:
                read_states[read_id] = [methyl]

    methyl_states = {}
    for state in read_states.values():
        state = tuple(state)
        if state in methyl_states:
            methyl_states[state] += 1
        else:
            methyl_states[state] = 1

    for state in sorted(methyl_states, cmp=compare_state):
        print("{0} {1}".format(pretty_state(state), methyl_states[state]))

if __name__ == '__main__':
    main()
