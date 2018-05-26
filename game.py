import Troll
import strategy_nash as strategy


def strategy_demo(game, previous_parties):
	number_of_stones = game.stockGauche
	return min(2, number_of_stones)


def strategy_of_nash(game, previous_parties):
	troll_position = game.positionTroll - (game.nombreCases - 1) / 2
	stones_left = game.stockGauche
	stones_right = game.stockDroite
	return strategy.calculate_what_to_play(stones_left, stones_right, troll_position)


if __name__ == "__main__":
	# party = Troll.Partie(7, 15)
	# print(party)
	Troll.jouerPartie(7, 15, strategy_of_nash, strategy_demo)
	# print(strategy_of_nash(party, None))
