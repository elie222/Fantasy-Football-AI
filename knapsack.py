#!/usr/bin/python
import sys

def zeros(rows,cols):
	row = []
	data = []
	for i in range(cols):
		row.append(0)
	for i in range(rows):
		data.append(row[:])
	return data
a = zeros(10,10)


def getItemsUsed(w,c):
    # item count
	i = len(c)-1
	# weight
	currentW =  len(c[0])-1
	
	# set everything to not marked
	marked = []
	for i in range(i+1):
		marked.append(0)	
		
	while (i >= 0 and currentW >=0):
		# if this weight is different than
		# the same weight for the last item
		# then we used this item to get this profit
		#
		# if the number is the same we could not add
		# this item because it was too heavy		
		if (i==0 and c[i][currentW] >0 )or c[i][currentW] != c[i-1][currentW]:
			marked[i] =1
			currentW = currentW-w[i]
		i = i-1
	return marked
	
	


# v = list of item values or profit
# w = list of item weight or cost
# W = max weight or max cost for the knapsack
def zeroOneKnapsack(v, w, W):
	# c is the cost matrix
	c = []
	n = len(v)
	#  set inital values to zero
	c = zeros(n,W+1)
	#the rows of the matrix are weights
	#and the columns are items
	#cell c[i,j] is the optimal profit
	#for i items of cost j
	
	#for every item
	for i in range(0,n):
		#for ever possible weight
		for j in range(0,W+1):
			#if this weight can be added to this cell
			#then add it if it is better than what we aready have
			
			if (w[i] > j):
				
				# this item is to large or heavy to add
				# so we just keep what we aready have
				
				c[i][j] = c[i-1][j]
			else:
				# we can add this item if it gives us more value
				# than skipping it
				
				# c[i-1][j-w[i]] is the max profit for the remaining 
				# weight after we add this item.
				
				# if we add the profit of this item to the max profit
				# of the remaining weight and it is more than 
				# adding nothing , then it't the new max profit
				# if not just add nothing.
				
				c[i][j] = max(c[i-1][j],v[i] +c[i-1][j-w[i]])
	print c
	return [c[n-1][W],getItemsUsed(w,c)]

if (len(sys.argv)!=3):
	print "Usage knapsack.py weight1-profit1,weight2-profit2,... max weight"
	print "Example:"
	print "knapsack.py 1-2,2-5,3-10 12"
	quit()
	
items = sys.argv[1].split(',')
w = []
v = []
total =0
for item in items:
	nums = item.split('-')
	w.append(int(nums[0]))
	v.append(int(nums[1]))

maxCost = int(sys.argv[2])
answer = zeroOneKnapsack(v,w,maxCost)
print "if my knapsack can hold %d pounds, i can get %d profit." % (maxCost,answer[0])
print "\tby taking item(s): ",
for i in range(len(answer[1])):
	if (answer[1][i] != 0):
		print i+1,

