# ECHR-OD loader

This project is a Python library to ease loading and manipulating the datasets provided by the European Court of Human Rights project.

# Installation

To install the dependencies:
```
pip install -r requirements.txt
```

The datasets are not provided with the library and you must manually download them. See [ECHR-OD](https://echr-opendata.eu).
The library will try to access the data in three different ways:

1. using the environment variable ```ECHR_OD_PATH```,
2. using the ECHR-OD standard installation path: ```~.echr/echr_database/datasets_documents```,
3. using the local path within the library source path: ```<echr_od_loader_path>/data```.

# Usage

The library is lazy by default and load in memory the datasets only when required.

```
dataset = echr.binary.get_dataset(article='1')  # Define the dataset model
X, y = dataset.load()  # Load in memory the dataset

# alternative syntax
X, y = dataset.X, dataset.y  # Explicit request to the data

# alternative syntax, useful to update the model (see below)
X = dataset.get_X()
y = dataset.get_y()

```

For multiclass and multilabel problem:
```
dataset = echr.multilabel.get_dataset()
X, y = dataset.load()

dataset = echr.multiclass.get_dataset()
X, y = dataset.load()

```

## Selecting and modifying the flavor

ECHR-OD datasets come in different flavors:

- Descriptive features
- Bag-of-Words

By default, ```get_dataset``` dataset define a model that will load all flavors. You can specify the one you want to select:
```
dataset = echr.binary.get_dataset(article='1', flavors=[echr.Flavor.desc])
dataset = echr.binary.get_dataset(article='1', flavors=[echr.Flavor.desc, echr.Flavor.bow])
dataset = echr.binary.get_dataset(article='1', flavors=None)  # Load all (default)
```

**REMARK:** loading the flavors is different from returning the dataset. When accessing the dataset, the different flavors will be stacked.

It is possible to access a specific flavor using ```get_X```:
```
X = dataset.get_X(echr.Flavor.bow)  # Works only if echr.Flavor.bow is in the flavors
```

It is possible to reset the flavors or to add new flavors at any moment:
```
dataset.set_flavors([echr.Flavor.desc])
dataset.add_flavor(echr.Flavor.desc)
```

You can check if a flavor is loaded:
```
dataset.is_loaded(echr.Flavor.desc)
```

## Preprocessing operators

It is possible to add preprocessing operations that will be applied when loaded a specific flavor.
The preprocessing operations must have the following signature ```data -> data``` where ```data``` is a list of list containing the raw features token from the dataset file.

Some preprocessing operators are provided such as ```filter``` to filter the features depending on a certain threshold of occurrences in the whole dataset.

The following example shows how to chain the registration of two preprocessing operator. The first one filter the feature of the descriptive flavors that appear only once while the second filter the token of the Bag-of-Word representation that appear less than 50 times in the whole corpus.

```
dataset = dataset.register_preprocess(
        echr.Flavor.desc, 
        partial(echr.preprocessing.filter, threshold=1)
    ).register_preprocess(
        echr.Flavor.bow, 
        partial(echr.preprocessing.filter, threshold=50)
    )
```


If you change the model, notably by registering new preprocessing operators, you must use ```force=True``` when requesting the data to update the part already loaded:
```
X = dataset.get_X(force=True)

# alternatively
X, y = dataset.load(force=True)
```