i=[]
dic1 = {"x": 9}
ship_map=[[0,1,9]]


if ship_map == 1:
    print("Hola")
else:
    print("Hello")

a = dic1["x"]
a = "acab"
print(dic1)

for i in a:
    if i =="c":
        print("c")
    elif i == "a":
        print("j")
    if type(i) == str:
        print("bbb")


for j in i:
    print("A")

def heu1():
    goal_state = ContainersState(goal_dic0)
    if problem.isGoalState(state):
        return 0
    cost_heu = 0
    total = -1
    list_cont = []
    to_be_unloaded = False
    to_be_loaded = False
    for i in range(100):
        list_cont.append([])
    for i in state.state.keys():
        if type(state.state[i]) != list:
            cost_heu += 15
            to_be_loaded = True
        else:
            to_be_unloaded = True
            position = state.state[i].copy()
            list_cont[position[0]].append([position[1], goal_state.state[i]])

    unload_1 = False
    unload_2 = False

    for column in list_cont:
        top = None
        port1 = 0
        for container in column:
            if top == None:
                top = container[0]
            elif top > container[0]:
                top = container[0]
            if container[1] == 1:
                unload_1 = True
                if port1 == 0:
                    port1 = container[0]
                elif port1 < container[0]:
                    port1 = container[0]
            unload_2 = True
        cost_heu += 40 * port1

    if to_be_unloaded:
        if unload_1:
            if state.state["port"] != 1:
                cost_heu += 3502
        if unload_2:
            if state.state["port"] == 0:
                cost_heu += 7004
            elif state.state["port"] == 1:
                cost_heu += 3502

    if to_be_loaded:
        if state.state["port"] == 0:
            cost_heu += 6999
        elif state.state["port"] == 1:
            cost_heu += 10499
        else:
            cost_heu += 12599

    return cost_heu


def heu2():
    goal_state = problem.isGoalState()
    cost_heu = 0
    port_un = 0
    port_ld = 0
    for i in state.state.keys():
        if i[-1] == "R" or i[-1] == "S":
            if type(state.state[i]) == list:
                if state.state["port"] == goal_state.state[i]:
                    cost_heu += 14
                else:
                    port_un = 1
            else:
                if state.state[i] == state.state["port"]:
                    cost_heu += 9
                else:
                    port_ld = 2

    cost_heu += 3499 * (port_ld + port_un)
    return cost_heu