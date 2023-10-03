from builtins import object
import time
import sys
import heapq

"""This class and the one below are in charge of storing the states"""
class StackQueue(object):
    def __init__(self):
        self.stack = []
        self.count = 0

    def pushItem(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.stack, entry)
        self.count += 1

    def popItem(self):
        (_, _, item) = heapq.heappop(self.stack)
        return item

    def checkIsEmpty(self):
        return len(self.stack) == 0


class StackQueueFunction(StackQueue):
    def __init__(self, priorityFunction):
        self.priorityFunction = priorityFunction
        StackQueue.__init__(self)

    def pushItem(self, item):
        priority = [x(item) for x in self.priorityFunction]
        StackQueue.pushItem(self, item, priority)

"""INPUTS PROCESSING AND CREATION OF THE INITIAL AND GOAL DICTIONARIES"""

"""MAP FILE READING"""
map = open(sys.argv[1]+"/"+sys.argv[2], "r")
xAxis = 0
ship_map = []
for i in map.read():
    if i == "N":
        if len(ship_map) <= xAxis:
            ship_map.append([])
        ship_map[xAxis].append("S")
        xAxis += 1
    elif i == "E":
        if len(ship_map) <=xAxis:
            ship_map.append([])
        ship_map[xAxis].append("R")
        xAxis += 1
    elif i == "\n":
        xAxis = 0
    elif i == "X":
        xAxis += 1

print(ship_map)
problem_data = {}
goal_dic0 = {}

#Reading the containers file
containers = open(sys.argv[1]+"/"+sys.argv[3],"r")

#Looping through the different lines and storing the data in the list that corresponds
digits = ["0","1","2","3","4","5","6","7","8","9"]
container = ""
port = ""
finding_port = False

"""CONTAINERS FILE READING"""
for i in containers.read():
    if i in digits:
        if not finding_port:
            container += i
        elif finding_port:
            port += i
    elif i == "S":
        num = int(container) - 1
        container = str(num) + "S"
        problem_data[container] = 0
        finding_port = True
    elif i == "R":
        num = int(container) - 1
        container = str(num) + "R"
        problem_data[container] = 0
        finding_port = True
    elif i == "\n":
        goal_dic0[container] = int(port)
        container = ""
        port = ""
        finding_port = False

if len(goal_dic0) < len(problem_data):
    goal_dic0[container] = int(port)
    container = ""
    port = ""
    finding_port = False


"""HERE THE BOTTOM POSITIONS ARE STORED IN THE DICTIONOARY"""
#Bottom positions
num_column = 0
for column in ship_map:
    key = "B"+str(num_column)
    problem_data[key] = [num_column, len(column)-1]
    goal_dic0[key] = [num_column, len(column) - 1]
    num_column += 1

problem_data["port"] = 0
goal_dic0["port"] = 0

print("problem_data: ", problem_data)
print("goal_dic0: ", goal_dic0)


"""CLASS TO DO THE SEARCH"""
def search(problem, structure):
    structure.pushItem([(problem.getStartState(), "No action", 0)])
    visited = []
    cost=0
    expanded_nodes = 0
    while not structure.checkIsEmpty():
        path = structure.popItem()
        curr_state = path[-1][0]
        if problem.checkIsGoalState(curr_state):
            for i in path[1:]:
                cost += i[2]
            return [x[1] for x in path][1:], cost, expanded_nodes

        if curr_state not in visited:
            visited.append(curr_state)
            expanded_nodes += 1
            print(expanded_nodes)
            for successor in problem.getSuccessors(curr_state):
                if successor[0] not in visited:
                    successorPath = path[:]
                    successorPath.append(successor)
                    structure.pushItem(successorPath)

    return False, expanded_nodes

