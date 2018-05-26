import strategy_nash as strategy
import pickle


def save_object(obj, filename):
	with open(filename, 'wb') as output:  # overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
	with open(filename, 'rb') as input:
		return pickle.load(input)


def load_dist(num):
	return load_object("field" + str(num) + "/distributions.pkl")


if __name__ == "__main__":
	# save_object({}, "distributions.pkl")
	# save_object({}, "utilities.pkl")
	util = load_object("utilities.pkl")
	dist = load_object("distributions.pkl")
	print("#util: ", len(util))
	print("#dist: ", len(dist))
	print(util)
	print(dist[50, 50, 0])
	# for t in range(7, -8, -1):
	# 	for x in range(1, 51):
	# 		for y in range(1, 51):
	# 			if (x, y, t) not in dist:
	# 				print("not found: ", (x, y, t))

# print(load_object("utilities.pkl"))
# print(load_object("distributions.pkl"))
# print(load_object("test_save.pkl"))
