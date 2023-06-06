import pdb
import queue
import re
import numpy as np
import cProfile

class State():
    def __init__(self):
        pass

    def new(self, blueprint):
        self.blueprint = blueprint

        self.minute = 0

        self.prod = np.array([1, 0, 0, 0])
        self.stock = np.array([0, 0, 0, 0])
        self.incoming_prod = np.array([0, 0, 0, 0])

        return self

    def copy(self, state):
        self.blueprint = state.blueprint

        self.prod = np.copy(state.prod)
        self.stock = np.copy(state.stock)
        self.incoming_prod = np.copy(state.incoming_prod)

        self.minute = state.minute

        return self

    def build_all(self):    
        ore_cost = self.blueprint[5]
        obsidian_cost = self.blueprint[6]
        if self.stock[0] >= ore_cost and self.stock[2] >= obsidian_cost:
            s = State().copy(self)
            s.stock[0] -= ore_cost
            s.stock[2] -= obsidian_cost
            s.incoming_prod[3] += 1

            yield s

        ore_cost = self.blueprint[3]
        clay_cost = self.blueprint[4]
        if self.stock[0] >= ore_cost and self.stock[1] >= clay_cost:
            if self.prod[2] < self.blueprint[6]:
                s = State().copy(self)
                s.stock[0] -= ore_cost
                s.stock[1] -= clay_cost
                s.incoming_prod[2] += 1
                
                yield s

        ore_cost = self.blueprint[2]
        if self.stock[0] >= ore_cost:
            if self.prod[1] < self.blueprint[4]:
                s = State().copy(self)
                s.stock[0] -= ore_cost
                s.incoming_prod[1] += 1
                
                yield s

        ore_cost = self.blueprint[1]
        if self.stock[0] >= ore_cost:
            if self.prod[0] < max((self.blueprint[2], self.blueprint[3], self.blueprint[5])):
                s = State().copy(self)
                s.stock[0] -= ore_cost
                s.incoming_prod[0] += 1
                
                yield s

        yield self

    def step(self):
        self.stock += self.prod
        self.prod += self.incoming_prod
        self.incoming_prod = np.array([0, 0, 0, 0])
        self.minute += 1

    def score(self):
        return self.stock[3] + self.prod[3]

    def __repr__(self) -> str:
        return f"{self.stock} {self.prod}"


def parse_raw_blueprint(s):
    """
    >>> parse_raw_blueprint("Blueprint 5: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 8 obsidian.")
    (5, 4, 4, 3, 14, 4, 8)
    """
    regex = "Blueprint (\d*): Each ore robot costs (\d*) ore. Each clay robot costs (\d*) ore. Each obsidian robot costs (\d*) ore and (\d*) clay. Each geode robot costs (\d*) ore and (\d*) obsidian."
    result = re.search(regex, s)
    return tuple(map(int, result.groups()))

def evaluate_blueprint(raw_input):
    blueprint = parse_raw_blueprint(raw_input)
    end_minute = 20
    states = queue.SimpleQueue()
    states.put(State().new(blueprint))
    best = 0

    while(not states.empty()):
        state = states.get()
        if state.minute == (end_minute - 1):
            best = max(best, state.score())
        else:
            for s in state.build_all():
                states.put(s)
                s.step()

        # print(f"Step {step} has {len(states)} states")

    
    return best



if __name__ == "__main__":
    cProfile.run('evaluate_blueprint("Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.")')
    # geodes = evaluate_blueprint("Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.")
    # print(geodes)