"""FIRST HEURISTIC"""
def heuristic1(state):
    goal_state = ContainersState(goal_dic0)
    cost_heu = port_un1 = port_un2 = port_ld1 = port_ld2 = port_ldn = 0
    bottom_list = []
    for i in state.state.keys():
        if i[0] == "B":
            bottom_list.append([])
    for i in state.state.keys():
        if i[0] == "B":
            bottom_list[int(i[-1])] = state.state[i][1]
    for i in state.state.keys():
        if i[-1] == "R" or i[-1] == "S":
            if type(state.state[i]) == list:
                if state.state["port"] == goal_state.state[i]:
                    cost_heu += 15
                elif goal_state.state[i] == 1:
                    port_un1 = 1
                    cost_heu += 15
                elif goal_state.state[i] == 2:
                    port_un2 = 1
                    cost_heu += 15
                cost_heu += 2 * state.state[i][1]

    for i in state.state.keys():
        if i[-1] == "R" or i[-1] == "S":
            if type(state.state[i]) == int:
                if state.state[i] != goal_state.state[i]:
                    if state.state[i] == state.state["port"]:
                        cost_heu += 25
                        if goal_state.state["port"] == 1 and port_un1 == 0:
                            port_ld1 = 1
                        elif port_un2 == 0:
                            port_ld2 = 1
                    else:
                        cost_heu += 25
                        port_ldn = 2

    cost_heu += 3500 * (port_ld1 + port_ld2 + port_un1 + port_un2 + port_ldn)
    return cost_heu

"""SECOND HEURISTIC"""
def heuristic2(state):

    goal_state = ContainersState(goal_dic0)
    cost_heu = port_un = port_ld = port_ldn = 0
    for i in state.state.keys():
        if i[-1] == "R" or i[-1] == "S":
            if type(state.state[i]) == list:
                if state.state["port"] == goal_state.state[i]:
                    cost_heu += 15
                elif goal_state.state[i] == 1:
                    port_un = 1
                    cost_heu += 15
                elif goal_state.state[i] == 2:
                    port_un = 1
                    cost_heu += 15
                cost_heu += 2 * state.state[i][1]
    for i in state.state.keys():
        if i[-1] == "R" or i[-1] == "S":
            if type(state.state[i]) == int:
                if state.state[i] != goal_state.state[i]:
                    if state.state[i] == state.state["port"]:
                        cost_heu += 25
                        port_ld = 1
                    else:
                        cost_heu += 25
                        port_ldn = 2
    cost_heu += 3500 * (port_ld + port_un + port_ldn)

    return cost_heu

"""CLASS TO CHOOSE BETWEEN THE HEURISTIC, COMPUTE THE COSTS OF THE PATHS AND STORE THE NODES"""
def aStarSearch(problem):
    if sys.argv[4] == "heuristic1":
        g = lambda path: problem.getCostActions([x[2] for x in path][1:]) + heuristic1(path[-1][0])
        h = lambda path: heuristic1(path[-1][0])
    elif sys.argv[4] == "heuristic2":
        g = lambda path: problem.getCostActions([x[2] for x in path][1:]) + heuristic2(path[-1][0])
        h = lambda path: heuristic2(path[-1][0])
    pq = StackQueueFunction((g, h))
    return search(problem, pq)



"""CLASS FOR THE STATES"""
class ContainersState(object):

    def __init__(self, state_dic):
        self.state = state_dic

    def __eq__(self, object):
        if self.state == object.state:
            return True
        return False

    """This function checks if a state is the goal state"""
    def checkIsGoal(self, goal_dic = goal_dic0):
        for key in self.state:
            if not key == "port":
                if self.state[key] != goal_dic[key]:
                    return False
        return True

    """This function obtains the possible moves for a given state"""
    def movementsPossible(self):
        moves = []
        bottom = []
        port = self.state["port"]
        for key in self.state.keys():
            if key[0] == "B":
                bottom.append(self.state[key])

        """These three ifs are to check the possible ports where the ship can go"""
        if port == 0:
            cost = 3500
            moves.append(["pup", cost])
            moves.append(["p2up", cost])
        if port == 1:
            cost = 3500
            moves.append(["pup", cost])
            moves.append(["pdown", cost])
        if port == 2:
            cost = 3500
            moves.append(["pdown", cost])
            moves.append(["p2down", cost])

        """LOAD()"""
        for i in bottom:
            if i[1] != -1:
                """This if is to look for refrigerated places"""
                if ship_map[i[0]][i[1]] == "R":
                    for containers_id in self.state.keys():
                        """All containers can go in the energy cell"""
                        if containers_id[-1] == "R" or containers_id[-1] == "S":
                            if self.state[containers_id] == port:
                                movement = ["l", containers_id, i[0], i[1]]
                                cost = 10 + i[1]
                                moves.append([movement, cost])
                """If the cell is standard"""
                if ship_map[i[0]][i[1]] == "S":
                    for containers_id in self.state.keys():
                        """Only standard containers can be placed there"""
                        if containers_id[-1] == "S":
                            if self.state[containers_id] == port:
                                movement = ["l", containers_id, i[0], i[1]]
                                cost = 10 + i[1]
                                moves.append([movement, cost])
            """UNLOAD()"""
            for containers_id in self.state.keys():
                if containers_id[-1] == "R" or containers_id[-1] == "S":
                    """If the containers are in the ship"""
                    if type(self.state[containers_id]) == list:
                        position = self.state[containers_id].copy()
                        if i[0] == position[0]:
                            """If they are the top items"""
                            if position[1] == i[1]+1:
                                movement = ["u", containers_id, position[0], position[1]]
                                cost = 15 + 2*position[1]
                                moves.append([movement, cost])
        return moves


    """This function returns the result of an action in the state"""
    def createNewState(self, move):
        new_dic = self.state.copy()
        if move == "pup":
            new_dic["port"] += 1
        elif move == "pdown":
            new_dic["port"] -= 1
        elif move == "p2up":
            new_dic["port"] += 2
        elif move == "p2down":
            new_dic["port"] -=2
        elif move[0] == "l":
            new_dic[move[1]] = [move[2], move[3]]
            new_dic["B"+str(move[2])] = [move[2], move[3]-1]
        elif move[0] == "u":
            port = new_dic["port"]
            new_dic[move[1]] = port
            new_dic["B" + str(move[2])] = [move[2], move[3]]
        new_state = ContainersState(new_dic)
        return new_state

