def rem(Tab, k):
	for i in range(len(Tab)):
		if Tab[i] == k :
			del Tab[i]
			return Tab

def Strategy(Tab):
	DEBUG = True
	L1 = list(range(len(Tab)))

	strategy = 0
	while strategy < len(Tab):
		indice = 0
		while indice <len(Tab):
			value = 0

			if indice == strategy:
				indice += 1
				value = 0

			if indice == len(Tab):
				return L1

			while value <len(Tab[0]):
				if Tab[strategy][value] > Tab[indice][value]:
					# Strategy is NOT dominated by indice
					indice += 1
					value = len(Tab[0]) +1
					break
				value += 1

			if value != len(Tab[0]) +1:
			# Strategy is dominated by indice
				if DEBUG:
					print(strategy, "<", indice)
				L1 = rem(L1, strategy)
				#indice = 0
				break

		strategy += 1

	return L1


print(Strategy([[10],
				[2],
				[2],
				[4],
				[4]]))
