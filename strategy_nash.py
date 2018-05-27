# coding: utf-8
from pulp import *
import time
import numpy as np
import logging
import pickle
from tqdm import tqdm
from optparse import OptionParser

# TIME : 1.74 seconds for (10,10,0)
# TODO: Try to implement a dynamic programming method in order to improve speed


# We define the distance between the two castles.
SIZE = 7

# This object contains all the states already computed in order not to compute them several times
SEEN = {}
distributions = {}

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


def triple_to_string(triple):
	return str(triple[0]) + "," + str(triple[1]) + "," + str(triple[2])


def eliminate_dominated_strategies(tab):
	old_size = 0
	tab = np.insert(tab, 0, range(1, tab.shape[0] + 1), axis=1)
	tab = np.insert(tab, 0, range(0, tab.shape[1]), axis=0)
	# while generating the pickles, the elimination took too long, so for better performance,
	# it might be better to remove this altogether. Uncomment if you want to observe the elimination
	# process e.g. with DEBUG
	# while tab.size is not old_size:
	# 	old_size = tab.size
	# 	tab = eliminate_strategies_in(tab).transpose()
	# 	tab = eliminate_strategies_in(tab, transposed=True).transpose()
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
				to_remove.append(strategy_index)
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
		# zfill is necessary : linear_problem.variables() list variables in alphabetical order, so after p1 it's p10 and
		# not p2. with zfill(4), we ensure the correct behaviour if there is less than 10000 variable
		variables.append(LpVariable("p" + str(tab[i][0]).zfill(4), 0, 1))
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

		global SEEN
		if (x, y, t) in SEEN:
			return SEEN[(x, y, t)]

		(_, utility) = solve(x, y, t)

		# We add the result of the computation in the dictionary SEEN in order to not compute it several times
		SEEN[(x, y, t)] = utility

		return utility


def solve(x, y, t):
	# We enumerate all the reachable states
	triple = (x, y, t)

	global distributions
	if triple in distributions:
		return distributions[triple]

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
		distributions[triple] = ([1.0], [1]), mini
		return ([1.0], [1]), mini

	# We replace all the states by their utility
	for row in states:
		for i in range(len(row)):
			(x, y, t) = row[i]
			row[i] = G(x, y, t)

	# We delete all the dominated strategies
	game = eliminate_dominated_strategies(np.array(states))

	dist = calculate_dist_and_utility(game)
	distributions[triple] = dist
	return dist


def represents_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def calculate_what_to_play(left, right, position):
	((dist, dist_ind), g) = solve(left, right, position)
	if DEBUG:
		start = time.time()
		print("--- %s seconds ---" % (time.time() - start))

	dist = np.array(dist)
	dist /= dist.sum()
	if DEBUG:
		print("Distribution:", list(dist), dist_ind)
		print("Utility: ", g)
	X = np.random.choice(dist_ind, 1, p=dist)
	return int(X[0])


def save_object(obj, filename):
	with open(filename, 'wb') as output:  # overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_dist(num):
	return load_object("field" + str(num) + "/distributions.pkl")


def load_object(filename):
	with open(filename, 'rb') as input:
		return pickle.load(input)


def export_to_pickle():
	if not os.path.exists("field" + str(SIZE)):
		os.makedirs("field" + str(SIZE))
	save_object({}, "field" + str(SIZE) + "/distributions.pkl")
	save_object({}, "field" + str(SIZE) + "/utilities.pkl")
	global SEEN
	global distributions
	print("size:", SIZE)
	SEEN = load_object("field" + str(SIZE) + "/utilities.pkl")
	distributions = load_object("field" + str(SIZE) + "/distributions.pkl")
	total = len(range(SIZE // 2, -1 * SIZE // 2 - 1, -1)) * 50 * 50
	with tqdm(total=total) as progress:  # type: tqdm
		for t in range(SIZE // 2, -1 * SIZE // 2 - 1, -1):
			for x in range(1, 51):
				for y in range(1, x + 1):
					solve(x, y, t)
				progress.update(x)
			for x in range(1, 51):
				for y in range(x + 1, 51):
					solve(x, y, t)
				progress.update(50-x)
	save_object(SEEN, "field" + str(SIZE) + "/utilities.pkl")
	save_object(distributions, "field" + str(SIZE) + "/distributions.pkl")


if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-s", "--size", dest="size", help="number of fields between the castles", metavar="SIZE")
	parser.add_option("-p", "--pickle", action="store_true", dest="pickle", help="create pickles", metavar="PICKLE")
	(options, args) = parser.parse_args()
	if options.size is not None:
		SIZE = int(options.size)
	if options.pickle is not None:
		export_to_pickle()
	elif len(args) == 3:
		try:
			start_time = time.time()
			((distribution, distribution_ind), g) = solve(int(args[0]), int(args[1]), int(args[2]))
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
		print("Usage: Python3 strategy_nash.py -s <size> <x y t>")
