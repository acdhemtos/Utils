# github.com/acdhemtos/Utils/evenly_distribute/order.py

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
def p(*lists):
	lists = clean(lists)
	if len(lists)==1:
		return lists[0]
	
	lists.sort(key=len, reverse=True)
	
	large = lists.pop()
	
	while lists:
		small = lists.pop()
		if len(small) == len(large):
			large = [item for pair in zip(small, large) for item in pair]
		
		if len(small) > len(large):
			small,large = large,small
		
		result = []	
		small.append(None)
		while small:
			k = len(large)//len(small)
			
			result.extend(large[:k])
			del large[:k]
			
			result.append(small.pop(0))
		
		result.pop()
		
		large = result
	
	return large
