# ORCA-Workflow-CLI
Simple and first project to showcase here. Using python, I have built a primitive CLI Workflow App for Input generation and calculation running for ORCA quantum chemistry calculation package.
For calculation what you need is a .xyz file.
Copy the path of that file and paste in the terminal when asked.
You will be asked for calculation type. Currently, it is supporting geometry optimization, single point energy calculation and frequency analysis. You can choose the criteria for level of SCF strictness you want to apply while calculation.
Then you need to select from the available - theory level (or functional) and basis set. After choosing theory level, you have option of applying dispersion correction for the theory. 
After that, you are asked for core usage configuration. They you need to enter system charge and multiplicity. 
RIJCOSX approximation option is availabble.
You will then get the input file in the same folder where .xyz file was present. The .xyz file can get updated as in geometry optimized case. 
You can either stop at input file generated or you can directly command to run the calculation. In latter case, another powershell window will open with live progress of output file being updated.
