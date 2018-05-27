import Troll
import create_database as db
import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
	Plot, Figure, Matrix, Alignat, Package
from pylatex.utils import italic
from pylatex.base_classes import Environment
import os

distributions = {}


class Minted(Environment):
	"""A class to wrap LaTeX's alltt environment."""

	packages = [Package('minted')]
	escape = False
	content_separator = "\n"


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
		stones_to_throw = min(np.random.normal(game.stockGauche // 2, 3), game.stockGauche)
	return int(max(stones_to_throw, 1))


# wins 25% of the time against 'nash'-one and 50% tie
def strategy_nash_eager(game, previous_parties):
	troll_position = int(game.positionTroll - (game.nombreCases - 1) // 2)
	stones_left = game.stockGauche
	stones_right = game.stockDroite
	((distribution, distribution_ind), g) = distributions[stones_left, stones_right, troll_position]
	return int(np.array(distribution).argmax() + 1)


if __name__ == "__main__":
	# party = Troll.Partie(7, 15)
	# print(party)
	distributions = db.load_dist(7)
	# 7 - 15 single
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_demo)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_random)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_gaussian)
	# Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_random)
	# Troll.jouerPartie(7, 15, strategy_of_nash, strategy_demo)
	# Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_always_throw_two)
	# 	Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_gaussian)
	# results = Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_nash_eager)
	# print(results.gagnant)
	# print(strategy_of_nash(party, None))
	geometry_options = {"tmargin": "1cm", "lmargin": "2cm"}
	doc = Document(geometry_options=geometry_options)
	doc.packages.append(Package('minted'))

	with doc.create(Section('Game type #1 - number of fields: 7')):
		doc.append('Some regular text and some')
		doc.append(italic('italic text. '))
		doc.append('\nAlso some crazy characters: $&#{}')
		with doc.create(Subsection('Strategy of nash VS random number of stones')):
			doc.append(Troll.jouerPlusieursParties(7, 15, strategy_of_nash, strategy_random))
		with doc.create(Minted()):
			doc.append("""def strategy_random(game, previous_parties):
	number_of_stones_of_enemy = min(game.stockGauche, game.stockDroite + 1)
	return int(np.random.choice(range(1, number_of_stones_of_enemy + 1)))""")

		with doc.create(Subsection('Strategy nash')):
			with doc.create(Tabular('rc|cl')) as table:
				table.add_hline()
				table.add_row((1, 2, 3, 4))
				table.add_hline(1, 2)
				table.add_empty_row()
				table.add_row((4, 5, 6, 7))

	a = np.array([[100, 10, 20]]).T
	M = np.matrix([[2, 3, 4],
								 [0, 0, 1],
								 [0, 0, 2]])

	with doc.create(Section('Field 15')):
		with doc.create(Subsection('Correct matrix equations')):
			doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))

		with doc.create(Subsection('Alignat math environment')):
			with doc.create(Alignat(numbering=False, escape=False)) as agn:
				agn.append(r'\frac{a}{b} &= 0 \\')
				agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])

		with doc.create(Subsection('Beautiful graphs')):
			with doc.create(TikZ()):
				plot_options = 'height=4cm, width=6cm, grid=major'
				with doc.create(Axis(options=plot_options)) as plot:
					plot.append(Plot(name='model', func='-x^5 - 242'))

					coordinates = [
						(-4.77778, 2027.60977),
						(-3.55556, 347.84069),
						(-2.33333, 22.58953),
						(-1.11111, -493.50066),
						(0.11111, 46.66082),
						(1.33333, -205.56286),
						(2.55556, -341.40638),
						(3.77778, -1169.24780),
						(5.00000, -3269.56775),
					]

					plot.append(Plot(name='estimate', coordinates=coordinates))

		with doc.create(Subsection('Cute kitten pictures')):
			with doc.create(Figure(position='h!')) as kitten_pic:
				# kitten_pic.add_image(image_filename, width='120px')
				kitten_pic.add_caption('Look it\'s on its back')

	doc.generate_pdf('report/report', clean_tex=False)
