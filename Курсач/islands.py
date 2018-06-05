import sys


class Solver:
    def __init__(self, width, height):
        self.w = int(width)
        self.h = int(height)
        self.count_of_islands = (self.w // 2 + 1) * (self.h // 2 + 1)
        self.islands = [[] for _ in range(self.count_of_islands)]
        self.answer = True
        self.solve()

    def solve(self):
        self.create_map_of_world()
        if (self.w % 2 == 0) or (self.h % 2 == 0):
            self.answer = False
        if self.answer:
            self.check_neighbourhood()
        try:
            if self.answer:
                self.check_connectivity()
            if self.answer:
                self.find_bridges(0, [0 for _ in range(self.count_of_islands)])
        except Exception:
            pass
        if self.answer:
            print("Island world")
        else:
            print("Just a picture")

    def create_map_of_world(self):
        for i in range(self.h):
            line = input()
            if len(line) != self.w:
                self.answer = False
            for j in range(self.w):
                if self.answer:
                    token = line[j]
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

    def create_bridge(self, first, second):
        count = 0
        for i in self.islands[first]:
            if i != 0:
                count += 1
        if count == 3:
            self.answer = False
        else:
            self.islands[first].append(second)
        count = 0
        for i in self.islands[second]:
            if i != 0:
                count += 1
        if count == 3:
            self.answer = False
        else:
            self.islands[second].append(first)

    def check_neighbourhood(self):
        for island_n in self.islands:
            if len(island_n) != 3:
                self.answer = False

    def check_connectivity(self):
        visited = [False for _ in range(self.count_of_islands)]
        count_visited_by_dfs = self.dfs(0, visited)
        if count_visited_by_dfs != self.count_of_islands:
            self.answer = False

    def dfs(self, u, visited):
        visited_vertices = 1
        visited[u] = True
        for island in self.islands[u]:
            if not visited[island]:
                visited_vertices += self.dfs(island, visited)
        return visited_vertices

    def find_bridges(self, v, time_in, timer=0, parent=-1):
        timer = timer + 1
        time_in[v] = timer
        min_time = time_in[v]
        for u in self.islands[v]:
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


