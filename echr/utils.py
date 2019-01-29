import os
from aenum import Enum

class Problem(Enum):
    binary     = 1
    multiclass = 2
    multilabel = 3

class Flavor(Enum):
    desc       = 1
    bow        = 2

__FLAVOR_TO_FILENAME = {
    Flavor.desc: 'descriptive',
    Flavor.bow:  'BoW'
}

def get_input_path():
    path = os.environ.get('ECHR_OD_PATH')
    if path is None:
        path = os.path.join(os.path.expanduser("~"), '.echr/echr_database/datasets_documents')
        path = path if os.path.isdir(path) else None
    if path is None:
        path = path if os.path.isdir('data') else None
    return path

def get_data_file_location(dataset, flavor):
    return os.path.join(get_input_path(), dataset, '{}.txt'.format(__FLAVOR_TO_FILENAME[flavor]))

def get_outcome_file_location(dataset):
    return os.path.join(get_input_path(), dataset, 'outcomes.txt')

def get_flavors_list():
    return [f for f in Flavor]
