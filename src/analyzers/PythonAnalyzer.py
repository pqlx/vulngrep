import BaseAnalyzer
import ast
from typing import *
import re

class PythonAnalyzer(BaseAnalyzer.BaseAnalyzer):
    
    class PythonWalker(ast.NodeVisitor):
        
        def __init__(self, analyzer) -> None:
            self.imports = []
            self.analyzer = analyzer
            

        def visit_Import(self, node: ast.Import) -> None:
            
            for alias in node.names:
                self.add_alias(alias)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            
            for alias in node.names:
                self.add_alias(alias, node.module)
        
        def visit_Call(self, node: ast.Call) -> None:

            name = self.get_function_name(node)
            
            if self.resolve_function_name(name) in PythonAnalyzer.dangerous_functions:
                self.analyzer.found.append({
                    
                    "name": name,
                    "lineno": node.lineno,
                    "col": node.col_offset

                })
                
        
        def get_function_name(self, call: ast.Call):
            """
            Extract function name from a Call object
            
            Sample:
            Call(func=Attribute(value=Attribute(value=Name(id='a', ctx=Load()), attr='b', ctx=Load()), attr='c', ctx=Load()), args=[Name(id='xd', ctx=Load())], keywords=[])
            """

            name = ""
            
            current_node = call.func
            while True:
                                
                if isinstance(current_node, ast.Attribute):
                    name = "." + current_node.attr + name
    
                if isinstance(current_node, ast.Name):
                    name = current_node.id + name
                    break
                current_node = current_node.value
            return name

        def resolve_function_name(self, function_name: str) -> str:
            """
            Resolve a function name to its absolute name
            """
            _function_name = function_name

            while True:
                attributes = _function_name.split('.')
                
                found = False

                for cutoff in range(len(attributes), 0, -1):
                    
                    current_permutation = '.'.join(attributes[:cutoff])
                    
                    for _import in self.imports:
                        if current_permutation == _import["usedname"]:
                            found = True
                            attributes[:cutoff] = _import["absolutename"]
                            _function_name = '.'.join(attributes)
                            _function_name = re.sub("\.+", ".", _function_name) # HACK to fix duplicate .s
                            break

                    if found:
                        break

                if not found:
                    break

            return _function_name

        def add_alias(self, alias, module=""):
            
            if alias.name == "":
                return 
            absolutename = ((module) if module == "" else (module + ".")) + alias.name
            usedname = alias.asname if alias.asname != None else absolutename


            self.add_import(absolutename, usedname)
             
        def add_import(self, absolute, used):
            
            self.imports.append({
        
                "absolutename": absolute,
                "usedname": used

            })

    def __init__(self, options, filename):
        super().__init__(options)
        self.filename = filename
        self.found = []
        
    def analyze_file(self, buffer: str):
        
        parsed = ast.parse(buffer)

        walker = PythonAnalyzer.PythonWalker(self)

        walker.visit(parsed)



if __name__ == "__main__":

    PythonAnalyzer.dangerous_functions = ["eval", "a.c.b"]

    a = PythonAnalyzer({}, "kek.py")

    a.analyze_file("import a.c as b; b.b()")
    print(a.found)
