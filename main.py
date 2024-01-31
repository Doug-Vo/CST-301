import ast

# Define a simple function
code = """
def add_numbers(a, b):
    return a + b
"""

# Parse the code into an AST
parsed_ast = ast.parse(code)

# Print out the AST in a readable format
print(ast.dump(parsed_ast, indent=4))
