"""Solution for problem set 3."""
import sys
import typing


class Vertex:
    """A data structure to represent each type of possible node on the board such as
    the starting port, ending port, villages, and cities.
    """

    def __init__(self, label: str, vertex_type: str, times_visited: int, neighbours: list):
        self.label = label
        self.vertex_type = vertex_type
        self.times_visited = times_visited
        self.neighbours = neighbours


def create_board_game(f):
    # Read text file 'f' into a list where each line is its own element
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    adj_list = {}
    villages = []
    cities = []

    for line in lines:
        if line.split(":")[0] == 'villages':
            villages = (line.split(":")[1].split(", "))
        elif line.split(":")[0] == 'cities':
            cities = (line.split(":")[1].split(", "))
        else:
            adj_list[line.split(":")[0]] = line.split(":")[1]

    # Initialize vertices with their labels
    vertices = {}
    for vertex in adj_list:
        v = Vertex(vertex, "", 0, [])
        vertices[vertex] = v

    # Initialize neighbours for each vertex
    for vertex in vertices:
        neighbours = adj_list[vertex].split(", ")
        for neighbour in neighbours:
            vertices[vertex].neighbours.append(vertices[neighbour])

    # Initialize type for each vertex
    for village in villages:
        vertices[village].vertex_type = "VILLAGE"

    for city in cities:
        vertices[city].vertex_type = "CITY"

    vertices["START"].vertex_type = "START"
    vertices["END"].vertex_type = "END"

    # Return the vertex dictionary and villages list
    return vertices["START"]


def paths_scenario1(s, num) -> int:
    s.times_visited += 1
    if s.label == "END":
        s.times_visited -= 1
        return num + 1
    for n in s.neighbours:
        if n.times_visited == 0:
            num = paths_scenario1(n, num)
    s.times_visited -= 1
    return num


def paths_scenario2(s, num) -> int:
    s.times_visited += 1
    if s.label == "END":
        s.times_visited -= 1
        return num + 1
    for n in s.neighbours:
        if n.vertex_type == "CITY" or (n.vertex_type in {"VILLAGE", "END"} and n.times_visited == 0):
            num = paths_scenario2(n, num)
    s.times_visited -= 1
    return num


def paths_scenario3(s, num, pass_used) -> int:
    s.times_visited += 1
    if s.label == "END":
        s.times_visited -= 1
        return num + 1
    for n in s.neighbours:
        if n.vertex_type == "CITY" or (n.vertex_type in {"START", "END", "VILLAGE"} and n.times_visited == 0):
            num = paths_scenario3(n, num, pass_used)
        elif n.vertex_type == "VILLAGE" and n.times_visited == 1 and pass_used is False:
            pass_used = True
            num = paths_scenario3(n, num, pass_used)
            pass_used = False
    s.times_visited -= 1
    return num


def open_file():
    """Open and return the file given as an argument."""
    # Check if filename is provided.
    if len(sys.argv) != 2:
        print("Usage: python3 Routes.py <inputfilename>")
        sys.exit()

    file = open(sys.argv[1])
    return file


file = open_file()
start = create_board_game(file)
scen1_paths = paths_scenario1(start, 0)
print("scenario 1 = " + str(scen1_paths))
scen2_paths = paths_scenario2(start, 0)
print("scenario 2 = " + str(scen2_paths))
scen3_paths = paths_scenario3(start, 0, False)
print("scenario 3 = " + str(scen3_paths))
