import json
from g4f.client import Client

options = {
    "Application": "third party apps or plugins for specific use attached to the system",
    "Application Performance Manager": "monitors performance or benchmark",
    "Big Data": "API's that deal with storing large amounts of data. with variety of formats",
    "Cloud": "APUs for software and services that run on the Internet",
    "Computer Graphics": "Manipulating visual content",
    "Data Structure": "Data structures patterns (e.g., collections, lists, trees)",
    "Databases": "Databases or metadata",
    "Software Development and IT": "Libraries for version control, continuous integration and continuous delivery",
    "Error Handling": "response and recovery procedures from error conditions",
    "Event Handling": "answers to event like listeners",
    "Geographic Information System": "Geographically referenced information",
    "Input/Output": "read, write data",
    "Interpreter": "compiler or interpreter features",
    "Internationalization": "integrate and infuse international, intercultural, and global dimensions",
    "Logic": "frameworks, patterns like commands, controls, or architecture-oriented classes",
    "Language": "internal language features and conversions",
    "Logging": "log registry for the app",
    "Machine Learning": "ML support like build a model based on training data",
    "Microservices/Services": "Independently deployable smaller services. Interface between two different applications so that they can communicate with each other",
    "Multimedia": "Representation of information with text, audio, video",
    "Multithread": "Support for concurrent execution",
    "Natural Language Processing": "Process and analyze natural language data",
    "Network": "Web protocols, sockets RMI APIs",
    "Operating System": "APIs to access and manage a computer's resources",
    "Parser": "Breaks down data into recognized pieces for further analysis",
    "Search": "API for web searching",
    "Security": "Crypto and secure protocols",
    "Setup": "Internal app configurations",
    "User Interface": "Defines forms, screens, visual controls",
    "Utility": "third party libraries for general use",
    "Test": "test automation"
}

def extract_functions(ast):
    functions = set()

    def traverse(node):
        if isinstance(node, dict):
            if "__class__" in node:
                if node["__class__"] == "MethodInvocation":
                    function_name = node.get("member")
                    if function_name:
                        functions.add(function_name)
                for key, value in node.items():
                    traverse(value)
            elif "imports" in node:
                for import_node in node["imports"]:
                    traverse(import_node)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(ast)
    return functions

def extract_unique_class(node):
    unique_class = set()  # To store unique class
    if isinstance(node, dict):
        if "__class__" in node:
            if node["__class__"] == "ReferenceType":
                unique_class.add(node["name"])
            elif node["__class__"] == "ClassDeclaration":
                unique_class.add(node["name"])
        for key, value in node.items():
            unique_class.update(extract_unique_class(value))  # Recursively traverse the JSON structure
    elif isinstance(node, list):
        for item in node:
            unique_class.update(extract_unique_class(item))  # Recursively traverse the JSON structure
    return unique_class

# Read AST from JSON file
with open('ast.json', 'r') as file:
    ast = json.load(file)

# Extract unique class
unique_class = extract_unique_class(ast)

# Initialize the file for writing
with open('output.txt', 'w') as output_file:
    client = Client()
    messages = [
        {"role": "system",
         "content": "You are attempting to classify the Java classes into one of the 31 given options"},
        {"role": "system",
         "content": "As you answering, only answer one simple word"},
        {"role": "system",
         "content": "Answer in the format of: Class (the given class) - LLM-domain - simulated domain"}
    ]

    def ask_gpt(classes):
        # Construct the prompt with the object description and option descriptions
        prompt = f"Here's the list of LLM domain options:\n {options}\n"
        prompt += "What is the LLM domain and the simulated domain of: \n"
        for class_info in classes:
            prompt += class_info + ", "
        prompt += "X is a created class in the Java code"
        prompt += "Please pick one of the 31 options for the LLM domain, and one for the simulated domain for each class"
        prompt += " and a sentence to give a reasoning for your choice"
        prompt += " the answers should be in the form of:\n"
        prompt += " Classes: \n- Chosen LLM-domain\n - Simulated Domain\n - Reasoning in one sentence "
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            stream=True
        )
        return response

    gpt_response = ask_gpt(unique_class)
    counter = 0
    answer = ""
    for chunk in gpt_response:
        if chunk.choices[0].delta.content:
            answer += (chunk.choices[0].delta.content.strip('*') or "")

    # Write the classification results to the file
    output_file.write("Classification Results:\n")
    output_file.write(answer + "\n")

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

    # Extract imported classes
    imports = {}
    for item in ast["imports"]:
        class_name = item["path"].split('.')[-1]
        imports[class_name] = item["path"]

    classes_and_functions = extract_classes_and_functions(ast, imports)

    # Convert the dictionary to the desired format
    result = []
    for functions in classes_and_functions.items():
        # Extracting the second part from each tuple
        result += list(functions[1])

    messages = [
        {"role": "system",
         "content": "You are attempting to give me a summary of these functions"},
        {"role": "system",
         "content": "As you answering, only answer one sentence"},
        {"role": "system",
         "content": "Answer in the format of: function - class it belongs to - summary of the function"}
    ]

    def ask_gpt_function(functions):
        # Construct the prompt with the object description and option descriptions
        prompt = "Using the classes from the previous question "
        prompt += "I want you to list these functions: "
        for func_info in functions:
            prompt += func_info + ", "

        prompt += "in the form of:\n"
        prompt += "Functions— function name, class it belongs to and the summary with 1 sentence."
        prompt += "For example: createStatement() - Connection - <summary of createStatement()>"
        prompt += "Make sure to only fit one class for one function, if there are many classes, only pick one"
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            stream=True
        )
        return response

    gpt_response = ask_gpt_function(result)
    answer = ""
    for chunk in gpt_response:
        if chunk.choices[0].delta.content:
            answer += (chunk.choices[0].delta.content.strip('*') or "")

    # Write the function summaries to the file
    output_file.write("\nFunction Summaries:\n")
    output_file.write(answer + "\n")

print("Output written to output.txt")
