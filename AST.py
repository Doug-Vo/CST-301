import javalang

class Node:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def create_ast(java_source):
    try:
        tree = javalang.parse.parse(java_source)
        return tree
    except javalang.parser.JavaSyntaxError as e:
        print("Java Syntax Error:", e)
        return None

def print_ast(node, depth=0):
    indent = "  " * depth
    if isinstance(node, Node):
        print(f"{indent}{type(node).__name__}:")
        for field, value in node.__dict__.items():
            if isinstance(value, (list, tuple)):
                for item in value:
                    print_ast(item, depth + 1)
            elif isinstance(value, Node):
                print_ast(value, depth + 1)
            else:
                print(f"{indent}  {field}: {value}")
    elif isinstance(node, (list, tuple)):
        for item in node:
            print_ast(item, depth)
    else:
        print(f"{indent}{node}")

if __name__ == "__main__":
    # Java source code snippet
    java_source_code = """
     public class Example {
  private ArrayList<String> names;

  public Example() {
    names = new ArrayList<>();
  }

  public void addName(String name) {
    names.add(name);
  }

  public List<String> getNames() {
    return new ArrayList<>(names);
  }
}
    """

    # Generate AST tree
    java_ast = create_ast(java_source_code)
    if java_ast:
        ast_tree = Node(name="compilationUnit", children=java_ast)
        print_ast(ast_tree)

# Add the AST node definitions here



# Add the AST node definitions here



































