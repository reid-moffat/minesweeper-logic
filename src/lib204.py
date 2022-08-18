from nnf import And, dsharp, NNF, config


class Encoding(object):
    def __init__(self):
        self.constraints = []

    def vars(self):
        ret = set()
        for c in self.constraints:
            ret |= c.vars()
        return ret

    def size(self):
        return sum([c.size() for c in self.constraints])

    def valid(self):
        return And(self.constraints).valid()

    def negate(self):
        return And(self.constraints).negate()

    def add_constraint(self, c):
        assert isinstance(c, NNF), "Constraints need to be of type NNF"
        self.constraints.append(c)

    @config(sat_backend="kissat")
    def is_satisfiable(self):
        return And(self.constraints).satisfiable()

    @config(sat_backend="kissat")
    def solve(self):
        return And(self.constraints).solve()

    def count_solutions(self, lst):
        T = And(self.constraints + lst)
        return dsharp.compile(T.to_CNF(), executable='bin/dsharp').model_count()

    def likelihood(self, lit):
        return self.count_solutions([lit]) / self.count_solutions([])
