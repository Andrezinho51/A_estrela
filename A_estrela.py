import copy 
from heapq import heappush, heappop

n = 3

linha = [ 1, 0, -1, 0 ]
coluna = [ 0, -1, 0, 1 ]

class priorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, k):
        heappush(self.heap, k)

    def pop(self):
        return heappop(self.heap)

    def empty(self):
        if not self.heap:
            return True
        else:
            return False

class node:
    def __init__(self, parent, mat, empty_tile_pos, cost, level, heuristic):
        self.parent = parent
        self.mat = mat
        self.empty_tile_pos = empty_tile_pos
        self.cost = cost
        self.level = level
        self.heuristic = heuristic

    def __lt__(self, nxt):
        return (self.cost + self.heuristic) < (nxt.cost + nxt.heuristic)

def calculateCost(mat, final) -> int:
    count = 0
    for i in range(n):
        for j in range(n):
            if ((mat[i][j]) and (mat[i][j] != final[i][j])):
                count += 1
    return count

def calculateHeuristic(mat, final) -> int:
    heuristic = 0
    for i in range(n):
        for j in range(n):
            if mat[i][j] != 0:
                x, y = divmod(mat[i][j] - 1, n)
                heuristic += abs(x - i) + abs(y - j)
    return heuristic

def newNode(mat, empty_tile_pos, new_empty_tile_pos, level, parent, final) -> node:
    new_mat = copy.deepcopy(mat)
    x1 = empty_tile_pos[0]
    y1 = empty_tile_pos[1]
    x2 = new_empty_tile_pos[0]
    y2 = new_empty_tile_pos[1]
    new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1]
    cost = calculateCost(new_mat, final)
    heuristic = calculateHeuristic(new_mat, final)
    new_node = node(parent, new_mat, new_empty_tile_pos, cost, level, heuristic)
    return new_node

def printMatrix(mat):
    for i in range(n):
        for j in range(n):
            print("%d " % (mat[i][j]), end=" ")
        print()

def isSafe(x, y):
    return x >= 0 and x < n and y >= 0 and y < n

def printPath(root):
    if root == None:
        return
    printPath(root.parent)
    printMatrix(root.mat)
    print()

def solve(initial, empty_tile_pos, final):
    pq = priorityQueue()
    cost = calculateCost(initial, final)
    heuristic = calculateHeuristic(initial, final)
    root = node(None, initial, empty_tile_pos, cost, 0, heuristic)
    pq.push(root)
    while not pq.empty():
        minimum = pq.pop()
        if minimum.cost == 0:
            printPath(minimum)
            return
        for i in range(4):
            new_tile_pos = [
                minimum.empty_tile_pos[0] + linha[i],
                minimum.empty_tile_pos[1] + coluna[i], ]
            if isSafe(new_tile_pos[0], new_tile_pos[1]):
                child = newNode(minimum.mat, minimum.empty_tile_pos, new_tile_pos, minimum.level + 1, minimum, final)
                pq.push(child)

inicial = [ [ 2, 3, 6 ],
            [ 1, 5, 4 ],
            [ 7, 8, 0 ] ]

final = [ [ 1, 2, 3 ],
          [ 4, 5, 6 ],
          [ 7, 8, 0 ] ]

empty_tile_pos = [ 1, 2 ]
solve(inicial, empty_tile_pos, final)