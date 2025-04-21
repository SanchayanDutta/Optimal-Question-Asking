import math
from collections import defaultdict

animals = {
    "cat": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": False,
        "has_fur": True,
        "domestic": True,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": False
    },
    "dog": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": True,
        "has_fur": True,
        "domestic": True,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": False
    },
    "lion": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": True,
        "can_fly": False,
        "can_swim": False,
        "has_fur": True,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": False
    },
    "elephant": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": True,
        "can_fly": False,
        "can_swim": False,
        "has_fur": False,
        "domestic": False,
        "carnivore": False,
        "herbivore": True,
        "lays_eggs": False
    },
    "whale": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": True,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": False
    },
    "shark": {
        "mammal": False,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": True,
        "insect": False,
        "big": True,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    },
    "eagle": {
        "mammal": False,
        "bird": True,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": True,
        "can_swim": False,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    },
    "penguin": {
        "mammal": False,
        "bird": True,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    },
    "crocodile": {
        "mammal": False,
        "bird": False,
        "reptile": True,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": True,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    },
    "frog": {
        "mammal": False,
        "bird": False,
        "reptile": False,
        "amphibian": True,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    },
    "snake": {
        "mammal": False,
        "bird": False,
        "reptile": True,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    },
    "kangaroo": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": True,
        "can_fly": False,
        "can_swim": True,
        "has_fur": True,
        "domestic": False,
        "carnivore": False,
        "herbivore": True,
        "lays_eggs": False
    },
    "bat": {
        "mammal": True,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": True,
        "can_swim": False,
        "has_fur": True,
        "domestic": False,
        "carnivore": False,  # many bats eat insects, some eat fruit, so it's not strictly herbivore or carnivore
        "herbivore": False,
        "lays_eggs": False
    },
    "chicken": {
        "mammal": False,
        "bird": True,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": False,
        "has_fur": False,
        "domestic": True,
        "carnivore": False,
        "herbivore": False,
        "lays_eggs": True
    },
    "cuttlefish": {
        "mammal": False,
        "bird": False,
        "reptile": False,
        "amphibian": False,
        "fish": False,
        "insect": False,
        "big": False,
        "can_fly": False,
        "can_swim": True,
        "has_fur": False,
        "domestic": False,
        "carnivore": True,
        "herbivore": False,
        "lays_eggs": True
    }
}

def entropy(distribution):
    """
    Computes the Shannon entropy of a probability distribution (dict: item -> prob).
    distribution.values() should sum to 1.
    """
    return -sum(p * math.log2(p) for p in distribution.values() if p > 0)

def update_posterior(prior, attribute, answer, data):
    """
    Updates the prior distribution over animals given the question and answer.
    :param prior: dict of {animal: prior_prob}
    :param attribute: string, the asked attribute
    :param answer: bool, the returned answer
    :param data: dict of {animal -> {attribute -> bool}}
    :return: dict of {animal: posterior_prob}
    """
    # Posterior unnormalized: p(a | answer) ~ p(a) * P(answer | a)
    # P(answer | a) is 1 if data[a][attribute] == answer, else 0
    unnormalized_posterior = {}
    for animal, p in prior.items():
        if data[animal][attribute] == answer:
            unnormalized_posterior[animal] = p
        else:
            unnormalized_posterior[animal] = 0.0
    
    # Normalize
    total_prob = sum(unnormalized_posterior.values())
    if total_prob > 0:
        for animal in unnormalized_posterior:
            unnormalized_posterior[animal] /= total_prob
    else:
        # If total_prob == 0, it means no animal matched the answer
        # (this might indicate inconsistent data or prior).
        # We'll keep the distribution uniform among possible animals.
        n = len(prior)
        for animal in unnormalized_posterior:
            unnormalized_posterior[animal] = 1.0 / n
    
    return unnormalized_posterior

def expected_information_gain(prior, attribute, data):
    """
    Computes the expected information gain of asking about a particular attribute.
    :param prior: current distribution over animals
    :param attribute: the candidate attribute to ask
    :param data: dict of {animal -> {attribute -> bool}}
    :return: float, the expected information gain
    """
    current_entropy = entropy(prior)
    
    # Probability that the answer is True or False
    p_true = sum(prior[a] for a in prior if data[a][attribute])
    p_false = 1 - p_true
    
    # Entropy if the answer is True
    if p_true > 0:
        posterior_true = update_posterior(prior, attribute, True, data)
        entropy_true = entropy(posterior_true)
    else:
        entropy_true = 0
    
    # Entropy if the answer is False
    if p_false > 0:
        posterior_false = update_posterior(prior, attribute, False, data)
        entropy_false = entropy(posterior_false)
    else:
        entropy_false = 0
    
    # Expected posterior entropy
    expected_posterior_entropy = p_true * entropy_true + p_false * entropy_false
    
    # Expected information gain
    return current_entropy - expected_posterior_entropy

def select_best_attribute(prior, data, asked_attributes):
    """
    Selects the attribute with the maximum expected information gain.
    :param prior: current distribution over animals
    :param data: dict of {animal -> {attribute -> bool}}
    :param asked_attributes: set of attributes we've already asked about
    :return: (best_attribute, best_ig)
    """
    # Gather all possible attributes
    all_attributes = set()
    for a in data:
        all_attributes.update(data[a].keys())
    
    # Filter out attributes we've already asked
    candidate_attributes = [attr for attr in all_attributes if attr not in asked_attributes]
    if not candidate_attributes:
        return None, 0.0
    
    best_attribute = None
    best_ig = -float('inf')
    for attribute in candidate_attributes:
        ig = expected_information_gain(prior, attribute, data)
        if ig > best_ig:
            best_ig = ig
            best_attribute = attribute
    
    return best_attribute, best_ig

def bilevel_solver(hidden_animal, data):
    """
    Runs the bilevel (active) question-asking strategy until we reach a confident guess.
    :param hidden_animal: the correct animal to guess
    :param data: dict of {animal -> {attribute -> bool}}
    """
    # Initialize posterior to uniform
    n = len(data)
    prior = {animal: 1.0 / n for animal in data}
    
    asked_attributes = set()
    step = 1
    
    while True:
        top_animal = max(prior, key=prior.get)
        
        # Print current belief state
        print(f"\nStep {step} - Current belief distribution:")
        for a in sorted(prior.keys(), key=lambda x: prior[x], reverse=True):
            print(f"  {a}: {prior[a]:.3f}")
        
        # If we're very confident, guess
        if prior[top_animal] > 0.99:
            print(f"Confident guess: '{top_animal}' with probability {prior[top_animal]:.2f}")
            break
        
        # Choose best attribute to ask
        attribute, ig = select_best_attribute(prior, data, asked_attributes)
        if attribute is None:
            # No more attributes to ask, guess the most probable
            print(f"No more attributes to ask. Final guess: {top_animal}")
            break
        
        asked_attributes.add(attribute)
        
        # Simulate the environment's answer
        answer = data[hidden_animal][attribute]
        print(f"Asking about '{attribute}' (expected IG={ig:.4f}). Answer: {answer}")
        
        # Update posterior
        prior = update_posterior(prior, attribute, answer, data)
        step += 1
    
    final_guess = max(prior, key=prior.get)
    print(f"\nFinal guess: {final_guess} (prob={prior[final_guess]:.2f})")
    print(f"True animal: {hidden_animal}")

if __name__ == "__main__":
    # Example usage
    hidden = "cuttlefish"
    bilevel_solver(hidden, animals)
