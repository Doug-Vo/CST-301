from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from JavaListener import JavaListener
import json

class MyListener(JavaListener):
    def __init__(self):
        self.ast = {}

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_name = ctx.Identifier().getText()
        parameters = [param.getText() for param in ctx.formalParameters().formalParameter()]
        self.ast[method_name] = {"type": "method", "parameters": parameters}

def generate_ast(java_code, output_file="ast.json"):
    input_stream = InputStream(java_code)
    lexer = JavaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.compilationUnit()

    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    ast_json = json.dumps(listener.ast, indent=2)

    with open(output_file, "w") as file:
        file.write(ast_json)

if __name__ == "__main__":
    # Read Java code from a file or user input
    java_code = """
    class MyClass {
        public void myMethod(int param1, String param2) {
            // Method body
        }
    }
    """

    generate_ast(java_code)
