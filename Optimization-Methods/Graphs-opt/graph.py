from math import inf
from exceptions import GraphException

# imports for graph display
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from copy import deepcopy
import sys


class OrientedGraph:
    adjacency_matrix = []

    def __init__(self, matrix):
        """
        :param matrix: adjacency matrix, infinity means that there is no edge
        """
        self.adjacency_matrix = matrix

    def __has_vertex_loops(self):
        """
        Checking for loops at the vertexes of the graph.

        :return: True - loops, False - no loops
        """
        for i in range(len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][i] != 0:  # m.b. != inf
                return True
        return False

    def __has_negative_edges(self):
        """
        Checks for the presence of negative weights on the edges of the graph.
        :return: True - negative, False - non negative
        """
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] < 0:
                    return True
        return False

    def __get_related_vertexes(self, vertex):
        """
        Gives a list of connected vertices (one edge)
        :param vertex: The vertex for which we are looking for connected
        :return: List of connected vertices
        """
        res = []
        for i in range(len(self.adjacency_matrix[vertex])):
            if i != vertex and self.adjacency_matrix[vertex][i] != inf:
                res.append(i)
        return res

    def __get_all_reachable__vertexes(self, visited=None, curr_v=0):
        """
        Recursively finds all vertexes that can be visited from the given one.
        :param visited: The set of visited vertexes. Use None.
        :param curr_v: The vertex from which the search begins.
        :return: The set of visited vertexes
        """
        if visited is None:
            visited = set()
        for v in self.__get_related_vertexes(curr_v):
            if v not in visited:
                visited.add(v)
                self.__get_all_reachable__vertexes(visited, v)
        return visited

    def __is_connected(self):
        """
        Checking that it is possible to go from the zero vertex to any next one
        :return: True - possible, False - not possible.
        """
        try:
            visited_set = self.__get_all_reachable__vertexes(curr_v=0)
            for v in range(1, len(self.adjacency_matrix)):
                if v not in visited_set:
                    return False
        except RecursionError:
            raise GraphException("Vertex recursion is broken :/")
        return True

    @staticmethod
    def __additive_criterion(w_crit, weight_edge):
        return w_crit + weight_edge

    @staticmethod
    def __maximum_criterion(w_crit, weight_edge):
        return max(w_crit, weight_edge)

    def __path_from_opt_edges(self, vertex_start, vertex_finish, opt_edges):
        """
        Get opt path
        :param vertex_start: v1
        :param vertex_finish: v2
        :param opt_edges: id - vertex 1, value - vertex 2 (like g*)
        :return: opt path from vertex_start to vertex_finish
        """
        max_iter_count = len(self.adjacency_matrix) * (len(self.adjacency_matrix) - 1) / 2
        iter_counter = 0
        tmp_vertex = vertex_finish
        path = [tmp_vertex]
        while tmp_vertex != vertex_start:
            tmp_vertex = opt_edges[tmp_vertex]
            path.append(tmp_vertex)
            iter_counter += 1
            if iter_counter > max_iter_count:
                path = []
                w_path = inf
                break
        return path[::-1]  # reverse because we started from the end

    def dijkstra(self, vertex_start, vertex_finish, criterion):
        """
        Dijkstra's algorithm for finding the optimal path.
        :param vertex_start: Xs
        :param vertex_finish: Xf
        :param criterion: 'add' or 'max'
        :return: ([optimal path], criteria_value)
        """
        if self.__has_vertex_loops():
            raise GraphException("The graph has vertex loops")
        if self.__has_negative_edges():
            raise GraphException("The graph has negative edges")
        if not self.__is_connected():
            raise GraphException("The graph is not connected (by directions)")
        visited_vertexes = set()
        labels = [inf for _ in range(len(self.adjacency_matrix))]
        curr_v = vertex_start
        labels[curr_v] = 0
        visited_vertexes.add(curr_v)
        opt_edges = [0 for _ in range(len(self.adjacency_matrix))]  # id - vertex 1, value - vertex 2 (like g*)
        stop = False
        while not stop:
            for v_related in self.__get_related_vertexes(curr_v):
                if v_related not in visited_vertexes:
                    w_criterion = 0
                    if criterion == 'add':
                        w_criterion = self.__additive_criterion(labels[curr_v],
                                                                self.adjacency_matrix[curr_v][v_related])
                    elif criterion == 'max':
                        w_criterion = self.__maximum_criterion(labels[curr_v], self.adjacency_matrix[curr_v][v_related])
                    else:
                        raise GraphException("Unknown criterion. Use 'add' or 'max'")

                    if w_criterion < labels[v_related]:
                        labels[v_related] = w_criterion
                        opt_edges[v_related] = curr_v

            min_label = inf
            min_vertex = -inf
            for i in range(len(labels)):
                if labels[i] < min_label and i not in visited_vertexes:
                    min_label = labels[i]
                    min_vertex = i
            curr_v = min_vertex
            if curr_v != -inf:
                visited_vertexes.add(curr_v)
            else:
                stop = True

        w_path = labels[vertex_finish]  # final criterion
        path = self.__path_from_opt_edges(vertex_start, vertex_finish, opt_edges)
        return path, w_path

    def bellman(self, vertex_start, vertex_finish, criterion):
        """
        Bellman's algorithm for finding the optimal path.
        :param vertex_start: Xs
        :param vertex_finish: Xf
        :param criterion: 'add' or 'max'
        :return: ([optimal path], criteria_value)
        """
        if self.__has_vertex_loops():
            raise GraphException("The graph has vertex loops")
        if not self.__is_connected():
            raise GraphException("The graph is not connected (by directions)")
        labels = [inf for _ in range(len(self.adjacency_matrix))]
        labels[vertex_start] = 0
        vertexes_k_steps = set()
        vertexes_k_steps.add(vertex_start)
        opt_edges = [0 for _ in range(len(self.adjacency_matrix))]  # id - vertex 1, value - vertex 2 (like g*)
        iter_counter = 0
        max_iter_count = len(self.adjacency_matrix) * (len(self.adjacency_matrix) - 1) / 2
        while len(vertexes_k_steps) != 0 and iter_counter < max_iter_count + 1:
            iter_counter += 1
            next_vertexes_k_steps = set()
            for v_k in vertexes_k_steps:
                vertexes_k_plus_1_steps = set(self.__get_related_vertexes(v_k))
                next_vertexes_k_steps = next_vertexes_k_steps.union(vertexes_k_plus_1_steps)
                for v_k_plus_1 in vertexes_k_plus_1_steps:
                    w_criterion = 0
                    if criterion == 'add':
                        w_criterion = self.__additive_criterion(labels[v_k], self.adjacency_matrix[v_k][v_k_plus_1])
                    elif criterion == 'max':
                        w_criterion = self.__maximum_criterion(labels[v_k], self.adjacency_matrix[v_k][v_k_plus_1])
                    else:
                        raise GraphException("Unknown criterion. Use 'add' or 'max'")
                    if w_criterion < labels[v_k_plus_1]:
                        labels[v_k_plus_1] = w_criterion
                        opt_edges[v_k_plus_1] = v_k
            vertexes_k_steps = next_vertexes_k_steps

        w_path = labels[vertex_finish]  # final criterion
        path = self.__path_from_opt_edges(vertex_start, vertex_finish, opt_edges)
        return path, w_path

    # can't correctly show zero weight
    def show(self, show_weights=False):
        """
        Show graph
        :param show_weights: True or False
        :return: None
        """
        tmp = deepcopy(self.adjacency_matrix)
        for x in range(len(tmp)):
            for y in range(len(tmp[x])):
                if tmp[x][y] == 0 and x != y:
                    tmp[x][y] = sys.float_info.epsilon
                elif tmp[x][y] == inf:
                    tmp[x][y] = 0
        tmp = np.array(tmp)
        G = nx.from_numpy_matrix(np.matrix(tmp), create_using=nx.DiGraph)
        layout = nx.spring_layout(G)
        nx.draw(G, layout)
        if show_weights:
            nx.draw_networkx_edge_labels(G, pos=layout)
        labels = {}
        for idx, node in enumerate(G.nodes()):
            labels[node] = idx
        nx.draw_networkx_labels(G, pos=layout, labels=labels)
        plt.show()

    def print_edge(self, vertex1, vertex2):
        """
        Print edge with weight and vertexes
        :param vertex1: v1
        :param vertex2: v2
        :return: None
        """
        print(f'({vertex1}) ---{self.adjacency_matrix[vertex1][vertex2]}--> ({vertex2})')

    def print_path(self, path):
        """
        Print path with weights and vertexes
        :param path: [path]
        :return: None
        """
        if len(path) < 1:
            print('The path between these vertexes does not exist')
            return
        s = ''
        for i in range(len(path) - 1):
            s += f'({path[i]}) --{self.adjacency_matrix[path[i]][path[i + 1]]}-> '
        s += f'({path[len(path) - 1]})'
        print(s)
