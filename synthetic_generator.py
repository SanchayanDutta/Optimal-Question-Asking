import itertools, random, json

def generate_synthetic_data():
    attributes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    data = {}
    for i, combo in enumerate(itertools.product([False, True], repeat=len(attributes))):
        data[f"{i:10x}"] = dict(zip(attributes, combo))
    return data

data = generate_synthetic_data()

def subset(n):
    keys = random.sample(list(data.keys()), n)
    return {k: data[k] for k in keys}

subset_25  = subset(25)
subset_100 = subset(100)

print(json.dumps(subset_25, indent=2, sort_keys=True))
print(json.dumps(subset_100, indent=2, sort_keys=True))
