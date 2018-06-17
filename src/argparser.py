def parse():
    import argparse
    import json
    import os.path

    openabs = lambda x: open(os.path.join(os.path.dirname(__file__), x))

    options = {
        "mode": "directory",    
        "path": "./",
        "recursive": True,
        "filename-pattern": ".+",
        "language-associations": json.load(openabs("../cfg/filetype_regex.json")),
        "dangerous-functions": json.load(openabs("../cfg/dangerous_functions.json"))
    }
    

    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", "-m",
                        help="Mode. Directory traverses a whole directory (recursive by default, see --no-recursive) while file analyzes a single file",
                        action="store",
                        choices=["directory", "file"],
                        default="directory",
                        dest="mode")

    
    parser.add_argument("--no-recursive",
                        help="Don't traverse recursively",
                        action="store_false",
                        dest="recursive")
    
    parser.add_argument("--filename-pattern",
                        help="Only analyze files matching this regex. Defaults to .+",
                        action="store",
                        default=".+",
                        dest="filename-pattern")
    
    parser.add_argument("--language-associations", "-l",
                        help="A JSON object in the form of {\"language:\": \"regex\", \"language2\": \"regex2\", ...} to associate arbitrary filenames with arbitrary languages if for example a non-standard extension is used",
                        type=json.loads,
                        default="{}",
                        dest="language-associations")
    
    parser.add_argument("--language-associations-file",
                        help="--language-associations, but loads it from a file instead of an argument",
                        type=lambda x: json.load(open(x)) if x != "" else {},
                        default="",
                        dest="language-associations-2")

    parser.add_argument("--dangerous-functions", "-f",
                        help="A JSON object in the form of {\"language\": [\"functionname\", \"functionname2\"], \"language2\": [\"functionname3\", \"functionname4\"]} to add project-specific dangerous functions to languages",
                        type=json.loads,
                        default="{}",
                        dest="dangerous-functions")
    
    parser.add_argument("--dangerous-functions-file",
                        help="--dangerous-functions, but loads it from a file instead of an argument",
                        type=lambda x: json.load(open(x)) if x != "" else {},
                        default="",
                        dest="dangerous-functions-2")
     
    parser.add_argument( help="Directory or file, depending on mode. defaults to \"./\"",
                         action="store",
                         default="./",
                         dest="path",
                         nargs='?')

    parsed = vars(parser.parse_args())
    def merge(x):
        parsed[x] = {**parsed[x+"-2"], **parsed[x]}
        del parsed[x+"-2"]
    
    merge("language-associations")
    merge("dangerous-functions")

    # Join dicts instead of overwriting
    
    def merge_option_dict(key):
        options[key] = {**options[key], **parsed[key]}
        del parsed[key]

    merge_option_dict("language-associations")
    

    def merge_lists(key):
        for lang in parsed[key]:
            if lang in options[key]:
                options[key][lang].extend(parsed[key][lang])
                options[key][lang] = list(set(options[key][lang]))

        del parsed[key]

    merge_lists("dangerous-functions")

    return {**options, **parsed }


if __name__ == "__main__":
    import pprint
    pprint.PrettyPrinter(indent=4).pprint(parse())
