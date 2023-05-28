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
    
    def toJson(self):
        # output myself as a json
        return json.dumps({
            "content": self.content,
            "grammar": self.grammar,
            "error": self.error,
            "logic": self.logic
        })
    
    def score(self):
        # output myself as a dict
        return {
            "content": self.content,
            "grammar": self.grammar,
            "error": self.error,
            "logic": self.logic
        }