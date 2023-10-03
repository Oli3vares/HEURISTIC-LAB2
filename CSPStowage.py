#!/usr/bin/env python
# −∗− coding: utf−8 −∗−

import constraint
import sys

def check_above(a, b):
    if a[0] == b[0]:
        if b[1] > a[1]:
            return True
        else:
            return False
    else:
        return True


def check_grav(ground, *args):
    temp_sols = args
    print("\n LOOP")
    #print("te:", temp_sols)
    for id in temp_sols:
        found = False
        for position in ground:
            if id == position:
                print("GROUND")
                print("Id:", id, "Ground:", position)
                found = True
        for id_rest in temp_sols:
            if id != id_rest:
                if id[0] == id_rest[0]:
                    if id[1] == id_rest[1]-1:
                        #print("Id", id, "Id2", id_rest)
                        found = True
        if not found:
            print("Incorrect solution")
            print(temp_sols)
            return False
    if found:
        #print("Correct solution")
        return True

NormalEnergyCells = []
EnergyCells = []

map = open(sys.argv[1]+"/"+sys.argv[2], "r")

#print(map.read())

xAxis = 0
yAxis = 0

for i in map.read():
    if i == "N":
        NormalEnergyCells.append([xAxis, yAxis])
        xAxis += 1
    elif i == "E":
        NormalEnergyCells.append([xAxis, yAxis])
        EnergyCells.append([xAxis, yAxis])
        xAxis += 1
    elif i == "\n":
        yAxis += 1
        xAxis = 0
    elif i == "X":
        xAxis += 1



port1=[]
port2=[]
refrigerated=[]
standard=[]


containers = open(sys.argv[1]+"/"+sys.argv[3],"r")

digits = ["0","1","2","3","4","5","6","7","8","9"]
number = ""
port = ""
for i in containers.read():
    if i in digits:
        number += i
    elif i == "S":
        standard.append(number)
    elif i == "R":
        refrigerated.append(number)
    elif i == "\n":
        if number[-1] == "1":
            port1.append(number[:-1])
            number = ""
        elif number[-1] == "2":
            port2.append(number[:-1])
            number = ""

if len(standard) + len(refrigerated) != len(port1)+len(port2):
    if number[-1] == "1":
        port1.append(number[:-1])
    if number[-1] == "2":
        port2.append(number[:-1])

for i in range(len(NormalEnergyCells)):
    NormalEnergyCells[i] = tuple(NormalEnergyCells[i])

for i in range(len(EnergyCells)):
    EnergyCells[i] = tuple(EnergyCells[i])

bottom = []
for i in range(len(NormalEnergyCells)):
    if len(bottom) == 0:
        bottom.append(NormalEnergyCells[i])
    else:
        bottom_column = False
        for j in range(len(bottom)):
            if NormalEnergyCells[i][0] == bottom[j][0]:
                bottom_column = True
                if NormalEnergyCells[i][1] > bottom[j][1]:
                    bottom[j] = NormalEnergyCells[i]
        if not bottom_column:
            bottom.append(NormalEnergyCells[i])

print("Bottom", bottom)
print("port1", port1)
print("port2", port2)
print("standard:", standard)
print("refrigerated:", refrigerated)
print("Normal cells:", NormalEnergyCells)
print("Energy cells:", EnergyCells)







problem = constraint.Problem()
problem.addVariables(standard, NormalEnergyCells)
problem.addVariables(refrigerated, EnergyCells)

problem.addConstraint(constraint.AllDifferentConstraint())
for i in port1:
    for j in port2:
        problem.addConstraint(check_above, (i, j))
l = standard+refrigerated
problem.addConstraint(lambda *args: check_grav(bottom, *args), l)



solutions = problem.getSolutions()
print(" #{0} solutions" .format(len(solutions)))

output = open(sys.argv[1]+"/"+sys.argv[2]+"-"+sys.argv[3]+".output", "w")
output.write("Number of solutions: " + str(len(solutions)) + "\n")
for i in solutions:
    out = "{"
    for key in i:
        out += str(key) + ": " + str(i[key]) +", "
    out = out[:-2]
    out += "}"
    output.write(out + "\n")
    #output.write(str(i)+"\n")