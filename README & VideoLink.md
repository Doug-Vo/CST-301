# CST-301
 
# README FILE
# By: Duc Vo, Ty Gehrke, Mahlete Legesse


## Documemtation
    + 'backup' folder: for backing up the pgadmin4 database

    + 'Java code' folder: including the input Java code that would be used for the project

    + 'outputTable' folder: the output table:
            "functions_api_csv": table of the output data (1)
            "api_function_specific.csv":  table of the ouput data (2)

	_ 4 executable Python file:
            "AST_1.py" (part 1): for reading the java code and convert it to an AST tree in json file
            "AST_2.py" (part 2): for print out the AST tree and the documentation of imported class from the json file
            "AST_3.py" (part 3): for using API and getting the output
            "AST_5.py" (part 4): for implement the change on the database

        _ "ast.json": the abstract tree of the current Java code
        _ "output4.txt": result used for the pgAdmin4 data from GPT-4

## Running the program

1/ Putting the desired java code in the 'Java code' folder
2/ Run "AST_1.py" which would convert all avalaible Java file into an abstract tree in 'ast.json'
3/ Run "AST_3.py" which would output all of the informations needed for the tables for pgAdmin4's data (keep in mind this would take a while due to GPT call being slow)
4/ Run "createTable.sql" in pgAdmin4 to clear the current database in pgAdmin4
5/ Run "AST_5.py" which would recreate these tables with the new data (keep in mind you will need to change the credentials for psycopg2.connect according to your own pgAdmin4 server)


