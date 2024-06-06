import pulp

# Define the triangles data with rotations
triangles = [
    ('Yw', 'Wh', 'Bl'), ('Yw', 'Yw', 'Wh'), ('Rd', 'Wh', 'Bl'), ('Bl', 'Bl', 'Wh'), ('Yw', 'Yw', 'Yw'), 
    ('Rd', 'Yw', 'Bl'), ('Rd', 'Rd', 'Wh'), ('Yw', 'Bl', 'Bl'), ('Rd', 'Yw', 'Yw'), ('Bl', 'Wh', 'Wh'), 
    ('Rd', 'Rd', 'Yw'), ('Yw', 'Bl', 'Wh'), ('Rd', 'Yw', 'Wh'), ('Rd', 'Bl', 'Wh'), ('Bl', 'Bl', 'Bl'), 
    ('Rd', 'Rd', 'Bl'), ('Rd', 'Wh', 'Wh'), ('Rd', 'Bl', 'Bl'), ('Yw', 'Yw', 'Bl'), ('Rd', 'Wh', 'Yw'), 
    ('Rd', 'Rd', 'Rd'), ('Yw', 'Wh', 'Wh'), ('Rd', 'Bl', 'Yw'), ('Wh', 'Wh', 'Wh')
]

# Define the edges and their corresponding color positions
edges = ['L', 'R', 'B']
colors = ['Yw', 'Wh', 'Bl', 'Rd']
ntriangles = len(triangles)
rows = [5, 7, 7, 5]

# Define the positions of the triangles in the grid
positions = [(i, j) for i in range(4) for j in range(rows[i])]

# Define the optimization model
model = pulp.LpProblem("TriangularPuzzle", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("x", (range(4), range(7), range(ntriangles), range(3)), cat='Binary')
y = pulp.LpVariable.dicts("y", (range(4), range(7), edges, colors), lowBound=0, upBound=1)

# Each triangle is assigned to one cell
for k in range(ntriangles):
    model += pulp.lpSum(x[i][j][k][r] for (i, j) in positions for r in range(3)) == 1

# Each cell is occupied by one triangle
for (i, j) in positions:
    model += pulp.lpSum(x[i][j][k][r] for k in range(ntriangles) for r in range(3)) == 1

# Linking x and y
for (i, j) in positions:
    for e in edges:
        for c in colors:
            model += y[i][j][e][c] == pulp.lpSum(
                x[i][j][k][r] * (triangles[k][(edges.index(e) - r) % 3] == c)
                for k in range(ntriangles) for r in range(3)
            )

# Shared edges must have the same color
# First, handle horizontal shared edges
for i in range(4):
    for j in range(rows[i] - 1):
        for c in colors:
            if (i,j) in [(0,0),(0,2),(1,0),(1,2),(1,4),(2,1),(2,3),(2,5),(3,1),(3,3)]:
                model += y[i][j]['R'][c] == y[i][j + 1]['L'][c]
            else:
                model += y[i][j]['B'][c] == y[i][j + 1]['L'][c]

for i in range(3):
    for j in range(7):
        for c in colors:
            if (i,j) in [(0,0),(0,2),(0,4)]:
                model += y[i][j]['B'][c] == y[i+1][j+1]['R'][c]
            elif (i,j) in [(1,0),(1,2),(1,4),(1,6)]:
                model += y[i][j]['B'][c] == y[i+1][j]['R'][c]
            elif (i,j) in [(2,1),(2,3),(2,5)]:
                model += y[i][j]['B'][c] == y[i+1][j-1]['R'][c]

for i in range(4):
    for j in range(7):
        for c in colors:
            if j==0:
                model += y[i][j]['L']['Bl']==1 
            elif (i,j) in [(0,1),(0,3),(0,4),(1,6)]:
                model += y[i][j]['R']['Bl']==1 
            elif (i,j) in [(2,6),(3,1),(3,3),(3,4)]:
                model += y[i][j]['B']['Bl']==1 



# Dummy objective
model += 0

# Solve the model and store solutions
solutions = []

def store_solution():
    solution = {}
    for (i, j) in positions:
        for k in range(ntriangles):
            for r in range(3):
                if pulp.value(x[i][j][k][r]) == 1:
                    solution[(i, j)] = (k, r)
    solutions.append(solution)

# Solve and add no-good cuts
for _ in range(1):  # Adjust the range for more solutions
    model.solve(pulp.PULP_CBC_CMD())
    if pulp.LpStatus[model.status] != 'Optimal':
        break
    store_solution()
    model += pulp.lpSum(
        x[i][j][k][r] * int((i, j) in solutions[-1] and solutions[-1][(i, j)] == (k, r))
        for (i, j) in positions for k in range(ntriangles) for r in range(3)
    ) <= len(positions) - 1

# Print and plot the solutions
for idx, solution in enumerate(solutions):
    print(f"Solution {idx + 1}:")
    for (i, j), (k, r) in solution.items():
        colors = [triangles[k][(edges.index(e) - r) % 3] for e in edges]
        print(f"Triangle at position ({i}, {j}):")
        for e, color in zip(edges, colors):
            print(f"  {e}: {color}")
        print()
    print()
