import math
import pdb
import re


class State:
    def __init__(self):
        self.minute = 0

        self.ore_prod = 1
        self.clay_prod = 0
        self.obsidian_prod = 0
        self.geode_prod = 0

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0

    def step(self):
        s = State()
        s._copy(self)
        s.ore += s.ore_prod
        s.clay += s.clay_prod
        s.obsidian += s.obsidian_prod
        s.geode += s.geode_prod

        s.minute += 1
        return s

    def _copy(self, state):
        self.ore_prod = state.ore_prod
        self.clay_prod = state.clay_prod
        self.obsidian_prod = state.obsidian_prod
        self.geode_prod = state.geode_prod

        self.ore = state.ore
        self.clay = state.clay
        self.obsidian = state.obsidian
        self.geode = state.geode

        self.minute = state.minute

        return self

    def score(self):
        return self.geode + self.geode_prod

    def best_possible(self):
        remaining = GOAL - self.minute
        return (
            self.geode + self.geode_prod * remaining + remaining * (remaining - 1) / 2
        )

    def __eq__(self, __value: object) -> bool:
        return repr(self) == repr(__value)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"{self.minute}: {self.ore} {self.clay} {self.obsidian} {self.geode} {self.ore_prod} {self.clay_prod} {self.obsidian_prod} {self.geode_prod}"


def solve(
    target: int,
    state: State,
    blueprint,
    cache: dict,
    skip_ore,
    skip_clay,
    skip_obsidian,
) -> int:
    if state.minute == target - 1:
        return state.score()

    if state in cache:
        return cache[state]

    best = 0
    ore_cost = blueprint[5]
    obsidian_cost = blueprint[6]
    if state.ore >= ore_cost and state.obsidian >= obsidian_cost:
        skip_obsidian = True
        s = state.step()
        s.ore -= ore_cost
        s.obsidian -= obsidian_cost
        s.geode_prod += 1

        best = max(best, solve(target, s, blueprint, cache, False, False, False))

        # heuristic: if we can build geode prod it's probably the best option, no need to search other options
        return best

    ore_cost = blueprint[3]
    clay_cost = blueprint[4]
    if not skip_obsidian and state.ore >= ore_cost and state.clay >= clay_cost:
        skip_obsidian = True
        # heuristic: don't need more prod than it takes to build a robot in a single turn
        if state.obsidian_prod < blueprint[6]:
            s = state.step()
            s.ore -= ore_cost
            s.clay -= clay_cost
            s.obsidian_prod += 1

            best = max(best, solve(target, s, blueprint, cache, False, False, False))

    ore_cost = blueprint[2]
    if not skip_clay and state.ore >= ore_cost:
        skip_clay = True
        # heuristic: don't need more prod than it takes to build a robot in a single turn
        if state.clay_prod < blueprint[4]:
            s = state.step()
            s.ore -= ore_cost
            s.clay_prod += 1

            best = max(best, solve(target, s, blueprint, cache, False, False, False))

    ore_cost = blueprint[1]

    if not skip_ore and state.ore >= ore_cost:
        skip_ore = True
        # heuristic: don't need more prod than it takes to build a robot in a single turn
        if state.ore_prod < max((blueprint[2], blueprint[3], blueprint[5])):
            s = state.step()
            s.ore -= ore_cost
            s.ore_prod += 1

            best = max(best, solve(target, s, blueprint, cache, False, False, False))

    s = state.step()
    best = max(
        best, solve(target, s, blueprint, cache, skip_ore, skip_clay, skip_obsidian)
    )

    cache[state] = best
    return best


def parse_raw_blueprint(s):
    """
    >>> parse_raw_blueprint("Blueprint 5: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 8 obsidian.")
    (5, 4, 4, 3, 14, 4, 8)
    """
    regex = "Blueprint (\d*): Each ore robot costs (\d*) ore. Each clay robot costs (\d*) ore. Each obsidian robot costs (\d*) ore and (\d*) clay. Each geode robot costs (\d*) ore and (\d*) obsidian."
    result = re.search(regex, s)
    return tuple(map(int, result.groups()))


def evaluate_blueprint(raw_input, target):
    blueprint = parse_raw_blueprint(raw_input)
    state = State()
    cache = {}
    ans = solve(target, state, blueprint, cache, False, False, False)

    print(f"Blueprint {blueprint[0]} can get {ans} geodes.")
    return ans


def part1():
    score = 0
    with open("day19.input") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        score += (1 + idx) * evaluate_blueprint(line, 24)

    return score


def part2():
    with open("day19.input") as f:
        lines = f.readlines()
    geodes = map(lambda line: evaluate_blueprint(line, 32), lines[0:3])
    return math.prod(geodes)


if __name__ == "__main__":
    print(part2())
