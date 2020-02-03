class Teacher:
    def __init__(self):
        # counterexample
        self.exs = ["ab", "abab"]

    def teacher_method(self, s):
        return (s.count("a") % 2 == 0 and s.count("b") % 2 == 0)