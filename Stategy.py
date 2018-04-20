def rem(Tab, k):
	for i in range(len(Tab)):
		if Tab[i] == k :
			del Tab[i]
			return Tab

def Strategy(Tab):
	L1 = list(range(len(Tab)))

	strategy = 0
	while strategy < len(Tab):
		indice = 0
		while indice <len(Tab):
			value = 0

			if indice == strategy:
				indice += 1
				value = 0

			while value <len(Tab[0]):

				if Tab[strategy][value] > Tab[indice][value]:
					# Strategy is NOT dominated by indice
					indice += 1
					value = 0
					break
				value += 1

			# Strategy is dominated by indice
			print(strategy, "<", indice)
			L1 = rem(L1, strategy)
			strategy += 1
			indice += 1
			break

		strategy += 1

	return L1


print(Strategy([[1, 2, 1, 4],
				[2, 1, 1, 2],
				[2, 4, 1, 5],
				[1, 2, 1, 3],
				[-1, -1, 0, 3]]))
