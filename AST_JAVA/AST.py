import javalang
import json

def read_java_file(file_path):
    try:
        with open(file_path, 'r') as file:
            java_source = file.read()
        return java_source
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def ast_to_dict(node):
    if isinstance(node, javalang.ast.Node):
        node_dict = {"__class__": node.__class__.__name__}
        for name, value in node.__dict__.items():
            if name != '_position' and value is not None:
                node_dict[name] = ast_to_dict(value)
        return node_dict
    elif isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    else:
        return node

def create_ast(java_source):
    try:
        tree = javalang.parse.parse(java_source)
        return tree
    except javalang.parser.JavaSyntaxError as e:
        print("Java Syntax Error:", e)
        return None

def save_ast_to_json(ast, output_file):
    ast_dict = ast_to_dict(ast)
    with open(output_file, 'w') as json_file:
        json.dump(ast_dict, json_file, default=str, indent=2)

if __name__ == "__main__":
    # Updated file paths
    file_path = "HelloWorld.java"
    output_json_file = "ast.json"

    java_source_code = read_java_file(file_path)

    if java_source_code:
        java_ast = create_ast(java_source_code)
        if java_ast:
            save_ast_to_json(java_ast, output_json_file)
            print(f"AST has been saved to {output_json_file}")
