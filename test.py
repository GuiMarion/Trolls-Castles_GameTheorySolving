def insertNonNp(tab):
	L = []
	L.append(list(range(len(tab[0]) +1 )))
	for i in range(len(tab)):
		L.append([i+1])

	for i in range(len(tab)):
		for e in range(len(tab[i])):
			L[i+1].append(tab[i][e])

	return L

print(insertNonNp([[0],[0]]))

print([[0, 1], [1, 0], [2, 0]])

print(insertNonNp([[ 0.,  0.], [ 0.,  0.], [-1.,  0.]]))

print([[ 0.,  1.,  2.], [ 1.,  0.,  0.], [ 2.,  0.,  0.], [ 3., -1.,  0.]])


print(insertNonNp([[ 0], [ 0], [-1]]))

print([[ 0,  1], [ 1,  0], [ 2,  0], [ 3, -1]])


print(insertNonNp([[ 0.,  0.,  1.], [ 0.,  0.,  0.], [-1.,  0.,  0.], [-1., -1.,  0.]]))

print([[ 0.,  1.,  2.,  3.], [ 1.,  0.,  0.,  1.], [ 2.,  0.,  0.,  0.], [ 3., -1.,  0.,  0.], [ 4., -1., -1.,  0.]])

