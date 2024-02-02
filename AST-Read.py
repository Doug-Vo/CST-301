import javalang
import json

def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        # Read the Java code from the file
        java_code = file.read()

    # Parse the Java code into an AST
    parser = javalang.parser.Parser()
    tree = parser.parse(java_code)

    return tree

def ast_to_json(ast):
    # Convert the AST to a dictionary
    ast_dict = {'type': ast.__class__.__name__}
    if hasattr(ast, '_fields'):
        for field in ast._fields:
            ast_dict[field] = getattr(ast, field)

    # Convert the dictionary to a JSON string
    return json.dumps(ast_dict, indent=2)

def save_ast_to_file(ast, output_file):
    # Convert AST to JSON
    ast_json = ast_to_json(ast)

    # Save JSON to a file
    with open(output_file, 'w') as file:
        file.write(ast_json)

if __name__ == "__main__":
    # Specify the Java file path
    java_file_path = 'YourJavaFile.java'

    # Parse the Java file into an AST
    ast = parse_java_file('HelloWorld.java')

    # Specify the output file path (JSON format)
    output_file_path = 'ast_output.json'

    # Save the AST to a file
    save_ast_to_file(ast, output_file_path)

    print(f"AST successfully created and saved to {output_file_path}")
