# github.com/acdhemtos/Utils/evenly_distribute/script.py

import sys

info = [
 (int(num), text)
 for line in open(sys.argv[1]).read().strip().split("\n")
 for num, text in [line.split('\t', 1)]
]

def clean(lst):
	global info
	result = []
	for elm in lst:
		if isinstance(elm,int):
			item = info[elm-1]
			elm = [item[1]]*item[0]

		result.append(elm)
	return result

def s(*lists):
	lists = clean(lists)
	result = []
	for lst in lists:
		result.extend(lst)
	
	return result
