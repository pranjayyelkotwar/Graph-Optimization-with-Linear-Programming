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
   \[ \sum_{j \in J} X_{ij} = t_i, \forall i \in I \]

2. **Category-Specific Constraints:**
   - For \( j \in X_1 \):
     - If \( X_{ij} = 1 \), then \( t_i = 1 \) and \( n_j = 2 \).
   - For \( j \in X_2 \):
     - If \( X_{ij} = 1 \), then \( t_i = 1 \) and \( n_j = 1 \) or \( t_i = 1 \) and \( n_j = 2 \).
   - For \( j \in X_3 \):
     - If \( X_{ij} = 1 \), then \( t_i = 1 \) and \( n_j = 2 \) or \( t_i = 2 \) and \( n_j = 2 \) or \( t_i = 3 \).

3. **Assignment Range Constraint:**
   \[ 1 \leq \sum_{j \in J} X_{ij} \leq 2, \forall i \in I \]

4. **Professor Course Load Constraint:**
   \[ \sum_{i \in I} X_{ij} = N_j, \forall j \in J \]

## Usage

Ensure you have the OR-Tools library installed. OR-Tools is a powerful optimization library that provides a variety of tools for solving optimization problems, making it an excellent choice for this project.

```bash
pip install ortools
