class FluencyScore:
    def __init__(self, content, grammar, error, logic):
        self.content = content
        self.grammar = grammar
        self.error = error
        self.logic = logic

    def score(self):
        # output myself as a dict
        return {
            "content": self.content,
            "grammar": self.grammar,
            "error": self.error,
            "logic": self.logic
        }