import os
import csv
import sys
from ortools.sat.python import cp_model

def data_parser(datafile):
    courses = []
    professors = []
    P = []

    if datafile[-4:] != '.csv':
        raise ValueError("File is not a CSV file")

    with open(datafile, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        professors = header[1:]

        for row in reader:
            courses.append(row[0])
            P.append(list(map(int, row[1:])))

    return courses, professors, P

def create_model(courses, professors, P):
    # Create the model
    model = cp_model.CpModel()

    I = len(courses)
    J = len(professors)

    # Xij is my decision variable where Xij is true if professor j teaches course i
    X = {}

    for i in range(I):
        for j in range(J):
            X[i, j] = model.NewBoolVar('x[%i,%i]' % (i, j))

    # T_is_2 is my decision variable where T_is_2[i] is true if course i has 2 professors
    T_is_2 = {}
    for i in range(I):
        T_is_2[i] = model.NewBoolVar('T_is_2[%i]' % i)

    for i in range(I):
        for j in range(J):
            model.Add(T_is_2[i] == sum(X[i, k] for k in range(J)) - 1).OnlyEnforceIf(X[i, j])

    for i in range(I):
        model.Add(sum(X[i, j] for j in range(J)) <= 2)
        model.Add(sum(X[i, j] for j in range(J)) >= 1)

    for j in range(J):
        category = professors[j][:2]
        if category == 'X1':
            for i in range(I):
                model.Add(sum(X[k, j] for k in range(I)) == 1).OnlyEnforceIf(X[i, j])
        if category == 'X2':
            for i in range(I):
                model.Add(sum(X[k, j] for k in range(I)) == 1).OnlyEnforceIf(T_is_2[i].Not())
                model.Add(sum(X[k, j] for k in range(I)) == 2).OnlyEnforceIf(T_is_2[i])
                model.Add(sum(X[k, j] for k in range(I)) >= 1)
                model.Add(sum(X[k, j] for k in range(I)) <= 2)
        if category == 'X3':
            for i in range(I):
                model.Add(sum(X[k, j] for k in range(I)) == 2).OnlyEnforceIf(T_is_2[i].Not())
                model.Add(sum(X[k, j] for k in range(I)) >= 2).OnlyEnforceIf(T_is_2[i])
                model.Add(sum(X[k, j] for k in range(I)) <= 3)
                model.Add(sum(X[k, j] for k in range(I)) >= 2)

    for i in range(I):
        for j in range(J):
            model.Add(X[i, j] * P[i][j] > 0).OnlyEnforceIf(X[i, j])

    return model, X

class SuboptimalSolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, courses, professors, P, X):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.courses = courses
        self.professors = professors
        self.P = P
        self.X = X
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        total_score = sum(self.Value(self.X[i, j]) * self.P[i][j] for i in range(len(self.courses)) for j in range(len(self.professors)))
        folder_path = sys.argv[2]
        os.makedirs(folder_path, exist_ok=True)
        output_file = os.path.join(folder_path, f'suboptimal_solution_{self.solution_count}_{total_score}.csv')
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Course", "Professor"])
            for i in range(len(self.courses)):
                for j in range(len(self.professors)):
                    if self.Value(self.X[i, j]) == 1:
                        writer.writerow([self.courses[i], self.professors[j]])
                        print('Course %s assigned to professor %s' % (self.courses[i], self.professors[j]))

def data_processor_suboptimal(courses, professors, P):
    model, X = create_model(courses, professors, P)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60

    callback = SuboptimalSolutionCallback(courses, professors, P, X)

    status = solver.SearchForAllSolutions(model, callback)

    if status == cp_model.INFEASIBLE:
        print('No solution found.')
    else:
        print('Search stopped. Number of solutions found:', callback.solution_count)

courses, professors, P = data_parser(sys.argv[1])
data_processor_suboptimal(courses, professors, P)
