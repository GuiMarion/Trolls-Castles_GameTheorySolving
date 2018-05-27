import Troll
import create_database as db
import numpy as np

distributions = {}


def strategy_demo(game, previous_parties):
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


if __name__ == "__main__":
	# party = Troll.Partie(7, 15)
	# print(party)
	# Troll.jouerPartie(15, 50, strategy_of_nash, strategy_demo)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_demo)
	distributions = db.load_dist(7)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_demo)
	Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_demo)
# print(strategy_of_nash(party, None))
