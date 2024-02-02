import javalang


def create_ast(java_source):
    try:
        tree = javalang.parse.parse(java_source)
        return tree
    except javalang.parser.JavaSyntaxError as e:
        print("Java Syntax Error:", e)
        return None


if __name__ == "__main__":
    # Example usage
    java_source_code = """
    public class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hello, world!");
        }
    }
    """

    java_ast = create_ast(java_source_code)
    if java_ast:
        print(java_ast)

