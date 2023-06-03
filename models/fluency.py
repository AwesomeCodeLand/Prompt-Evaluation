import json

class FluencyScore:
    def __init__(self, content, grammar, error, logic):
        self.content = content
        self.grammar = grammar
        self.error = error
        self.logic = logic

    def __str__(self):
        # output myself as a string
        return "content: {}\ngrammar: {}\nerror: {}\nlogic: {}".format(
            self.content, self.grammar, self.error, self.logic)
    
    def toJSON(self):
        # output myself as a json
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # def toJson(self):
    #     # output myself as a json
    #     return json.dumps({
    #         "content": self.content,
    #         "grammar": self.grammar,
    #         "error": self.error,
    #         "logic": self.logic
    #     })
    
    def score(self):
        # output myself as a dict
        return {
            "content": self.content,
            "grammar": self.grammar,
            "error": self.error,
            "logic": self.logic
        }

class FluencyScoreEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FluencyScore):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
