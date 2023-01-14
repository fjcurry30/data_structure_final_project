"""

其中定义了一个类 Node 来存储一个点及其左右子节点，
并定义了一个类 KDTree 以使用提供的点列表创建 k-d 树。 
KDTree 类构造函数使用递归函数 build_kdtree() 来创建 k-d 树。 
该函数根据当前深度选择一个轴来分割点，并根据该轴对点进行排序，并选择中间点作为轴心。 
然后它用枢轴点创建一个新节点，并递归地分别为小于和大于枢轴的点创建左子树和右子树。

"""
import math

class Node:
	def __init__(self, point, left=None, right=None):
		self.point = point
		self.left = left
		self.right = right

class KDTree:
	def __init__(self, points):
		def build_kdtree(point_list, depth):
			if len(point_list) < 1:
				return None

			# 根据深度选择坐标轴，使坐标轴循环遍历所有有效值
			k = len(point_list[0])
			axis = depth%k

			# 排序点列表并选择中位数作为轴心点
			# 减少时间复杂度
			
			point_list.sort(key=lambda point: point[axis])
			
			median = len(point_list) // 2
			# Create node and construct subtrees
			return Node(point_list[median],	
						build_kdtree(point_list[:median], depth + 1),
						build_kdtree(point_list[median + 1:], depth + 1))
		self.root = build_kdtree(points, 0)

	def insert(self, point):
		"""
		定义一个insert_help递归函数,它将在td树中找到新的正确的位置

		insert() 函数的时间复杂度平均为 O(log(n))，最坏情况下为 O(n)。
		遍历 k-d 树并找到新点的正确位置。 时间复杂度平均为 n 的对数，因为我们遍历的是平衡二叉树。
		但是，如果树不平衡，最坏情况下的时间复杂度可能为 O(n)
		"""
		def insert_help(node, point, depth=0):
			if not node:
				return Node(point)

			k = len(point)
			axis = depth % k

			if point[axis] < node.point[axis]:
				node.left = insert_help(node.left, point, depth+1)
			else:
				node.right = insert_help(node.right, point, depth+1)

			return node
		self.root = insert_help(self.root, point)

	def range(self, low, high):
		"""
		定义一个range_help递归函数,通过比较点的坐标与范围的
		下限和上限来搜索包含查询范围的子树。

		range的时间复杂度平均为O(log(n)*k),其中n为k-d树的点数,k为维数。 
		这是因为我们需要遍历树，时间复杂度是对数的
		"""
		def range_help(node, low, high, depth=0):
			if not node:
				return []

			# print(low)
			k = len(low)
			axis = depth % k

			if all(low[i] <= node.point[i] <= high[i] for i in range(k)):
				result.append(node.point)

			if low[axis] < node.point[axis]:
				range_help(node.left, low, high, depth+1)

			if high[axis] > node.point[axis]:
				range_help(node.right, low, high, depth+1)

		result = []
		range_help(self.root, low, high)
		return result

	def distance(self, point1, point2):
		return math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in \
			zip(point1, point2)))

	def nearest_neighbor(self, point):
		def nearest_neighbor_help(node, point, best=None,\
			best_distance=None, depth=0):

			if not node:
				return best, best_distance

			k = len(point)
			axis = depth % k
			near_subtree = None
			far_subtree = None

			if point[axis] < node.point[axis]:
				near_subtree = node.left
				far_subtree = node.right
			else:
				near_subtree = node.right
				far_subtree = node.left

			current_distance = self.distance(point, node.point)

			if best is None or current_distance < best_distance:
				bese = node.point
				best_distance = current_distance

			near_best, near_best_distance = nearest_neighbor_help( \
					near_subtree, point, best, best_distance, depth + 1)

			if far_subtree is not None and (near_best is None or \
					abs(point[axis] - node.point[axis]) < near_best_distance):

				far_best, far_best_distance = nearest_neighbor_help( \
            		far_subtree, point, best, best_distance, depth + 1)
				if far_best is not None and (near_best is None or \
	            		far_best_distance < near_best_distance):
					near_best, near_best_distance = far_best, far_best_distance

			return near_best, near_best_distance
		return nearest_neighbor_help(self.root, point)

def main():
	points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
	kd_tree = KDTree(points)
	kd_tree.insert((3, 7))
	print(kd_tree.range([1,2], [8,8]))
	print(kd_tree.nearest_neighbor((2,3)))
	



