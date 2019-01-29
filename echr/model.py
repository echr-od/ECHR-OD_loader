import numpy as np
from scipy import sparse

from utils import get_data_file_location, \
                  get_flavors_list, \
                  get_outcome_file_location, \
                  get_input_path, \
                  Flavor, \
                  Problem

class Model(object):

    def __init__(self, dataset_type, article, flavors=None, lazy=True):
        if get_input_path() is None:
            raise Exception('Could not find ECHR datasets.')
            raise NotADirectoryError('Could not find ECHR datasets.')

        self.dataset_type = dataset_type
        self.article = article
        self.flavors = flavors if flavors is not None else get_flavors_list() # TODO: per article / dataset
        self.lazy = lazy
        self._data = {}
        self._outcomes = None
        self._preprocess = {}

        if not lazy:
            load()

    @property
    def X(self):
        return self._load_flavors()

    @property
    def y(self):
        return self._load_outcomes()

    def register_preprocess(self, flavor, operator):
        if flavor not in self._preprocess:
            self._preprocess[flavor] = []
        self._preprocess[flavor].append(operator)
        return self

    def get_X(self, flavors=None, force=False):
        return self._load_flavors(flavors, force)

    def load(self, flavors=None, force=False):
        X = self._load_flavors(flavors, force)
        y = self._load_outcomes(force)
        return X, y

    def is_loaded(self, flavor):
        return flavor in self._data

    def set_flavors(self, flavors):
        for flavor in self._data[flavor].keys():
            if flavor not in flavors:
                del self._data[flavor]
        self.flavors = flavors
        return self

    def add_flavors(self, flavor):
        if flavor not in self.flavor:
            self.flavors.append(flavor)
        return self

    def _stack_flavors(self, flavors):
        return sparse.hstack([d for f,d in self._data.iteritems() if f in flavors])

    def _load_flavors(self, flavors=None, force=False):
        if flavors is None:
            to_load = self.flavors
        elif isinstance(flavors, Flavor):
            to_load = [flavors]
        else:
            to_load = flavors
        loaded = {}
        for flavor in to_load:
            if not self.is_loaded(flavor) or force:
                X, errors = self._load_flavor(flavor)
                if not len(errors):
                    loaded[flavor] = X

        self._data.update(loaded)
        if flavors is None:
           to_return = self._data.keys()
        else:
            to_return = to_load
        return self._stack_flavors(to_return)

    def _load_flavor(self, flavor, mode='binary'):
        if mode == 'binary':
            return self._load_flavor_binary(flavor)
        else:
            return [], [] # Todo

    def _load_flavor_binary(self, flavor):
        if self.dataset_type == Problem.binary:
            name = 'article_{}'.format(self.article)
        else:
            name = self.dataset_type.name
        data_file = get_data_file_location(name, flavor)
        with open(data_file) as file:
            data = file.readlines()
            data = [d.split() for d in data]
            for i, d in enumerate(data):
                data[i] = [int(''.join(e.split(':'))) for e in d]
            file.close()
        docs = np.array(data, dtype=object)
        for op in self._preprocess.get(flavor, []):
            docs, stats = op(docs)
        indptr = [0]
        indices = []
        data = []
        vocabulary = {}
        for d in docs:
            for term in d:
                index = vocabulary.setdefault(term, len(vocabulary))
                indices.append(index)
                #data.append(1)
                data.append(term)
            indptr.append(len(indices))
        X = sparse.csr_matrix((data, indices, indptr), dtype=int)
        return X, []

    def _load_outcomes(self, force=True):
        if self.dataset_type == Problem.binary:
            name = 'article_{}'.format(self.article)
        else:
            name = self.dataset_type.name
        if self._outcomes is None or force:
            outcome_file = get_outcome_file_location(name)
            with open(outcome_file) as file:
                outcomes = file.readlines()
                if self.dataset_type == Problem.binary:
                    outcomes = np.array([int(d.split()[-1].split(':')[-1]) for d in outcomes])
                else:
                    if self.dataset_type == Problem.multilabel:
                        outcomes = [d.split() for d in outcomes]
                        #outcomes = MultiLabelBinarizer().fit_transform(outcomes)
                    else:
                        outcomes = np.array([d.split()[-1] for d in outcomes])
            self._outcomes = outcomes
        return self._outcomes

    def _load_statistics(self):
        pass