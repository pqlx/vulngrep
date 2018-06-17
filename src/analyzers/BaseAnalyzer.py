class BaseAnalyzer(object):

    def __init__(self, options, filename):
        self.potential_vulns = []
        self.options = options
        self.filename = filename


    def analyze_file(self, mode="file"):
        pass

    

