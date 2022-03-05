# Python 3.9.6
from math import inf
from graph import OrientedGraph

"""
Граф хранится в виде матрицы смежности.
Чтобы убрать отображение графа и решить таким образом проблемы с зависимостями нужно
убрать импорты для построения и метод show в файле graph.py, убрать вызов G.show() в main.py
"""

# my task
M = [
    [0, 2, 4, 3, inf, inf, inf, inf, inf, inf, inf],
    [inf, 0, inf, inf, 6, 2, inf, inf, inf, inf, inf],
    [inf, inf, 0, inf, 5, 7, 3, inf, inf, inf, inf],
    [inf, inf, inf, 0, inf, 2, 2, inf, inf, inf, inf],
    [inf, inf, inf, inf, 0, inf, inf, 8, 4, inf, inf],
    [inf, inf, inf, inf, inf, 0, inf, 8, 3, 9, inf],
    [inf, inf, inf, inf, inf, inf, 0, inf, 4, 5, inf],
    [inf, inf, inf, inf, inf, inf, inf, 0, inf, inf, 9],
    [inf, inf, inf, inf, inf, inf, inf, inf, 0, inf, 6],
    [inf, inf, inf, inf, inf, inf, inf, inf, inf, 0, 4],
    [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 0]
]


G = OrientedGraph(M)
start = 0
finish = len(G.adjacency_matrix) - 1
print('Dijkstra')
path, W = G.dijkstra(vertex_start=start, vertex_finish=finish, criterion='add')
G.print_path(path)
print(f'W = {W}')

print('\nBellman')
path, W = G.bellman(vertex_start=start, vertex_finish=finish, criterion='add')
G.print_path(path)
print(f'W = {W}')

G.show(show_weights=False)
