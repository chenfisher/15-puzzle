import numpy as np
import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


def a_star_iterative_deepening(graph, start, max_cost):
    for c in range(max_cost+1):
        print "ID depth = {}".format(c)
        result = a_star_search(graph, start, c)
        if result:
            return result
    return None, None


def a_star_search(graph, start, max_cost=np.inf):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        if graph.is_goal(current):
            break
        if cost_so_far[current] > max_cost:
            return None

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + graph.heuristic(next)
                frontier.put(next, priority)
                came_from[next] = current
    
    path = get_path(came_from, current)
    return cost_so_far[current], path


def get_path(came_from, current):
    path = [current]
    while True:
        prev = came_from[current]
        if not prev:
            break;
        path.insert(0, prev)
        current = prev
    return path

