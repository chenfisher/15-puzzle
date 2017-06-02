import numpy as np
from search import a_star_search

class State(object):
	def __init__(self, array, empty_spot):
		self.array = array
		self.empty_spot = empty_spot

	def move(self, new_empty_spot):
		array = np.array(self.array)
		array[self.empty_spot] = array[new_empty_spot]
		return State(array, new_empty_spot)

	def __str__(self):
		return str(self.array) + ", " + str(self.empty_spot)

class GameGraph(object):
	def __init__(self, dim):
		self._dim = dim
		self._dim_squared = dim * dim
		self._goal_state_array = np.add(np.arange(self._dim_squared), 1)
		self._neighbors = tuple([self._calc_neighbors(x) for x in range(self._dim_squared)])

	def neighbors(self, state):
		spots = self._neighbors[state.empty_spot]
		return [state.move(s) for s in spots]
	
	def is_goal(self, state):
		return state.empty_spot == self._dim_squared-1 and np.all(state.array[:-1] == self._goal_state_array[:-1])

	def cost(self, current_state, next_state):
		return 1

	def heuristic(self, state):
		return sum(self._single_dist(n, i) for i, n in enumerate(state.array))

	def _calc_neighbors(self, n):
		i, j = self._num2ij(n)
		potential_neighbors = ((i-1,j),(i,j-1),(i,j+1),(i+1,j))
		return tuple([x*self._dim + y for x ,y in potential_neighbors if x>=0 and y>=0 and x<self._dim and y<self._dim])

	def _num2ij(self, n):
		i = n / self._dim
		j = n % self._dim
		return i, j

	def _single_dist(self, num, index):
		goal_i, goal_j = self._num2ij(num-1)
		i, j = self._num2ij(index)
		return abs(i - goal_i) + abs(j - goal_j)


class Solver(object):
	def __init__(self, dim):
		self._graph = GameGraph(dim)

	def solve(self, start_state):
		return a_star_search(self._graph, start_state)


def main():
	graph = GameGraph(4)
	print graph._calc_neighbors(0)
	print graph._calc_neighbors(1)
	print graph._calc_neighbors(2)
	print graph._calc_neighbors(5)


main()
