def parse():
    import argparse
    import json
    directory_options = {
        
        "project-directory": "./",
        "recursive": True,
        "filename-matches": ".+",
        "language-associations": json.load(""
    }

    file_options = {

    }

    general_options = {
    
        "mode": "directory" # file|directory / f|d

    }
    
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", 
                        help="Mode. Directory traverses a whole directory (recursive by default, see --no-recursive) while file analyzes a single file",
                        action="store",
                        choices=["directory", "file"],
                        dest="mode")

    parser.add_argument("--project-directory", "-d",
                         help="Directory of the project",
                         action="store",
                         default="./",
                         dest="project-directory")
    
    parser.add_argument("--no-recursive",
                        help="Don't traverse recursively",
                        action="store_false",
                        dest="recursive")
    
    parser.add_argument("--filename-matches", "-m",
                        help="Only analyze files matching this regex. Defaults to .+",
                        action="store",
                        default=".+",
                        dest="filename-matches")
    
    parser.add_argument("--language-associations", "-a",
                        help="A json dictionary in the form of {\"language:\": \"regex\", \"language2\": \"regex2\", ...} to associate arbitrary filenames with arbitrary languages if for example a non-standard extension is used",
                        type=json.loads,
                        default="{}",
                        dest="language-associations")

    parsed = vars(parser.parse_args())

    # Join dicts instead of overwriting
    key = "language-associations"
    directory_options[key] = {**directory_options[key], **parsed[key]}
    del parsed[key]

    options = {**directory_options, **file_options, **general_options, **parsed }
    
    return options  


if __name__ == "__main__":
    import pprint
    pprint.PrettyPrinter(indent=4).pprint(parse())