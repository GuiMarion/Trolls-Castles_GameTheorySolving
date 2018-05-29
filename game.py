import Troll
import strategy_nash as db
import numpy as np

distributions = {}


def strategy_always_throw_two(game, previous_parties):
	number_of_stones = game.stockGauche
	return min(2, number_of_stones)


def strategy_of_nash(game, previous_parties):
	troll_position = int(game.positionTroll - (game.nombreCases - 1) // 2)
	stones_left = game.stockGauche
	stones_right = game.stockDroite
	((distribution, distribution_ind), g) = distributions[stones_left, stones_right, troll_position]
	distribution = np.array(distribution)
	distribution /= distribution.sum()
	X = np.random.choice(distribution_ind, 1, p=distribution)
	return int(X[0])


def strategy_random(game, previous_parties):
	number_of_stones_of_enemy = min(game.stockGauche, game.stockDroite + 1)
	return int(np.random.choice(range(1, number_of_stones_of_enemy + 1)))


# wins 20% of the time against 'nash'-one
def strategy_gaussian(game, previous_parties):
	stones_to_throw = np.random.normal(2, 0.5)
	if stones_to_throw > game.stockGauche:
		stones_to_throw = min(np.random.normal(game.stockGauche//2, 3), game.stockGauche)
	return int(max(stones_to_throw, 1))


# wins 25% of the time against 'nash'-one and 50% tie
def strategy_nash_eager(game, previous_parties):
	troll_position = int(game.positionTroll - (game.nombreCases - 1) // 2)
	stones_left = game.stockGauche
	stones_right = game.stockDroite
	((distribution, distribution_ind), g) = distributions[stones_left, stones_right, troll_position]
	return int(np.array(distribution).argmax() + 1)


if __name__ == "__main__":
	distributions = db.load_dist(7)
	# 7 - 15 single
	#Troll.jouerPartie(7, 15, strategy_of_nash, strategy_random)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_always_throw_two)
	# # 7 - 15 multiple
	Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_random)
	Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_gaussian)
	Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_nash_eager)
	Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_always_throw_two)
	# # 7 - 30 single
	# Troll.jouerPartie(7, 30, strategy_of_nash, strategy_random)
	# Troll.jouerPartie(7, 30, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPartie(7, 30, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPartie(7, 30, strategy_of_nash, strategy_always_throw_two)
	# # 7 - 30 multiple
	# Troll.jouerPlusieursParties(7, 30, strategy_of_nash, strategy_random)
	# Troll.jouerPlusieursParties(7, 30, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPlusieursParties(7, 30, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPlusieursParties(7, 30, strategy_of_nash, strategy_always_throw_two)
	# # load strategy of game with 15 fields
	# distributions = db.load_dist(15)
	# # 15 - 30 single
	# Troll.jouerPartie(15, 30, strategy_of_nash, strategy_random)
	# Troll.jouerPartie(15, 30, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPartie(15, 30, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPartie(15, 30, strategy_of_nash, strategy_always_throw_two)
	# # 15 - 30 multiple
	# Troll.jouerPlusieursParties(15, 30, strategy_of_nash, strategy_random)
	# Troll.jouerPlusieursParties(15, 30, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPlusieursParties(15, 30, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPlusieursParties(15, 30, strategy_of_nash, strategy_always_throw_two)
	# # 15 - 50 single
	# Troll.jouerPartie(15, 50, strategy_of_nash, strategy_random)
	# Troll.jouerPartie(15, 50, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPartie(15, 50, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPartie(15, 50, strategy_of_nash, strategy_always_throw_two)
	# # 15 - 50 multiple
	# Troll.jouerPlusieursParties(15, 50, strategy_of_nash, strategy_random)
	# Troll.jouerPlusieursParties(15, 50, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPlusieursParties(15, 50, strategy_of_nash, strategy_nash_eager)
	# Troll.jouerPlusieursParties(15, 50, strategy_of_nash, strategy_always_throw_two)
