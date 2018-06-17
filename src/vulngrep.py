from analyzers.PythonAnalyzer import PythonAnalyzer
from analyzers.BaseAnalyzer import BaseAnalyzer
import os.path
import re

language_analyzer_map = {

    "python": PythonAnalyzer,
    "javascript": NotImplementedError("Javascript"),
    "coffeescript": NotImplementedError("Coffeescript"),
    "c": NotImplementedError("C"),
    "cplusplus": NotImplementedError("C++"),
    "php": NotImplementedError("PHP")
}

def main():
    options = __import__("argparser").parse()
    
    PythonAnalyzer.dangerous_functions = options["dangerous-functions"]["python"]
    
    if options["mode"] == "file":
        
        path = options["path"]
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)

        analyzer = resolve_parser_from_filename(options["path"], options["language-associations"])
        
        if analyzer == None:
            print(f"No filename matches for ({dirname}/){basename}")
            return 1
        
        if isinstance(analyzer, NotImplementedError):
            raise analyzer

        analyzer = analyzer(options, path) 

        buffer = open(options["path"], 'r')

        analyzer.analyze_file(buffer.read())
        
        print_founds(analyzer)

def resolve_parser_from_filename(filename, language_assocs):
    
    for language, regex in language_assocs.items():
        
        if re.match(regex, os.path.basename(filename)):
            return language_analyzer_map[language]

    return None
            
def print_founds(analyzer: BaseAnalyzer):

    for found in analyzer.found:
        print(f"{analyzer.filename}:{found['lineno']}:{found['col']}: {found['name']}")    
    

if __name__ == "__main__":
    exit(main())



if 1 == 0:
    eval("a")
    os.system('ls')
