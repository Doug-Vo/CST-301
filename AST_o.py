import json
import requests
from bs4 import BeautifulSoup


doc = ""
Java_link = ""
def describe_node(node, indent=0):
    result = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "__class__":
                result.append(f"{' ' * indent}Class: {value}")
            elif key == "imports" and isinstance(value, list):
                for import_node in value:
                    result.extend(describe_import(import_node, doc, indent + 2))
            else:
                result.append(f"{' ' * indent}{key}:")
                result.extend(describe_node(value, indent + 2))
    elif isinstance(node, list):
        for item in node:
            result.extend(describe_node(item, indent))
    elif isinstance(node, str):
        result.append(f"{' ' * indent}Value: {node}")
    return result

def read_java_documentation(url):
    result = ""
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the text content
        documentation_content = soup.find('div', class_="header")
        if documentation_content:
            result += documentation_content.get_text(separator='')
        else:
            print("Java documentation content not found on this page.")

        # Extract the text content
        documentation_content = soup.find('div', class_="inheritance")
        if documentation_content:
            result += documentation_content.get_text(separator='')
        else:
            print("Java documentation content not found on this page.")

        # Extract the text content
        documentation_content = soup.find('section', class_="class-description")
        if documentation_content:
            result += documentation_content.get_text(separator='')
        else:
            print("Java documentation content not found on this page.")
    else:
        print("Failed to retrieve Java documentation. Status code: {}".format(response.status_code))

    return result


def describe_import(import_node, doc, indent=0):
    global Java_link
    result = []
    if isinstance(import_node, dict) and "__class__" in import_node and import_node["__class__"] == "Import":
        path = import_node.get("path")
        if path:
            documentation_link = f"https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/{path.replace('.', '/')}.html"
            Java_link = documentation_link
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
                        describe_import(import_node, doc)
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

# Call the function to read the Java documentation content
java_doc_content = read_java_documentation(Java_link)
print(java_doc_content)

