import random
from main import KDTree
from matplotlib import pyplot as plt
import time

if __name__ == "__main__":
	kd_tree_time = []
	naive_time = []
	num_points = []

	for n in range(100, 10000, 100):
		points = []
		for i in range(n):
			points.append((random.randint(1, 10000), \
				random.randint(1, 10000)))
		kd_tree = KDTree(points)

		start = time.time()
		kd_tree.range((100, 100), (9000, 9000))
		end = time.time()
		kd_tree_time.append(end-start)

		start = time.time()
		result = [point for point in points if \
				100 <= point[0] <= 9000 and 100 <= point[1] <= 9000]
		end = time.time()
		naive_time.append(end-start)

		num_points.append(n)

	# plot
	plt.plot(num_points, kd_tree_time, label="K-D Tree")
	plt.plot(num_points, naive_time, label="Naive")
	plt.xlabel("Number of Points")
	plt.ylabel("Time (s)")
	plt.legend()
	plt.show()


