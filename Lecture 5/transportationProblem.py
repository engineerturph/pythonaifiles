import heapq
import sys

sys.setrecursionlimit(10000)


class PriorityQueue:
    def __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isnt in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with min priority,priority)
    # or (None,None) if priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None)


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


# Mesela 9 da recursion duruyor 9 dan giden 2 yol var 2 yoldan birini cache e ekliyor sonra
# Recursion istemeyen onceki value ya geciyor onun da en kisa yolunu cache e ekliyor.
# Nereden geldigi onemli degil her turlu sonuca ayni sekilde ulasabilir.
def dynamicProgramming(problem):
    cache = {}
    result2 = []

    def futureCost(state):
        if problem.isEnd(state):
            return 0
        if state in cache:
            return cache[state]
        result2 = []
        for action, newState, cost in problem.succAndCost(state):
            result2.append(cost + futureCost(newState))
        result = min(result2)  # suan calismiyor burasi duzelt
        cache[state] = result
        print('cache=', cache)
        return result

    return (futureCost(problem.startState()), [])


def uniformCostSearch(prolem):
    frontier = PriorityQueue()
    frontier.update(problem.startState(), 0)
    while True:
        # Move from frontier to explored
        state, pastCost = frontier.removeMin()
        if problem.isEnd(state):
            return (pastCost, [])
        # Push out on the frontier
        for action, newState, cost in problem.succAndCost(state):
            frontier.update(newState, pastCost + cost)


def printSolution(solution):
    totalCost, history = solution
    print('totalCost:', format(totalCost))
    for item in history:
        print(item)


problem = transportationProblem(N=100)
printSolution(backtrackingSearch(problem))
printSolution(dynamicProgramming(problem))
printSolution(uniformCostSearch(problem))
