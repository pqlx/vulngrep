class BaseAnalyzer(object):

    def __init__(self, options, filename):
        self.options = options
        self.filename = filename
        self.found = []

    def analyze_file(self, mode="file"):
        pass

    

