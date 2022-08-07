import sys

sys.setrecursionlimit(10000)


class transportationProblem(object):
    def __init__(self, N):
        self.N = N

    def startState(self):
        return 1

    def isEnd(self, state):
        return state == self.N

    def succAndCost(self, state):
        # return list of (action,newState,cost) triples
        result = []
        if state + 1 <= self.N:
            result.append(('walk', state + 1, 1))
        if state * 2 <= self.N:
            result.append(('tram', state * 2, 2))
        return result


### Algorithms

def backtrackingSearch(problem):
    # Best solution found so far (discitonary because of python scoping technicality)
    best = {
        'cost': float('+inf'),
        'history': None
    }

    def recurse(state, history, totalCost):
        # At state, having undergone history,accumulated totalcost
        # Explore the rest of the subtree under state
        if problem.isEnd(state):
            # Update the best solution so far
            # TODO
            if totalCost < best['cost']:
                best['cost'] = totalCost
                best['history'] = history
            return
        # Recurse on children
        for action, newState, cost in problem.succAndCost(state):
            recurse(newState, history + [(action, newState, cost)], totalCost + cost)

    recurse(problem.startState(), history=[], totalCost=0)
    return [best['cost'], best['history']]


def printSolution(solution):
    totalCost, history = solution
    print('totalCost: {}', format(totalCost))
    for item in history:
        print(item)


problem = transportationProblem(N=1000)
printSolution(backtrackingSearch(problem))
