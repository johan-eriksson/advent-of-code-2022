import numpy as np


class Cube:
    def __init__(self, dimensions) -> None:
        self.points = np.zeros(tuple(dim + 2 for dim in dimensions), dtype=int)

    def add_point(self, point) -> None:
        self.points[*point] = 1

    # warning: i is a neighbour of itself
    def neighbours(self, i):
        # Neighbours along x-axis
        slice_x = self.points[[i[0] - 1, i[0] + 1], i[1], i[2]]
        # Neighbours along y-axis
        slice_y = self.points[i[0], [i[1] - 1, i[1] + 1], i[2]]
        # Neighbours along z-axis
        slice_z = self.points[i[0], i[1], [i[2] - 1, i[2] + 1]]
        neighbours = np.concatenate((slice_x, slice_y, slice_z))

        return neighbours

    def get_surface_area(self):
        score = 0
        non_zero_indices = np.nonzero(self.points)
        for i in zip(*non_zero_indices):
            neighbours = self.neighbours(i)
            score += 6 - np.sum(neighbours)
        return score

    def get_exterior_area(self):
        zero_indices = np.where(self.points == 0)
        free_area = set()
        trapped_area = set()
        for i in zip(*zero_indices):
            if i in free_area or i in trapped_area:
                continue
            area = set()
            self.fill_area(i, area)
            if self.is_trapped(area):
                trapped_area = trapped_area.union(area)
            else:
                free_area = free_area.union(area)

        score = 0
        non_zero_indices = np.nonzero(self.points)
        for i in zip(*non_zero_indices):
            adj = self.adj(i)
            for j in adj:
                if self.points[j] == 0 and j not in trapped_area:
                    score += 1
        return score

    def adj(self, i):
        x, y, z = i
        offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

        for dx, dy, dz in offsets:
            p = (x + dx, y + dy, z + dz)
            if self.in_bounds(p):
                yield p

    # so so lazy
    def in_bounds(self, p):
        try:
            discard = self.points[p]
            return True
        except IndexError:
            return False

    def fill_area(self, i, area):
        s = set()
        s.add(i)
        self._fill_area(area, s, set())

    def _fill_area(self, area, to_visit, visited):
        while len(to_visit) > 0:
            i = to_visit.pop()

            visited.add(i)
            if i in area:
                continue

            if self.points[*i] == 1:
                continue

            area.add(i)
            for j in self.adj(i):
                if j not in visited and j not in area:
                    to_visit.add(j)

    def is_trapped(self, area):
        for p in area:
            if p[0] <= 0 or p[0] >= self.points.shape[0] - 2:
                return False
            elif p[1] <= 0 or p[1] >= self.points.shape[1] - 2:
                return False
            elif p[2] <= 0 or p[2] >= self.points.shape[2] - 2:
                return False
        return True


def parse_input(lines):
    xdim, ydim, zdim = 0, 0, 0
    for line in lines:
        coord = line.strip().split(",")
        xdim = max(xdim, int(coord[0]))
        ydim = max(ydim, int(coord[1]))
        zdim = max(zdim, int(coord[2]))

    cube = Cube((xdim, ydim, zdim))
    for line in lines:
        point = tuple(map(int, line.strip().split(",")))
        cube.add_point(point)
    return cube


def part1():
    with open("day18.input") as f:
        lines = f.readlines()

    cube = parse_input(lines)
    return cube.get_surface_area()


def part2():
    with open("day18.input") as f:
        lines = f.readlines()

    cube = parse_input(lines)
    return cube.get_exterior_area()


if __name__ == "__main__":
    print(part1())
    print(part2())
