from typing import Dict

def describe_node(node, indent=0):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "__class__":
                print(f"{' ' * indent}Class: {value}")
            else:
                print(f"{' ' * indent}{key}:")
                describe_node(value, indent + 2)
    elif isinstance(node, list):
        for item in node:
            describe_node(item, indent)
    elif isinstance(node, str):
        print(f"{' ' * indent}Value: {node}")

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
    elif isinstance(node, list):
        for item in node:
            classify_nodes(item, node_types)

# Example AST (provided AST with added missing elements)
ast = {
    "__class__": "CompilationUnit",
    "imports": [],
    "types": [
        {
            "__class__": "ClassDeclaration",
            "modifiers": "{'public'}",
            "annotations": [],
            "name": "Example",
            "body": [
                {
                    "__class__": "FieldDeclaration",
                    "modifiers": "{'private'}",
                    "annotations": [],
                    "type": {
                        "__class__": "ReferenceType",
                        "name": "ArrayList",
                        "dimensions": [],
                        "arguments": [
                            {
                                "__class__": "TypeArgument",
                                "type": {
                                    "__class__": "ReferenceType",
                                    "name": "String",
                                    "dimensions": []
                                }
                            }
                        ]
                    },
                    "declarators": [
                        {
                            "__class__": "VariableDeclarator",
                            "name": "names",
                            "dimensions": []
                        }
                    ]
                },
                {
                    "__class__": "ConstructorDeclaration",
                    "modifiers": "{'public'}",
                    "annotations": [],
                    "name": "Example",
                    "parameters": [],
                    "body": [
                        {
                            "__class__": "StatementExpression",
                            "expression": {
                                "__class__": "Assignment",
                                "expressionl": {
                                    "__class__": "MemberReference",
                                    "prefix_operators": [],
                                    "postfix_operators": [],
                                    "qualifier": "",
                                    "selectors": [],
                                    "member": "names"
                                },
                                "value": {
                                    "__class__": "ClassCreator",
                                    "prefix_operators": [],
                                    "postfix_operators": [],
                                    "selectors": [],
                                    "type": {
                                        "__class__": "ReferenceType",
                                        "name": "ArrayList",
                                        "arguments": []
                                    },
                                    "arguments": []
                                },
                                "type": "="
                            }
                        }
                    ]
                },
                {
                    "__class__": "MethodDeclaration",
                    "modifiers": "{'public'}",
                    "annotations": [],
                    "name": "addName",
                    "parameters": [
                        {
                            "__class__": "FormalParameter",
                            "modifiers": "set()",
                            "annotations": [],
                            "type": {
                                "__class__": "ReferenceType",
                                "name": "String",
                                "dimensions": []
                            },
                            "name": "name",
                            "varargs": False
                        }
                    ],
                    "body": [
                        {
                            "__class__": "StatementExpression",
                            "expression": {
                                "__class__": "MethodInvocation",
                                "prefix_operators": [],
                                "postfix_operators": [],
                                "qualifier": "names",
                                "selectors": [],
                                "arguments": [
                                    {
                                        "__class__": "MemberReference",
                                        "prefix_operators": [],
                                        "postfix_operators": [],
                                        "qualifier": "",
                                        "selectors": [],
                                        "member": "name"
                                    }
                                ],
                                "member": "add"
                            }
                        }
                    ]
                },
                {
                    "__class__": "MethodDeclaration",
                    "modifiers": "{'public'}",
                    "annotations": [],
                    "return_type": {
                        "__class__": "ReferenceType",
                        "name": "List",
                        "dimensions": [],
                        "arguments": [
                            {
                                "__class__": "TypeArgument",
                                "type": {
                                    "__class__": "ReferenceType",
                                    "name": "String",
                                    "dimensions": []
                                }
                            }
                        ]
                    },
                    "name": "getNames",
                    "parameters": [],
                    "body": [
                        {
                            "__class__": "ReturnStatement",
                            "expression": {
                                "__class__": "ClassCreator",
                                "prefix_operators": [],
                                "postfix_operators": [],
                                "selectors": [],
                                "type": {
                                    "__class__": "ReferenceType",
                                    "name": "ArrayList",
                                    "arguments": []
                                },
                                "arguments": [
                                    {
                                        "__class__": "MemberReference",
                                        "prefix_operators": [],
                                        "postfix_operators": [],
                                        "qualifier": "",
                                        "selectors": [],
                                        "member": "names"
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

# Describe each node
print("Describing each node:")
describe_node(ast)

# Classify nodes in-depth
node_types = {}
classify_nodes(ast, node_types)

# Print in-depth classification
print("\nIn-depth classification of nodes:")
for node_type, info in node_types.items():
    print(f"Node Type: {node_type}, Count: {info['count']}, Fields: {', '.join(info['fields'])}")
    if "variables" in info:
        print(f"  Variables: {', '.join(info['variables'])}")
    if "literals" in info:
        print(f"  Literals: {', '.join(info['literals'])}")
    if "classes" in info:
        print(f"  Classes: {', '.join(info['classes'])}")



