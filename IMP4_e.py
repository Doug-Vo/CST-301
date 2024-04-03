import json
from g4f.client import Client

def extract_classes_and_functions(ast_tree, imports):
    classes_and_functions = {}
    def traverse(node):
        if isinstance(node, dict):
            if "__class__" in node:
                if node["__class__"] == "MethodInvocation":
                    qualifier = node.get("qualifier")
                    if qualifier:
                        class_name = qualifier.split('.')[-1]  # Extract class name from the qualifier
                        class_name = imports.get(class_name, class_name)  # Replace object name with class name
                        method_name = node.get("member")
                        if class_name not in classes_and_functions:
                            classes_and_functions[class_name] = set()
                        classes_and_functions[class_name].add(method_name)
                # Traverse children recursively
                for key, value in node.items():
                    if key != "name":  # Skip "name" field
                        traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(ast_tree)

    return classes_and_functions

def find_imported_class(ast_tree, variable_name):
    class_name = None

    def traverse(node):
        nonlocal class_name
        if isinstance(node, dict):
            if "__class__" in node:
                if node["__class__"] == "LocalVariableDeclaration":
                    for declarator in node.get("declarators", []):
                        if declarator.get("name") == variable_name:
                            type_node = node.get("type")
                            if type_node and "__class__" in type_node and type_node["__class__"] == "ReferenceType":
                                class_name = type_node.get("name")
                                return
            # Traverse children recursively
            for key, value in node.items():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(ast_tree)
    return class_name

# Read AST from JSON file
with open("ast.json", "r") as file:
    ast_tree = json.load(file)

# Extract imported classes
imports = {}
for item in ast_tree["imports"]:
    class_name = item["path"].split('.')[-1]
    imports[class_name] = item["path"]


classes_and_functions = extract_classes_and_functions(ast_tree, imports)

# Convert the dictionary to the desired format
result = []
for functions in classes_and_functions.items():
    # Extracting the second part from each tuple
    result += list(functions[1])







client = Client()
messages = [
    {"role": "system",
     "content": "You are attempting to give me a summary of these functions"},
    {"role": "system",
     "content": "As you answering, only answer one sentence"},
    {"role": "system",
     "content": "Answer in the format of: function - class it belongs to - summary of the function"}
]

def ask_gpt(functions):
    # Construct the prompt with the object description and option descriptions
    prompt = "You are a robot that would only give out answers in a list, and the question is:\n"
    prompt += "Here are the imported classes: "
    for classes in imports:
        prompt += classes + ", "
    prompt += "and X is a created class in the Java code."

    prompt += "I want you to list these functions: "
    for func_info in functions:
        prompt += func_info + ", "

    prompt += "in the form of:\n"
    prompt += "Functions— function name, class it belongs to and the summary with 1 sentence."
    prompt += "For example: createStatement() - Connection - <summary of createStatement()>"
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        stream=True
    )
    return response



gpt_response = ask_gpt(result)
counter = 0
answer = ""
for chunk in gpt_response:
    if chunk.choices[0].delta.content:
        answer += (chunk.choices[0].delta.content.strip('*') or "")
print(answer)


