from pulp import *


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

    P = []
    # Solution
    for v in prob.variables():
        #print(v.name, "=", v.varValue)
        if v.name != "t":
            P.append(v.varValue)

    #print("objective=", value(prob.objective))

    return(P, value(prob.objective))




print(LinProg([[0,-1],[-1,0]]))

