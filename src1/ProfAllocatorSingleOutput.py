#This code will generate the absolute best case scenario for the professors. Howvever it will sometimes assign X3 category professors only 1 course equivalent.

import csv 
from ortools.sat.python import cp_model
import sys

def data_parser(datafile):
    courses = []
    professors = []
    P = []

    #throw error if file is not csv
    if datafile[-4:] != '.csv':
        raise ValueError("File is not a CSV file")
    
    # Read the CSV file
    with open(datafile, 'r') as file:
        reader = csv.reader(file)
        
        # Extract course names
        header = next(reader)
        professors = header[1:]

        # Extract professor names and data
        for row in reader:
            courses.append(row[0])
            P.append(list(map(int, row[1:])))

    return courses,professors,P

def data_processor(courses,professors,P):

    # Create the model
    model = cp_model.CpModel()

    I = len(courses)
    J = len(professors)

    #Xij is my decision variable where Xij is true if professor j teaches course i
    X = {}

    # print(courses)
    # print(professors)

    for i in range(I):
        for j in range(J):
            X[i,j] = model.NewBoolVar('x[%i,%i]' % (i,j)) 
            #Such that Xij can take only bool values 0 or 1
    

    #T_is_2 is my decision variable where T_is_2[i] is true if course i has 2 professors
    T_is_2 = {}
    for i in range(I):
        T_is_2[i] = model.NewBoolVar('T_is_2[%i]' % i)


    #When T[i] == 2 , T_is_2[i] == 1 and when T[i] == 1 , T_is_2[i] == 0
    for i in range(I):
        for j in range(J):
            model.Add(T_is_2[i] == sum(X[i, k] for k in range(J)) - 1).OnlyEnforceIf(X[i, j])

    #This loop mandates that T[i] can only take values 1 or 2
    for i in range(I):
        model.Add(sum(X[i,j] for j in range(J)) >= 1)
        model.Add(sum(X[i,j] for j in range(J)) <= 2)


    #This loop mandates the specific constraints for each professor category
    for j in range(J):
        category = professors[j][:2]
        if category == 'X1':
            for i in range(I):
                model.Add(sum(X[k,j] for k in range(I)) == 1).OnlyEnforceIf(T_is_2[i])
                model.Add(sum(X[k,j] for k in range(I)) <= 1)
        if category == 'X2':
            for i in range(I):
                model.Add(sum(X[k,j] for k in range(I)) == 1).OnlyEnforceIf(T_is_2[i].Not())
                model.Add(sum(X[k,j] for k in range(I)) == 2).OnlyEnforceIf(T_is_2[i])
                model.Add(sum(X[k,j] for k in range(I)) <= 2)
        if category == 'X3':
            for i in range(I):
                model.Add(sum(X[k,j] for k in range(I)) == 2).OnlyEnforceIf(T_is_2[i].Not())
                model.Add(sum(X[k,j] for k in range(I)) >= 2).OnlyEnforceIf(T_is_2[i])
                model.Add(sum(X[k,j] for k in range(I)) <= 3).OnlyEnforceIf(T_is_2[i])
    

    #This loop makes sure that no professor is assigned a course that is not in his priority list
    for i in range(I):
        for j in range(J):
            model.Add(X[i,j]*P[i][j] > 0).OnlyEnforceIf(X[i,j])
    
    #This is the objective function that we want to maximize
    model.Maximize(sum([P[i][j]*X[i,j] for i in range(I) for j in range(J)]))
    

    solver = cp_model.CpSolver()
    status = solver.Solve(model)


    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Total Prof Score = %i' % solver.ObjectiveValue())
        print()
        #print out data into a csv file 
        with open(sys.argv[2], 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Course", "Professor"])
            for i in range(I):
                for j in range(J):
                    if solver.Value(X[i,j]) == 1:
                        writer.writerow([courses[i], professors[j]])
                        print('Course %s assigned to professor %s' % (courses[i], professors[j]))  
                        if solver.Value(T_is_2[i]) == 0:
                            print('This course has 1 professor teaching it')
                        if solver.Value(T_is_2[i]) == 1:
                            print('This course has 2 professors teaching it')
        print()
        print('Statistics')
        print('  - conflicts       : %i' % solver.NumConflicts())
        print('  - branches        : %i' % solver.NumBranches())
        print('  - wall time       : %f s' % solver.WallTime())
    else:
        print('No solution found.')

#take name of input and output file as the first and second argument
input_file = sys.argv[1]
courses,professors,P = data_parser(input_file)
data_processor(courses,professors,P)
