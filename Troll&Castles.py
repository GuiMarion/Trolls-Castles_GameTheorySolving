
# coding: utf-8
from pulp import *
import time

# TIME : 1.74 seconds for (10,10,0)
# TODO : Properly eliminate dominated stategies
#		  Try to implement a dynamic programming method in order to improve speed


# We define the distance between the two castles.
global SIZE
SIZE = 5

#This object contains all the states already computed in order to not compute them several times
global SEEN
SEEN = {}

def minMax(Tab):
	Min = Tab[0][0]
	Max = Tab[0][0]
	for liste in Tab:
		for elem in liste:
			if elem >Max :
				Max = elem
			elif elem < Min:
				Min = elem 
	return (Min,Max)

def Print(Tab):
	for row in Tab:
		print()
		for elem in row:
			print(elem, end=" ")
	print()

def enumStatesfrom(n1,n2,t):
	Liste = []
	for x in range(1, n1+1):
		L = []
		for y in range(1, n2+1):
			if x == y :
				L.append((n1-x, n2-y, t))
			elif x > y :
				L.append((n1-x, n2-y, t+1))
			elif x < y :
				L.append((n1-x, n2-y, t-1))
			else :
				raise ValueError("Impossible case")
		Liste.append(L)
	return Liste

def LinProg(Tab):

	# Variables
	variables = []
	for i in range(len(Tab)):
		variables.append(LpVariable("p"+str(i), 0, 1))
	weights = Tab

	# Solving the problem from the vectors Variables and weights
	prob = LpProblem("test1", LpMaximize)

	(Min,Max) = minMax(weights)
	t = LpVariable("t",Min,Max)
	
	# Objective
	prob += t

	# Constraints
	for column in range(len(weights[0])):
		utility = 0
		for row in range(len(weights)):
			utility += variables[row]*weights[row][column]
		#print("UTILITY : ",utility)
		prob += utility - t >= 0

	probabilities = 0
	for variable in variables:
		probabilities += variable
	prob += probabilities == 1

	GLPK().solve(prob)

	P = []
	# Solution
	for v in prob.variables():
		#print(v.name, "=", v.varValue)
		if v.name != "t":
			P.append(v.varValue)

	#print("objective=", value(prob.objective))

	return(P, value(prob.objective))


def len1(x):
	l = -1
	for i in range(len(x)):
		if x[i] == 1 and l > -1:
			return -1
	
		elif x[i] == 1:
			l = i
			
	return l


def G(x,y,t):

	# First the initialization cases
	if t == 0 and x == y:
		return 0
	elif t <= -(SIZE-1)/2:
		return -1
	elif t >= (SIZE-1)/2:
		return 1    
	elif x == 0: 
		if t < 0: 
			return -1
		elif y == t:
			return 0
		elif y < t:
			return 1
		elif y > t:
			return -1
		else:
			raise ValueError("Impossible case")
	elif y == 0: 
		if t > 0:
			return 1
		elif (x+t) == 0:
			return 0
		elif x > t:
			return 1
		elif x < t:
			return -1
		else:
			raise ValueError("Impossible case")
	else:

		# It's not possible to get the utility from the state, so we use the function Solve() to get the utility and 
		# the mixed stategy. 

		if (x,y,t) in SEEN :
			return SEEN[(x,y,t)]


		(_, g) = Solve(x,y,t)

		# We add the result of the computation in the dictionary SEEN in order to not compute it several times
		SEEN[(x,y,t)] = g

		return g

		# # Here is the reccurence
		
		# # We enumerate all the reachable states
		# states = enumStatesfrom(x,y,t)
		
				
		# #If there is only one issue for the player 1, the profits will be the argmin of all the issues from the player 2
		# if x == 1: 
		#     x,y,t = states[0][0]
		#     mini = G(x,y,t)
		#     for state in states[0]:
		#         x,y,t = state
		#         profits = G(x,y,t)
		#         if  profits < mini:
		#             mini = profits
		#     return mini
		
		# # If there is more the one issue for the player 1 we try to reduce the number of issues by finding dominated ones
		# p = []
		# for x1 in range(len(states)):
		#     p.append(0)
		#     for y in range(len(states[0])):
		#         for x2 in range(len(states)):
		#             if x1 < x2 :
		#                 p[x1] = 1        

		
		# if len1(p) > -1: 
		#     x,y,t = states[len1(p)][0]
		#     mini = G(x,y,t)
		#     for state in states[len1(p)]:
		#         x,y,t = state
		#         profits = G(x,y,t)
		#         if  profits < mini:
		#             mini = profits
		#     return mini


def Solve(x,y,t):

	# We enumerate all the reachable states
	states = enumStatesfrom(x,y,t)

	#If there is only one issue for the player 1, the profits will be the argmin of all the issues from the player 2
	if x == 1: 
		x,y,t = states[0][0]
		mini = G(x,y,t)
		for state in states[0]:
			x,y,t = state
			profits = G(x,y,t)
			if  profits < mini:
				mini = profits
		return ([1.0],mini)


	# We replce all the states by their utility
	for row in states:
		for i in range(len(row)):
			(x,y,t) = row[i]
			row[i] = G(x,y,t)

	return LinProg(states)


if __name__ == "__main__":
	if len(sys.argv) == 4:
		start_time = time.time()
		print(Solve(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])))
		print("--- %s seconds ---" % (time.time() - start_time))

	else:
		print("Usage: Python3 Troll&Castles <x y t>")


#print(Solve(5,4,-1))

