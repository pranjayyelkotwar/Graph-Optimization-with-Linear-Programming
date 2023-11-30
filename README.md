# University Course Assignment System Optimization

## Overview

This Python code utilizes the OR-Tools library to optimize the University Course Assignment System. The objective is to maximize the total preference score over all possible assignments, considering professor preferences, course capacities, and category-specific constraints.

## Variables

- **I**: Set of all courses.
- **J**: Set of all professors.
- **pij**: Preference weight for course i, professor j.
- **ti**: Number of professors teaching course i.
- **Nj**: Number of courses taught by professor j.
- **Xij**: Binary variable (0,1) indicating if professor j teaches course i.

## Objective Function

The objective function aims to maximize the double summation of Xij · pij over all courses and professors:

\[ \text{Maximize} \sum_{i \in I} \sum_{j \in J} X_{ij} \cdot p_{ij} \]

## Constraints

1. **Professor Assignment Constraint:**
   - \[ \sum_{j \in J} X_{ij} = t_i \text{,} \forall i \in I \]

2. **Category-Specific Constraints:**
   - For \( j \in X_1 \):
     - If \( X_{ij} = 1 \), then \( t_i = 1 \) and \( n_j = 2 \).
   - For \( j \in X_2 \):
     - If \( X_{ij} = 1 \), then \( t_i = 1 \) and \( n_j = 1 \) or \( t_i = 1 \) and \( n_j = 2 \).
   - For \( j \in X_3 \):
     - If \( X_{ij} = 1 \), then \( t_i = 1 \) and \( n_j = 2 \) or \( t_i = 2 \) and \( n_j = 2 \) or \( t_i = 3 \).

3. **Assignment Range Constraint:**
   - \[ 1 \leq \sum_{j \in J} X_{ij} \leq 2, \forall i \in I \]

4. **Professor Course Load Constraint:**
   - \[ \sum_{i \in I} X_{ij} = N_j \text{,} \forall j \in J \]

## Usage

Ensure you have the OR-Tools library installed. OR-Tools is a powerful optimization library that provides a variety of tools for solving optimization problems, making it an excellent choice for this project.

```bash
pip install ortools
```

## Two Source Code Pieces

In this project, we have developed two distinct source code pieces, each serving a specific purpose in the optimization of the University Course Assignment System.

### Source 1 (src1)

The code in `src1` is designed to provide the most optimal solution by rigorously maximizing the objective function. It focuses on finding the assignment that results in the highest total preference score while adhering to the specified constraints and preferences. The optimization algorithm implemented in `src1` aims to achieve the best possible distribution of courses among professors.

### Source 2 (src2)

On the other hand, `src2` takes a different approach. Instead of solely concentrating on the most optimal solution, this code generates a substantial number of suboptimal solutions. The emphasis here is on exploring a broader solution space, allowing for a variety of potential course assignments. This can be particularly useful in scenarios where multiple acceptable solutions are acceptable, and a diverse set of outcomes is desired.

The existence of both source code pieces provides users with flexibility. Depending on the project requirements and objectives, one can choose between the highly optimized solution from `src1` or explore a range of alternatives with `src2`. This versatility caters to different use cases and preferences within the context of the University Course Assignment System.

It's recommended to evaluate and choose the source code piece that aligns best with the specific goals of your optimization project. Additionally, the comparison between the outputs of both sources can offer valuable insights into the diversity and robustness of the solutions generated.

# Assignment Validation Scripts

## CheckFile.py

The `CheckFile.py` script validates the format and constraints of an individual assignment CSV file.

### Usage

```bash
python CheckFile.py <input_file>
```
## CheckFolder.py

The `CheckFolder.py` script validates the format and constraints of all csv files in a given input-folder

### Usage

```bash
python CheckFolder.py <input_directory>
```
