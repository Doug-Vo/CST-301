import json
def describe_node(node, indent=0):
    result = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "__class__":
                result.append(f"{' ' * indent}Class: {value}")
            elif key == "imports" and isinstance(value, list):
                for import_node in value:
                    result.extend(describe_import(import_node, indent + 2))
            else:
                result.append(f"{' ' * indent}{key}:")
                result.extend(describe_node(value, indent + 2))
    elif isinstance(node, list):
        for item in node:
            result.extend(describe_node(item, indent))
    elif isinstance(node, str):
        result.append(f"{' ' * indent}Value: {node}")
    return result

def describe_import(import_node, indent=0):
    result = []
    if isinstance(import_node, dict) and "__class__" in import_node and import_node["__class__"] == "Import":
        path = import_node.get("path")
        if path:
            documentation_link = f"https://docs.oracle.com/en/java/javase/21/docs/api/java.base/{path.replace('.', '/')}.html"
            result.append(f"{' ' * indent}Imported: {path}")
            result.append(f"{' ' * (indent + 2)}Documentation: {documentation_link}")
    return result

def classify_nodes(node, node_types):
    if isinstance(node, dict):
        if "__class__" in node:
            node_type = node["__class__"]
            if node_type in node_types:
                node_types[node_type]["count"] += 1
            else:
                node_types[node_type] = {"count": 1, "fields": set()}
            for key, value in node.items():
                if key != "__class__":
                    if isinstance(value, str):
                        if value.isidentifier():
                            if value.islower():
                                node_types[node_type].setdefault("variables", set()).add(value)
                            else:
                                node_types[node_type].setdefault("classes", set()).add(value)
                        else:
                            node_types[node_type].setdefault("literals", set()).add(value)
                    classify_nodes(value, node_types)
                elif key == "imports" and isinstance(value, list):
                    for import_node in value:
                        describe_import(import_node)
    elif isinstance(node, list):
        for item in node:
            classify_nodes(item, node_types)


# Open the JSON file in read mode
with open('ast.json', 'r') as json_file:
    # Load the JSON data from the file
    ast = json.load(json_file)

# Describe each node and store in a list
description_list = describe_node(ast)

# Classify nodes in-depth
node_types = {}
classify_nodes(ast, node_types)

# Store in-depth classification in a list
classification_list = []
for node_type, info in node_types.items():
    classification_list.append(f"Node Type: {node_type}, Count: {info['count']}, Fields: {', '.join(info['fields'])}")
    if "variables" in info:
        classification_list.append(f"  Variables: {', '.join(info['variables'])}")
    if "literals" in info:
        classification_list.append(f"  Literals: {', '.join(info['literals'])}")
    if "classes" in info:
        classification_list.append(f"  Classes: {', '.join(info['classes'])}")

# Print or use the lists as needed
for item in description_list:
    print(item)

for item in classification_list:
    print(item)
