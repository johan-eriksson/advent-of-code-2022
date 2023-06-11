import numpy as np


class Chamber:
    def __init__(self, jet_pattern, width) -> None:
        self.width = width
        self.jet_pattern = jet_pattern
        self.jet_index = 0
        self.total_rocks_dropped = 0
        self.rock_index = 0
        self.height = -1

        height_limit = 500000 * 4
        self.chamber = np.zeros((self.width, height_limit), dtype=bool)

        # first method returns where first part should be placed relative to height
        # second method returns pos of every part
        self.rocks = [
            (
                lambda height: (2, height + 1 + 3),
                lambda x, y: [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)],
            ),
            (
                lambda height: (3, height + 1 + 5),
                lambda x, y: [
                    (x, y),
                    (x - 1, y - 1),
                    (x, y - 1),
                    (x + 1, y - 1),
                    (x, y - 2),
                ],
            ),
            (
                lambda height: (4, height + 1 + 5),
                lambda x, y: [
                    (x, y),
                    (x, y - 1),
                    (x, y - 2),
                    (x - 1, y - 2),
                    (x - 2, y - 2),
                ],
            ),
            (
                lambda height: (2, height + 1 + 6),
                lambda x, y: [
                    (x, y),
                    (x, y - 1),
                    (x, y - 2),
                    (x, y - 3),
                ],
            ),
            (
                lambda height: (2, height + 1 + 4),
                lambda x, y: [
                    (x, y),
                    (x, y - 1),
                    (x + 1, y),
                    (x + 1, y - 1),
                ],
            ),
        ]

    def run_simulation(self, target_rocks):
        while self.total_rocks_dropped < target_rocks:
            self.tick()

    def tick(self):
        rock = self.rocks[self.rock_index % len(self.rocks)]
        drop_pos = rock[0](self.height)
        rocks_parts = rock[1]
        self.drop_rock(rocks_parts, drop_pos)
        self.total_rocks_dropped += 1
        self.rock_index += 1

    def drop_rock(self, rock, pos):
        while True:
            pos = self.jet_movement(rock, pos)
            pos, is_stuck = self.gravity_movement(rock, pos)
            if is_stuck:
                self.save_rock(pos, rock)
                return

    def jet_movement(self, rock, pos):
        direction = 1 if self.jet_pattern[self.jet_index] == ">" else -1
        self.jet_index = (self.jet_index + 1) % len(self.jet_pattern)

        new_pos = (pos[0] + direction, pos[1])
        for rock_pos in rock(*new_pos):
            if rock_pos[0] < 0 or rock_pos[0] >= self.width:
                return pos
            if self.chamber[rock_pos]:
                return pos

        return new_pos

    def gravity_movement(self, rock, pos):
        new_pos = (pos[0], pos[1] - 1)
        for rock_pos in rock(*new_pos):
            if self.chamber[rock_pos] or rock_pos[1] < 0:
                return pos, True

        return new_pos, False

    def save_rock(self, pos, rock):
        for rock_part in rock(*pos):
            self.height = max(self.height, rock_part[1])
            self.chamber[rock_part] = True

    def draw(self):
        stack = []
        stack.append("+-------+")
        i = 0
        while True:
            line = self.chamber[:, i]
            i += 1
            if any(line):
                stack.append(f"|{''.join(['#' if pos else '.' for pos in line])}|")
            else:
                stack.append("|.......|")
                stack.append("|.......|")
                stack.append("|.......|")

                for line in reversed(stack):
                    print(line)
                return

    def score(self):
        # one extra because zero indexed
        return self.height + 1


def part1():
    with open("day17.input") as f:
        jet_pattern = f.read()

    chamber = Chamber(jet_pattern, 7)
    chamber.run_simulation(2022)

    return chamber.score()


def part2():
    with open("day17.input") as f:
        jet_pattern = f.read()

    chamber = Chamber(jet_pattern, 7)
    i = 0

    jets = []

    # 1000 is a random low number where there will probably be a cycle
    # if not, increase the number until a cycle is found
    while i < 1000:
        jets.append(chamber.jet_index)
        for _ in range(5):
            chamber.tick()
        i += 1

    # floyds cycle finding algorithm
    ti = 1
    hi = 2

    tortoise = jets[ti]
    hare = jets[hi]

    while tortoise != hare:
        ti += 1
        hi += 2
        tortoise = jets[ti]
        hare = jets[hi]

    ti = 0
    tortoise = jets[ti]
    while tortoise != hare:
        hi += 1
        ti += 1
        tortoise = jets[ti]
        hare = jets[hi]

    # floyds algorithm can keep going to find the smallest cycle, but in this application
    # we don't care because we are happy getting some multiple of the smallest cycle

    cycle_start = ti * 5
    cycle_end = hi * 5

    chamber = Chamber(jet_pattern, 7)
    chamber.run_simulation(cycle_start)

    height_before_cycle = chamber.score()

    cycle_length = cycle_end - cycle_start

    i = cycle_length
    while i > 0:
        chamber.tick()
        i -= 1

    single_cycle_height = chamber.score() - height_before_cycle

    cycles_needed = (1_000_000_000_000 - cycle_start) // cycle_length

    height_all_cycles = single_cycle_height * cycles_needed

    remainder = (1_000_000_000_000 - cycle_start) % cycle_length

    while remainder > 0:
        chamber.tick()
        remainder -= 1

    height_of_remainders = chamber.score() - height_before_cycle - single_cycle_height

    return height_before_cycle + height_all_cycles + height_of_remainders


if __name__ == "__main__":
    print(part1())
    print(part2())
