## Introduction

This project involves solving a MacMahon 24 triangle puzzle using linear programming (LP). The puzzle consists of arranging 24 triangles in a 4-row structure to form a larger hexagonal shape. The arrangement must ensure that the shared edges of adjacent triangles have the same color. The triangles are represented by their edges with specific colors.

## Triangles

Each triangle is defined by the colors of its three edges, given in the order of left, right, and bottom edges:

```python
triangles = [
    ('Yw', 'Wh', 'Bl'), ('Yw', 'Yw', 'Wh'), ('Rd', 'Wh', 'Bl'), ('Bl', 'Bl', 'Wh'), ('Yw', 'Yw', 'Yw'), 
    ('Rd', 'Yw', 'Bl'), ('Rd', 'Rd', 'Wh'), ('Yw', 'Bl', 'Bl'), ('Rd', 'Yw', 'Yw'), ('Bl', 'Wh', 'Wh'), 
    ('Rd', 'Rd', 'Yw'), ('Yw', 'Bl', 'Wh'), ('Rd', 'Yw', 'Wh'), ('Rd', 'Bl', 'Wh'), ('Bl', 'Bl', 'Bl'), 
    ('Rd', 'Rd', 'Bl'), ('Rd', 'Wh', 'Wh'), ('Rd', 'Bl', 'Bl'), ('Yw', 'Yw', 'Bl'), ('Rd', 'Wh', 'Yw'), 
    ('Rd', 'Rd', 'Rd'), ('Yw', 'Wh', 'Wh'), ('Rd', 'Bl', 'Yw'), ('Wh', 'Wh', 'Wh')
]
```

## Grid Structure

The triangles are arranged in 4 rows to form a larger hexagonal shape:
- 1st row: 5 triangles
- 2nd row: 7 triangles
- 3rd row: 7 triangles
- 4th row: 5 triangles

## Variables

### Decision Variables

- `x[i][j][k][r]`: A binary variable indicating whether triangle `k` with rotation `r` is placed at position `(i, j)`.
- `y[i][j][e][c]`: A binary variable indicating whether edge `e` at position `(i, j)` has color `c`.

### Constraints

1. **Assignment Constraint**: Each triangle is assigned to exactly one cell and each cell contains exactly one triangle.

2. **Edge Color Matching**: Linking the decision variables `x` and `y` ensures that shared edges between adjacent triangles have the same color.

3. **Fixed Colors for Specific Edges**: Specific edges are fixed to a certain color to ensure the puzzle's solution adheres to the rules.

### Objective Function

A dummy objective function is used since the primary goal is to find feasible solutions that satisfy all constraints.

## Solving the Model

The model is solved using PuLP's CBC solver. After solving, multiple solutions are stored and printed.

## Output

The solution is printed, showing the triangle at each position and the colors of its edges.

### Sample Output Format

```
Solution 1:
Triangle at position (0, 0):
  L: Yw
  R: Wh
  B: Bl

Triangle at position (0, 1):
  L: Yw
  R: Yw
  B: Wh
...
```

## Usage

1. **Dependencies**: Ensure you have PuLP installed.
   ```
   pip install pulp
   ```

2. **Run the Script**: Execute the script to solve the puzzle and print the solutions.
   ```
   python main.py
   ```

3. **Modify Constraints**: Adjust the constraints if necessary to explore different arrangements or solutions.

## Conclusion

This project demonstrates the use of linear programming to solve a complex combinatorial puzzle, ensuring all constraints are met for a valid solution. The MacMahon 24 triangle puzzle showcases how optimization techniques can be applied to puzzle-solving and other combinatorial problems.
