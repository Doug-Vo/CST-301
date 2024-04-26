import javalang
import json
import os

def read_java_files(directory):
    java_sources = {}
    for filename in os.listdir(directory):
        if filename.endswith(".java"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    java_sources[filename] = file.read()
            except FileNotFoundError:
                print(f"File not found: {file_path}")
    return java_sources

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

def merge_asts(asts):
    merged_ast = asts[0]  # Start with the first AST
    for ast in asts[1:]:  # Merge the rest of the ASTs
        merged_ast.types.extend(ast.types)
    return merged_ast

def save_ast_to_json(ast, output_file):
    ast_dict = ast_to_dict(ast)
    with open(output_file, 'w') as json_file:
        json.dump(ast_dict, json_file, default=str, indent=2)

if __name__ == "__main__":
    # Directory containing Java files
    directory = "Java code"
    output_json_file = "ast.json"

    java_sources = read_java_files(directory)

    if java_sources:
        asts = [create_ast(java_source) for java_source in java_sources.values() if java_source]
        if all(asts):
            merged_ast = merge_asts(asts)
            save_ast_to_json(merged_ast, output_json_file)
            print(f"Combined AST has been saved to {output_json_file}")
