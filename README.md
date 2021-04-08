ANSA Scripts
========
Written in python and for specific requirements, these scripts will help user
to automate work in ANSA Pre-Processor built by BETA CAE. Scripts have been tested
on large files and across various ANSA versions.

## Description
This Repo currently includes three scripts:

**Free_Edge.py -** Creates a SET of shell elements having two or more Free edges.

**Master_Slave.py -** Creates a table of master and slave PIDs based on user
selection. Makes it easy to copy and paste master and corresponding slave PIDs
into other software (Hypermesh etc.).

**FE_Counter.py -** Changes PID values and names of shell elements based on
either filename or ANSAPART name. Changes PID, element and grid
numbering based on user input counter sorted by ascending thickness values.
Corrects thickness values to two decimal
places. Checks and fixes intersection and penetration errors. Removes
duplicate materials, curves and points.

## Installation
Requires no installation. Load the scripts using script manager available
in ANSA and user buttons with script names will be generated.

## Limitations
These scripts work on first order shell elements only (Quads and Trias).
***use at your own risk***.

## Feedback
- Scripts not working as intended?
- Could the scripts have been better written?
- Want to collab with me for new scripts?

contact me on [Linkedin](https://www.linkedin.com/in/nikhilbhargav)
