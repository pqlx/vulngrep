from analyzers.PythonAnalyzer import PythonAnalyzer
from analyzers.BaseAnalyzer import BaseAnalyzer
import os.path
import re
import pygments
import pygments.lexers
import pygments.formatters
import ansiwrap

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
        if dirname == "":
            dirname = "."

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



def highlight_colors(language, code):

    lexers = {
        "python": pygments.lexers.PythonLexer
    }

    return pygments.highlight(code, lexers[language](), pygments.formatters.TerminalFormatter()).strip()


def print_founds(analyzer: BaseAnalyzer):
    
    from colored import fg, bg, attr
    

    def ansi_ljust(s, width):
        needed = width - ansiwrap.ansilen(s)
        if needed > 0:
            return s + ' ' * needed
        else:
            return s

    for found in analyzer.found:
        found["code"] = highlight_colors(analyzer.language, found["code"])


    filename_line_col_max = len(analyzer.filename) + max([len(str(x['lineno']) + str(x['col'])) for x in analyzer.found]) + 2
    code_max = max([ansiwrap.ansilen(x['code']) for x in analyzer.found])

    for found in analyzer.found:
        
        filename_line_col = (analyzer.filename + ":" + str(found['lineno']) + ":" + str(found['col'])).ljust(filename_line_col_max + 4)

        code = ansi_ljust(found['code'], code_max + 4)

        line = f"{fg(164)}{filename_line_col}{attr(0)}{code}{{ "
        
        if found['name'] != found['from']:
            line += f"{fg('red')}{found['name']}{attr(0)}() -> "
        
        line += f"{fg(46)}{found['from']}{attr(0)}() }}"

        print(line)
        
    
    if len(analyzer.found) == 0:
        print(f"{analyzer.filename}: No potentially dangerous functions found")

if __name__ == "__main__":
    exit(main())



if 1 == 0:
    eval("a")
    import os
    os.system('ls')

    import os.system as b
    from os import *
    b("a")
    system("ls")
