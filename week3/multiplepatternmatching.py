__author__ = 'Siddhant Srivastava'

import sys
filename = sys.argv[1]

with open(filename) as file:
    data = []
    for line in file:
        data.append(line[:-1])
word = data[0]
patterns = data[1:]

def burrows_wheeler_transform(word):
    word += ['', '$'][word[-1] != '$']
    L = len(word)
    cyclic_rot_index = lambda i, n: word[(n-i) % L]
    cyclic_comp = lambda i, j, n=0: [1, -1][cyclic_rot_index(i,n) < cyclic_rot_index(j,n)] if cyclic_rot_index(i,n) != cyclic_rot_index(j,n) else cyclic_comp(i,j,n+1)
    cyclic_sort = sorted(xrange(len(word)), cmp=cyclic_comp)
    return ''.join([cyclic_rot_index(i, -1) for i in cyclic_sort])


def construct_suffix_array(word):
    word += ['', '$'][word[-1] != '$']
    suffix_comp = lambda i,j: [1, -1][word[i] < word[j]] if word[i] != word[j] else suffix_comp(i+1,j+1)
    suffix_array = sorted(xrange(len(word)), cmp=suffix_comp)
    return suffix_array


def get_multi_pattern_count(word, patterns):
    bwt = burrows_wheeler_transform(word)
    suffix_array = construct_suffix_array(word)
    symbols = set(bwt)
    current_count = {ch:0 for ch in symbols}
    count = {0:{ch:current_count[ch] for ch in symbols}}
    for i in xrange(len(bwt)):
        current_count[bwt[i]] += 1
        count[i+1] = {ch:current_count[ch] for ch in symbols}
    sorted_bwt = sorted(bwt)
    first_occurrence = {ch:sorted_bwt.index(ch) for ch in set(bwt)}
    matches = []
    for pattern in patterns:
        matches += multi_pattern_match_bw(bwt, suffix_array, first_occurrence, count, pattern)
    return matches


def multi_pattern_match_bw(bwt, suffix_array, first_occurrence, count, pattern):
    top, bottom = 0, len(bwt) - 1
    while top <= bottom:
        if pattern != '':
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol in bwt[top:bottom+1]:
                top = first_occurrence[symbol] + count[top][symbol]
                bottom = first_occurrence[symbol] + count[bottom+1][symbol] - 1
            else:
                return []
        else:
            return [suffix_array[i] for i in xrange(top, bottom+1)]


if __name__ == '__main__':
    pattern_locations = get_multi_pattern_count(word, patterns)
    pattern_locations = map(str, sorted(pattern_locations))
    print ' '.join(pattern_locations)
    #with open('output/Assignment_10F.txt', 'w') as output_data:
    #    output_data.write(' '.join(pattern_locations))

