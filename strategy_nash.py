# coding: utf-8
from pulp import *
import time
import numpy as np
import logging

# TIME : 1.74 seconds for (10,10,0)
# TODO : Properly eliminate dominated strategies
#         Try to implement a dynamic programming method in order to improve speed


# We define the distance between the two castles.
SIZE = 7

# This object contains all the states already computed in order not to compute them several times
SEEN = {}

DEBUG = False

# set up logger
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
# SHORTER_FORMAT = "[%(filename)s:%(lineno)s ] %(message)s"
# logging.basicConfig(format=SHORTER_FORMAT)
if DEBUG:
	logger.setLevel(logging.DEBUG)


def rem(tab, k):
	for i in range(len(tab)):
		if tab[i] == k:
			del tab[i]
			return tab


def eliminate_dominated_strategies(tab):
	old_size = 0
	tab = np.insert(tab, 0, range(1, tab.shape[0] + 1), axis=1)
	tab = np.insert(tab, 0, range(0, tab.shape[1]), axis=0)
	while tab.size is not old_size:
		old_size = tab.size
		tab = eliminate_strategies_in(tab).transpose()
		tab = eliminate_strategies_in(tab, transposed=True).transpose()
	return tab


def eliminate_strategies_in(tab, transposed=False):
	to_remove = []

	strategy_index = 1
	while strategy_index < len(tab):
		other_strategy_index = 1
		while other_strategy_index < len(tab):
			enemy_strategy_index = 1
			same = True

			if other_strategy_index == strategy_index:
				other_strategy_index += 1
				enemy_strategy_index = 1

			if other_strategy_index == len(tab):
				tab = np.delete(tab, to_remove, 0)
				return tab

			while enemy_strategy_index < len(tab[0]):
				gain_player1 = tab[strategy_index][enemy_strategy_index]
				gain_player2 = tab[other_strategy_index][enemy_strategy_index]
				# if ((gain_player1 > gain_player2) != transposed) or ((gain_player1 < gain_player2) != (not transposed)):
				not_dominated = gain_player1 < gain_player2 if transposed else gain_player1 > gain_player2
				if not_dominated:
					# Strategy is NOT dominated by other_strategy_index
					other_strategy_index += 1
					enemy_strategy_index = len(tab[0]) + 1
					break

				elif tab[strategy_index][enemy_strategy_index] != tab[other_strategy_index][enemy_strategy_index]:
					same = False

				enemy_strategy_index += 1

			if enemy_strategy_index != len(tab[0]) + 1 and not same:
				# Strategy is dominated by other_strategy_index
				logger.debug("%s < %s", strategy_index, other_strategy_index)
				logger.debug("\n%s", np.array(tab))
				# result_list = rem(result_list, strategy_index)
				to_remove.append(strategy_index)
				# other_strategy_index = 0
				break
			if same:
				break

		strategy_index += 1

	return np.delete(tab, to_remove, 0)


def find_min_and_max(tab):
	matrix = np.array(tab)
	return matrix.min(), matrix.max()


def enum_states_from(n1, n2, t):
	result_states = []
	for x in range(1, n1 + 1):
		states_for_strategy = []
		for y in range(1, n2 + 1):
			if x == y:
				states_for_strategy.append((n1 - x, n2 - y, t))
			elif x > y:
				states_for_strategy.append((n1 - x, n2 - y, t + 1))
			else:
				# x < y:
				states_for_strategy.append((n1 - x, n2 - y, t - 1))
		result_states.append(states_for_strategy)
	return result_states


