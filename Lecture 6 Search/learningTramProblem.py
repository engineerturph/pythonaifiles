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


class TransportationProblem(object):
    def __init__(self, N, weights):
        self.N = N
        self.weights = weights

    def startState(self):
        return 1

    def isEnd(self, state):
        return state == self.N

    def succAndCost(self, state):
        # return list of (action,newState,cost) triples
        result = []
        if state + 1 <= self.N:
            result.append(('walk', state + 1, self.weights['walk']))
        if state * 2 <= self.N:
            result.append(('tram', state * 2, self.weights['tram']))
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


def dynamicProgramming(problem):
    cache = {}
    result2 = []

    def futureCost(state):
        if problem.isEnd(state):
            return 0
        if state in cache:
            return cache[state][0]
        result2 = []
        for action, newState, cost in problem.succAndCost(state):
            result2.append((cost + futureCost(newState), action, newState, cost))
        result = min(result2)  # suan calismiyor burasi duzelt
        cache[state] = result
        return result[0]

    state = problem.startState()
    totalCost = futureCost(state)

    # Recover history
    history = []
    while not problem.isEnd(state):
        _, action, newState, cost = cache[state]
        history.append((action, newState, cost))
        state = newState

    return (futureCost(problem.startState()), history)


def uniformCostSearch(problem):
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


### Main

def predict(N, weights):
    # f(x)
    # Input (x): N (number of blocks)
    # Output (y): path (sequence of actions)
    problem = TransportationProblem(N, weights)
    totalCost, history = dynamicProgramming(problem)
    return [action for action, newState, cost in history]


def generateExamples():
    trueWeights = {'walk': 1, 'tram': 2}
    return [(N, predict(N, trueWeights)) for N in range(1, 30)]


def structuredPerceptron(examples):
    weights = {'walk': 0, 'tram': 0}
    for t in range(100):
        numMistakes = 0
        for N, trueActions in examples:
            # Make a prediction(calculate actions according to your weights)
            predActions = predict(N, weights)
            if predActions != trueActions:
                numMistakes += 1
            # Update weights
            for action in trueActions:
                weights[action] -= 1
            for action in predActions:
                weights[action] += 1
        print('Iteration {}, numMistakes = {},weights = {}'.format(t, numMistakes, weights))
        if numMistakes == 0:
            break


examples = generateExamples()
print('Training dataset:')
for example in examples:
    print('', example)
structuredPerceptron(examples)
