# ProfAllocatorSingleOutput.py - Optimization Script

The `ProfAllocatorSingleOutput.py` script in the `src1` directory is designed to generate the absolute best-case scenario for professors' course assignments. This script utilizes the OR-Tools library to optimize the University Course Assignment System, maximizing the total preference score while adhering to various constraints and professor preferences.

## Usage

To run the script, provide the input CSV file containing course and professor data, and specify the output file for the optimized assignments. The script can be executed using the following command:

```bash
python ProfAllocatorSingleOutput.py input_file.csv output_file.csv
```
## Input Data Format
The input CSV file should follow the format below:
Courses,X1_Aiden,X2_Shar,X3_PJ  
FD1,10,8,10      
FD2,9,10,8  
FD3,8,9,9  
Where 10 represents highest preference , 9 represents second highest preference and so on and so forth 

### Input Data Sub-Format
We realise it might be difficult to procure data in the above format hence , in the parent directory there if a program - DataSetCreator.py which can create data in above format if it is given data in the following format :

Professors,Category,P1,P2,P3  
Pj,X1,FD1,FD2,FD3  
Shar,X2,FD4,HD3,HD1   
Nabz,X2,FD3,FD9,HD1  
