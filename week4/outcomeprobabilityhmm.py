__author__ = 'Siddhant Srivastava'

import sys

filename = sys.argv[1]

with open(filename) as file:
	data = []
	for line in file:
		data.append(line[:-1])

string = data[0]
letters = data[2].split()
path = data[4]
states = data[6].split()
emission = []
emission.append(map(float,data[9].split()[1:]))
emission.append(map(float,data[10].split()[1:]))
statelookup = {states[i]:i for i in range(len(states))}
letterlookup = {letters[j]:j for j in range(len(letters))}

def outcomeprobability_hmm(string,path,emission,statelookup,letterlookup):
	prob = 1
	for i in range(len(path)):
		prob *= emission[statelookup[path[i]]][letterlookup[string[i]]]
	return prob

if __name__ == '__main__':
	ans = outcomeprobability_hmm(string,path,emission,statelookup,letterlookup)
	print ans
