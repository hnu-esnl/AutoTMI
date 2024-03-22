class FunctionInfo:

    def __init__(self):

        self.filename = ''
        self.functionname = ''
        self.functionfullname = ''
        self.startline = 0
        self.endline = 0
        self.fullparameters = []
        self.nloc = 0
        self.cyclomatic_complexity = 0
        self.token_count = 0
        self.max_nested_structures = 0
        self.sum_if = 0
        self.sum_equal = 0
        self.sum_operator = 0

