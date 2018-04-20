# Example of Linear Programming solving using pulp

from pulp import *

prob = LpProblem("test1", LpMaximize)
# Variables
variables = [ LpVariable("p1", 0, 1) , LpVariable("p2", 0, 1) ]
weights = [[1,-1],[-1,0]]
# p1 = lpvariable("p1", 0, 1)
# p2 = lpvariable("p2", 0, 1)

t = LpVariable("t",-1,0)


# Objective
prob += t

# Constraints
for column in range(len(weights)):
    utility = 0
    for row in range(len(weights[0])):
        utility += variables[row]*weights[column][row]
    prob += utility - t >= 0
# prob += -p1 - t >= 0
# prob += p1-p2 - t >= 0
probabilities = 0
for variable in variables:
    probabilities += variable
prob += probabilities == 1

GLPK().solve(prob)

# Solution
for v in prob.variables():
    print(v.name, "=", v.varValue)

print("objective=", value(prob.objective))
