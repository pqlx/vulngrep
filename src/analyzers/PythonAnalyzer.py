import BaseAnalyzer
import ast
from typing import *

class PythonAnalyzer(BaseAnalyzer.BaseAnalyzer):
    
    class PythonWalker(ast.NodeVisitor):
i       
        def __init__(self, analyzer: PythonAnalyzer) -> None:
            self.analyzer = analyzer
            self.imports = []


        def visit_Import(self, node: ast.Import) -> None:
            
            for alias in node.names:
                add_alias(alias)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            
            for alias in node.names:
                add_alias(alias, node.module)
        
        def visit_Call(self, node: ast.Call) -> None:
                    
    
        def resolve_function(function_name: str) -> str:
            """
            Resolve a function name to its absolute name
            """
            



        def add_alias(self, alias, module=""):
            
            absolutename = (module) if module == "" else (module + ".") + alias.name
            usedname = alias.asname if alias.asname != None else absolutename


            self.add_import(absolutename, usedname)
             
        def add_import(absolute, used):

            self.imports.append({
        
                "absolutename": absolute,
                "usedname": used

            })

    def __init__(self, options):
        super().__init__(options)

        self.imports = []
    
        
    def analyze_file(self, buffer):
        
        parsed = ast.parse(buffer)
