from collections import Counter 

def filter(data, threshold):
    counter = Counter(x for xs in data for x in set(xs))
    feature_count = {x : counter[x] for x in counter if counter[x] > threshold}
    data = [[f for f in x if f in feature_count] for x in data]
    stats = {
        'threshold': int(threshold),
        'before': len(counter),
        'after': len(feature_count),
        'ratio': len(feature_count) / (1. * len(counter))
    }
    print(stats)
    return data, stats
