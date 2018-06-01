import Troll
import game as game

from pylatex import Document, Section, Subsection


if __name__ == "__main__":
	geometry_options = {"tmargin": "1cm", "lmargin": "2cm"}
	doc = Document(geometry_options=geometry_options)

	with doc.create(Section('Number of fields: 7, stones: 15')):
		with doc.create(Subsection('Strategy of nash VS random number of stones')):
			doc.append(Troll.jouerPlusieursParties(7, 15, game.get_strategy_nash(7), game.strategy_random))
		with doc.create(Subsection('Strategy of nash VS eager version of strategy of nash')):
			doc.append(Troll.jouerPlusieursParties(7, 15, game.get_strategy_nash(7), game.get_strategy_nash_eager(7)))
		with doc.create(Subsection('Strategy of nash VS gaussian with location of 2 and variance of 0.5')):
			doc.append(Troll.jouerPlusieursParties(7, 15, game.get_strategy_nash(7), game.strategy_gaussian))
		with doc.create(Subsection('Strategy of nash VS always throw two stones')):
			doc.append(Troll.jouerPlusieursParties(7, 15, game.get_strategy_nash(7), game.strategy_always_throw_two))
		with doc.create(Subsection('Nash equilibrium')):
			doc.append(Troll.jouerPlusieursParties(7, 15, game.get_strategy_nash(7), game.get_strategy_nash(7)))

	with doc.create(Section('Number of fields: 7, stones: 30')):
		with doc.create(Subsection('Strategy of nash VS random number of stones')):
			doc.append(Troll.jouerPlusieursParties(7, 30, game.get_strategy_nash(7), game.strategy_random))
		with doc.create(Subsection('Strategy of nash VS eager version of strategy of nash')):
			doc.append(Troll.jouerPlusieursParties(7, 30, game.get_strategy_nash(7), game.get_strategy_nash_eager(7)))
		with doc.create(Subsection('Strategy of nash VS gaussian with location of 2 and variance of 0.5')):
			doc.append(Troll.jouerPlusieursParties(7, 30, game.get_strategy_nash(7), game.strategy_gaussian))
		with doc.create(Subsection('Strategy of nash VS always throw two stones')):
			doc.append(Troll.jouerPlusieursParties(7, 30, game.get_strategy_nash(7), game.strategy_always_throw_two))
		with doc.create(Subsection('Nash equilibrium')):
			doc.append(Troll.jouerPlusieursParties(7, 30, game.get_strategy_nash(7), game.get_strategy_nash_eager(7)))

	with doc.create(Section('Number of fields: 15, stones: 30')):
		with doc.create(Subsection('Strategy of nash VS random number of stones')):
			doc.append(Troll.jouerPlusieursParties(15, 30, game.get_strategy_nash(15), game.strategy_random))
		with doc.create(Subsection('Strategy of nash VS eager version of strategy of nash')):
			doc.append(Troll.jouerPlusieursParties(15, 30, game.get_strategy_nash(15), game.get_strategy_nash_eager(15)))
		with doc.create(Subsection('Strategy of nash VS gaussian with location of 2 and variance of 0.5')):
			doc.append(Troll.jouerPlusieursParties(15, 30, game.get_strategy_nash(15), game.strategy_gaussian))
		with doc.create(Subsection('Strategy of nash VS always throw two stones')):
			doc.append(Troll.jouerPlusieursParties(15, 30, game.get_strategy_nash(15), game.strategy_always_throw_two))
		with doc.create(Subsection('Nash equilibrium')):
			doc.append(Troll.jouerPlusieursParties(15, 30, game.get_strategy_nash(15), game.get_strategy_nash(15)))

	with doc.create(Section('Number of fields: 15, stones: 50')):
		with doc.create(Subsection('Strategy of nash VS random number of stones')):
			doc.append(Troll.jouerPlusieursParties(15, 50, game.get_strategy_nash(15), game.strategy_random))
		with doc.create(Subsection('Strategy of nash VS eager version of strategy of nash')):
			doc.append(Troll.jouerPlusieursParties(15, 50, game.get_strategy_nash(15), game.get_strategy_nash_eager(15)))
		with doc.create(Subsection('Strategy of nash VS gaussian with location of 2 and variance of 0.5')):
			doc.append(Troll.jouerPlusieursParties(15, 50, game.get_strategy_nash(15), game.strategy_gaussian))
		with doc.create(Subsection('Strategy of nash VS always throw two stones')):
			doc.append(Troll.jouerPlusieursParties(15, 50, game.get_strategy_nash(15), game.strategy_always_throw_two))
		with doc.create(Subsection('Nash equilibrium')):
			doc.append(Troll.jouerPlusieursParties(15, 50, game.get_strategy_nash(15), game.get_strategy_nash(15)))

	doc.generate_pdf('report', clean_tex=False)