def calculate_dist_and_utility(tab):
	# Variables
	variables = []
	distribution_indices = []
	for i in range(1, len(tab)):
		variables.append(LpVariable("p" + str(tab[i][0]), 0, 1))
		distribution_indices.append(tab[i][0])
	weights = tab

	# Solving the problem from the vectors Variables and weights
	linear_problem = LpProblem("test1", LpMaximize)

	(Min, Max) = find_min_and_max(weights)
	t = LpVariable("t", Min, Max)

	# Objective
	linear_problem += t

	# Constraints
	for column in range(1, len(weights[0])):
		utility = 0
		for row in range(1, len(weights)):
			logger.debug("\ntab: \n%s, row: %s, column: %s, variables: %s", weights, row, column, variables)
			utility += variables[row - 1] * weights[row][column]
		# print("UTILITY : ",utility)
		linear_problem += utility - t >= 0

	probabilities = 0
	for variable in variables:
		probabilities += variable
	linear_problem += probabilities == 1

	global DEBUG
	# produce output only in DEBUG mode
	linear_problem.solve(GLPK_CMD(msg=DEBUG))

	distribution_list = []
	# Solution
	for v in linear_problem.variables():
		# print(v.name, "=", v.varValue)
		if v.name != "t":
			distribution_list.append(v.varValue)

	# print("objective=", value(linear_problem.objective))

	return (distribution_list, distribution_indices), value(linear_problem.objective)


# noinspection PyPep8Naming
def G(x, y, t):
	# First the initialization cases
	if t == 0 and x == y:
		return 0
	elif t <= -(SIZE - 1) / 2:
		return -1
	elif t >= (SIZE - 1) / 2:
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
		elif (x + t) == 0:
			return 0
		elif x > t:
			return 1
		elif x < t:
			return -1
		else:
			raise ValueError("Impossible case")
	else:

		# It's not possible to get the utility from the state, so we use the function Solve() to get the utility and
		# the mixed strategy.

		if (x, y, t) in SEEN:
			return SEEN[(x, y, t)]

		(_, utility) = solve(x, y, t)

		# We add the result of the computation in the dictionary SEEN in order to not compute it several times
		SEEN[(x, y, t)] = utility

		return utility


def solve(x, y, t):
	# We enumerate all the reachable states
	states = enum_states_from(x, y, t)

	# If there is only one issue for the player 1, the profits will be the arg min of all the issues from the player 2
	if x == 1:
		x, y, t = states[0][0]
		mini = G(x, y, t)
		for state in states[0]:
			x, y, t = state
			profits = G(x, y, t)
			if profits < mini:
				mini = profits
		return ([1.0], [1]), mini

	# We replace all the states by their utility
	for row in states:
		for i in range(len(row)):
			(x, y, t) = row[i]
			row[i] = G(x, y, t)

	# We delete all the dominated strategies
	# not_dominated_strategy_indices = get_not_dominated_strategies(states)
	game = eliminate_dominated_strategies(np.array(states))

	# for i in range(len(states) - 1, -1, -1):
	# 	if i not in not_dominated_strategy_indices:
	# 		del states[i]

	return calculate_dist_and_utility(game)


def represents_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


# print(solve(5, 4, -1))

def calculate_what_to_play(left, right, position):
	((distribution, distribution_ind), g) = solve(left, right, position)
	if DEBUG:
		print("--- %s seconds ---" % (time.time() - start_time))

	distribution = np.array(distribution)
	distribution /= distribution.sum()
	if DEBUG:
		print("Distribution:", list(distribution), distribution_ind)
		print("Utility: ", g)
	X = np.random.choice(distribution_ind, 1, p=distribution)
	return int(X[0])


if __name__ == "__main__":
	if len(sys.argv) == 4:
		try:
			start_time = time.time()
			((distribution, distribution_ind), g) = solve(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
			print("--- %s seconds ---" % (time.time() - start_time))

			distribution = np.array(distribution)
			distribution /= distribution.sum()
			print("Distribution:", list(distribution), distribution_ind)
			print("Utility: ", g)
			X = np.random.choice(distribution_ind, 1, p=distribution)
			print("You should shoot", X[0], "rocks.")
		except ValueError:
			for index in range(1, len(sys.argv)):
				if not represents_int(sys.argv[index]):
					print("<", sys.argv[index], "> is not an integer")
					print("Usage: Python3 strategy_nash.py <x y t> where x,y,t are integers")
					break
	else:
		print("Usage: Python3 strategy_nash.py <x y t>")
