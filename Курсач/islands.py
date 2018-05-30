import sys


class Solver:
    def __init__(self, width, height):
        self.w = int(width)
        self.h = int(height)
        self.str_map = [[None for _ in range(0, self.w)] for _ in range(0, self.h)]
        self.count_of_islands = (self.w // 2 + 1) * (self.h // 2 + 1)
        self.islands = [0 for _ in range(self.count_of_islands)]
        self.bridges = [[0 for _ in range(len(self.islands))] for _ in range(len(self.islands))]
        self.answer = True
        self.solve()

    def solve(self):
        self.read_str_map()
        if (self.w % 2 == 0) or (self.h % 2 == 0):
            self.answer = False
        else:
            self.create_map_of_world()
        if self.answer:
            self.check_neighbourhood()
        try:
            if self.answer:
                self.check_connectivity()
        except Exception:
            pass
        if self.answer:
            self.find_bridges(0, [0 for _ in range(self.count_of_islands)])
        if self.answer:
            print("Island world")
        else:
            print("Just a picture")

    def read_str_map(self):
        for k in range(self.h):
            row = input()
            if len(row) != self.w:
                self.answer = False
                continue
            else:
                for j in range(self.w):
                    self.str_map[k][j] = row[j]

    def create_map_of_world(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.answer:
                    token = self.str_map[i][j]
                    if i % 2 == 0:
                        if j % 2 == 0:
                            if token != "O":
                                self.answer = False
                        else:
                            if token != " " and token != "-":
                                self.answer = False
                            elif token == "-":
                                first = (self.w // 2 + 1) * i // 2 + (j - 1) // 2
                                second = (self.w // 2 + 1) * i // 2 + (j + 2) // 2
                                self.create_bridge(first, second)
                    else:
                        if j % 2 == 0:
                            if token != " " and token != "|":
                                self.answer = False
                            elif token == "|":
                                first = (self.w // 2 + 1) * (i - 1) // 2 + j // 2
                                second = (self.w // 2 + 1) * (i + 1) // 2 + j // 2
                                self.create_bridge(first, second)
                        else:
                            if token == "/":
                                first = (self.w // 2 + 1) * (i - 1) // 2 + (j + 1) // 2
                                second = (self.w // 2 + 1) * (i + 1) // 2 + (j - 1) // 2
                                self.create_bridge(first, second)
                            elif token == "\\":
                                first = (self.w // 2 + 1) * (i - 1) // 2 + (j - 1) // 2
                                second = (self.w // 2 + 1) * (i + 1) // 2 + (j + 1) // 2
                                self.create_bridge(first, second)
                            elif token != " ":
                                self.answer = False
                else:
                    break

    def change_count_neighbourhood(self, island):
        self.islands[island] += 1
        if self.islands[island] > 3:
            self.answer = False

    def create_bridge(self, first, second):
        self.bridges[first][second] = 1
        self.bridges[second][first] = 1
        self.change_count_neighbourhood(first)
        self.change_count_neighbourhood(second)

    def check_neighbourhood(self):
        for island_n in self.islands:
            if island_n != 3:
                self.answer = False

    def check_connectivity(self):
        visited = [False for _ in range(self.count_of_islands)]
        count_visited_by_dfs = self.dfs(0, visited)
        if count_visited_by_dfs != self.count_of_islands:
            self.answer = False

    def dfs(self, u, visited):
        visited_vertices = 1
        visited[u] = True
        for island in range(self.count_of_islands):
            if self.bridges[u][island] == 1:
                if not visited[island]:
                    visited_vertices += self.dfs(island, visited)
        return visited_vertices

    def update_dfs (self, island, tin, fup, timer, used):
        used[island] = True
        tin[island] = fup[island] = timer + 1
        for i in range(len(self.bridges[island])):
            to = self.bridges[island][i]
            if to == 0:
                continue
            if used[to]:
                fup[island] = min (fup[island], tin[to])
            else:
                self.update_dfs(to, tin, fup, timer, used)
                fup[island] = min (fup[island], fup[to])
                if fup[to] > tin[island]:
                    self.answer = False

    def find_bridges(self, v, time_in, timer=0, parent=-1):
        timer = timer + 1
        time_in[v] = timer
        min_time = time_in[v]
        for u in range(len(self.bridges[v])):
            if self.bridges[u][v] == 1:
                if u != parent:
                    t = 0
                    if time_in[u] == 0:
                        t = self.find_bridges(u, time_in, timer, v)
                        if t > time_in[v]:
                            self.answer = False
                    else:
                        t = time_in[u]
                    min_time = min(min_time, t)
        return min_time


if __name__ == "__main__":
    numbers = input().split(" ")
    Solver(numbers[0], numbers[1])


