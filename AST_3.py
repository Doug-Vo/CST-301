import json
from g4f.client import Client


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
with open('output4.txt', 'w') as output_file:
    client = Client()

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

    unique_result = set(result)
    result = list(unique_result)

    messages = [
        {"role": "system",
         "content": "You are attempting to give me a summary of these functions"},
        {"role": "system",
         "content": "As you answering, only answer one sentence"},
        {"role": "system",
         "content": "Answer in the format of: function - class it belongs to - summary of the function"}
    ]



    def split_set(set_name):
        if len(set_name) > 10:
            # Calculate the size of each subset
            subset_size = len(set_name) // 3

            # Convert set to list to allow indexing
            set_list = list(set_name)

            # Split the set into three subsets
            subset1 = set(set_list[:subset_size])
            subset2 = set(set_list[subset_size:2 * subset_size])
            subset3 = set(set_list[2 * subset_size:])

            return subset1, subset2, subset3
        else:
            print("Set size is not bigger than 10.")
            return None


    if len(result) > 10:
        subset1, subset2, subset3 = split_set(result)


    def ask_gpt_function(functions):
        # Construct the prompt with the object description and option descriptions
        prompt = "Answer this questions as the form I have given you, make sure to stay with the format I gave. "
        prompt += "I want you to list these Java functions: "
        for func_info in functions:
            prompt += func_info + ", "

        prompt += "in the format of:\n"
        prompt += (" = [method name, the java class that the method belongs to (make sure to give its fully qualitified name)"
                   ", class context (1 sentence summary), "
                   "class topic (Hypothetical topics based on the general utility of the function/API)"
                   ", function_context (1 sentence summary), function topic"
                   "Large language model domain of the API class, the simulated domain of the API class, "
                   "the Large Language Model of the method, the simulated domain of the method] ")
        prompt += ("For example: "
                   "= [getInstance, java.util.Calendar"
                   ", Provides methods to manipulate date and time, "
                   "Date and Time,"
                   "Retrieves a Calendar instance, Date and Time, "
                   "Utility, Date and Time, "
                   "Data Structure, Date and Time] ")

        prompt += "Make sure you stay with the format of the example I have given you!!!"
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            stream=True
        )
        return response


    answer = ""
    if subset1:
        gpt_response = ask_gpt_function(subset1)
        for chunk in gpt_response:
            if chunk.choices[0].delta.content:
                answer += (chunk.choices[0].delta.content.strip('*') or "")

    print("--------- Completed 1/3 ----------")
    if subset2:
        gpt_response = ask_gpt_function(subset2)
        for chunk in gpt_response:
            if chunk.choices[0].delta.content:
                answer += (chunk.choices[0].delta.content.strip('*') or "")

    print("--------- Completed 2/3 ----------")
    if subset3:
        gpt_response = ask_gpt_function(subset3)
        for chunk in gpt_response:
            if chunk.choices[0].delta.content:
                answer += (chunk.choices[0].delta.content.strip('*') or "")

    print("--------- Completed 3/3 ----------")

    # Write the function summaries to the file
    output_file.write("\nFunction Summaries:\n")
    output_file.write(answer + "\n")

print("******** Output written to output4.txt ********")