"""CLASS TO INITIALIZE THE PROBLEM"""
class ContainersSearchProblem():

    def __init__(self, data):
        self.problem_data = data

    def __eq__(self, other):
        if self.problem_data == other.problem_data:
            return True
        return False
    def getStartState(self):
        return data

    def checkIsGoalState(self, state):
        return state.checkIsGoal()

    def getSuccessors(self, state):
        succ = []
        for moves in state.movementsPossible():
            succ.append((state.createNewState(moves[0]), moves[0], moves[1]))
        return succ

    def getCostActions(self, actions):
        total_cost = 0
        for cost in actions:
            total_cost+=cost
        return total_cost

"""FUNCTION TO READ THE OUTPUS OF THE PROBLEM AND CREATE THE OUTPUT FILES"""
def createOutput(path, params_init, time):
    output = open(params_init[1]+"/"+params_init[2]+"-"+params_init[3]+"-"+params_init[4]+".output", "w")
    if path == False:
        output.write("1. False")
        stat = open(params_init[1] + "/" + params_init[2] + "-" + params_init[3] + "-" + params_init[4] + ".stat", "w")
        stat.write("Overall time: " + str(time) + "\n")
        stat.write("Overall cost: None"+ "\n")
        stat.write("Plan length: None" + "\n")
        stat.write("Expanded nodes: None")
    else:
        counter = 1
        port = 0
        for i in path[0]:
            out = str(counter) + ". "
            if type(i) == list:
                if i[0] == "l":
                    out += "Load("
                elif i[0] == "u":
                    out += "Unload("
                if i[1][-1] == "R":
                    out += "Refrig cont: "
                elif i[1][-1] == "S":
                    out += "Std cont: "
                out += str(i[1][:-1]) + ", Pos in boat: (" + str(i[2]) + "," + str(i[3]) + "), Port: "+str(port)+")"
            elif type(i) == str:
                out += "Sail(Port: "
                if i == "pup":
                    port += 1
                elif i == "pdown":
                    port -= 1
                elif i == "p2up":
                    port += 2
                elif i == "p2down":
                    port -= 2

                out += str(port) + ")"

            output.write(out + "\n")
            counter += 1
        stat = open(params_init[1]+"/"+params_init[2]+"-"+params_init[3]+"-"+params_init[4]+".stat", "w")
        stat.write("Overall time: " + str(time)+ "\n")
        stat.write("Overall cost: " + str(path[1])+"\n")
        stat.write("Plan length: " + str(len(path[0]))+"\n")
        stat.write("Expanded nodes: " + str(path[2]))


"""WHEN THIS FILE IS CALLED, THE INITIAL STATE AND THE PROBLEM IS CREATED, THEN THE SEARCH IS STARTED AND THE OUTPUTS ARE PROCESSED"""
if __name__ == '__main__':
    data = ContainersState(problem_data)
    problem = ContainersSearchProblem(data)
    start_time = time.time()
    path = aStarSearch(problem)
    end_time = time.time()
    print("SOLUTION:",path)
    createOutput(path, sys.argv, end_time - start_time)
    print("TIME:", end_time-start_time)
