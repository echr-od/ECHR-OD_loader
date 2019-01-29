from echr.model import Model
from echr.utils import Problem

def get_dataset(flavors=None, lazy=True):
    return Model(Problem.multiclass, 'multiclass', flavors, lazy)
