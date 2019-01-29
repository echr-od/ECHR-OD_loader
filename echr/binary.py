from echr.model import Model
from echr.utils import Problem

def get_dataset(article, flavors=None, lazy=True):
    return Model(Problem.binary, article, flavors, lazy)
