# coding: utf-8
import numpy as np
import logging

DEBUG = True

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
	tab = np.insert(tab, 0, range(tab.shape[0]), axis=1)
	tab = np.insert(tab, 0, range(-1, tab.shape[1] - 1), axis=0)
	while tab.size is not old_size:
		old_size = tab.size
		tab = eliminate_strategies_in(tab).transpose()
		tab = eliminate_strategies_in(tab).transpose()
	return tab


def eliminate_strategies_in(tab):
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
				if tab[strategy_index][enemy_strategy_index] > tab[other_strategy_index][enemy_strategy_index]:
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


test1 = [[7, 2, 3], [2, 3, 4], [5, 6, 7]]
test2 = [[1, 2, 3], [2, 3, 4], [5, 6, 7]]
test_random = np.random.randint(-1, 6, size=(10, 13))

test_other = [[5, 1, 4, 1, - 1, 0, 5, 1, 51, 2, - 1, 2, 2],
							[2, 2, 4, 1, 0, 4, 4, 5, 1, 43, 2, 5, 3],
							[-1, 4, 2, 0, - 1, 2, 3, 1, 34, 2, 3, 3, 5],
							[2, 11, 23, 3, 2, 33, 23, 23, 53, 2, 5, 23, 23],
							[2, 1, 5, 2, 5, 4, 4, 4, 2, 1, 27, 2, 3],
							[2, - 1, 5, 5, - 1, 4, 4, 1, 0, 27, 4, 5, 2],
							[2, - 1, 1, 4, - 1, 0, 2, 5, 24, - 1, 0, 3, - 1],
							[5, 0, 0, - 1, 1, 5, 5, 0, 3, 34, 5, 4, 3],
							[0, 3, 5, 0, 4, 1, 4, - 1, 4, 38, 3, 4, 1],
							[5, 2, 4, 3, 3, 1, 2, 4, 3, 1, 35, 34, 2]]

# print(get_not_dominated_strategies(np.array(test1)))
# print(get_not_dominated_strategies(np.array(test2)))
# print(get_not_dominated_strategies(np.array(test_random)))
print(eliminate_dominated_strategies(np.array(test_other)))
