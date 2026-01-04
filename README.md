# find-libraries
Library Inspection

This script analyzes a Python source file to identify libraries that have been imported, excluding standard libraries. It returns a list of installed library names along with their versions. The script utilizes the `ast` module to parse the source code and identify import statements. It also handles potential errors during the process, logging them for debugging. This is a useful tool for understanding the dependencies of a Python project. The script employs argument parsing using `argparse` to accept the file path of the source code file. 
