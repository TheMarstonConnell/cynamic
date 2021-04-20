# cynamic
 A programming language implimentation built on python to enforce C-style syntax.
 

 Syntax: 
 
 All blocks of code are contained in C-style curly braces ({}). Variables are delcared just like in python or javascript, no strong typing. 
 Every line is defined by a semi-colon just like C or java. 
 Declaring function are defined as 'function FUNCTION_NAME' followed by parameters. 
 Every program must have a 'main' function in order to run. 
 To import other code into your program, use the preprocessr function '#include' followed by the .pyc file you wish to import or '<PYTHON_IMPORT>' and it will import your files accordingly. 
 You can also define constants using '#define' followed by the key then a space and then whatever it is you wish to define.

 Compilation:

 Run the translator.py file with your python interpreter and as a paramter add the file containing your 'main' function. This will compile your program and export it as a .cy file in the same directory as the file with your 'main' function. This .cy file can be run with your python interpretor.