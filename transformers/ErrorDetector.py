from instances.ErrorInstance import ErrorInstance


class ErrorDetector:
    def __init__(self, ft_model):
        self.model = ft_model

    def fit(self, x=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            for i, token in enumerate(problem.tokens):
                if not self.model.is_in_dict(token):
                    problem.errors.append(ErrorInstance(token, i))
                    problem.is_error.append(True)
                else:
                    problem.is_error.append(False)
        return x
