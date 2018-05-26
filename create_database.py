import strategy_nash as strategy
import pickle


def save_object(obj, filename):
	with open(filename, 'wb') as output:  # overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
	with open(filename, 'rb') as input:
		return pickle.load(input)


if __name__ == "__main__":
	save_object({}, "distributions.pkl")
	save_object({}, "utilities.pkl")
	print(load_object("utilities.pkl"))
	print(load_object("distributions.pkl"))
	for t in range(7, -7, -1):
		for x in range(1, 50):
			for y in range(1, x + 1):
				strategy.solve(x, y, t)

	# print(load_object("utilities.pkl"))
	# print(load_object("distributions.pkl"))
# print(load_object("test_save.pkl"))
