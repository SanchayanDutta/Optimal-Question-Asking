import math

def build_decision_tree(possible_cars, data, memo=None):
    """Globally optimal yes-no tree that minimizes expected questions."""
    if memo is None:
        memo = {}

    if len(possible_cars) == 1:
        return {"type": "leaf", "cars": set(possible_cars)}

    key = frozenset(possible_cars)
    if key in memo:
        return memo[key]

    # All attributes present in this subset
    attributes = set()
    for car in possible_cars:
        attributes.update(data[car].keys())

    if not attributes:
        leaf = {"type": "leaf", "cars": set(possible_cars)}
        memo[key] = leaf
        return leaf

    n = len(possible_cars)
    best_subtree = None
    best_cost = float("inf")

    for attr in attributes:
        yes_set = {c for c in possible_cars if data[c][attr]}
        no_set = possible_cars - yes_set
        if not yes_set or not no_set:
            continue  # no split

        yes_sub = build_decision_tree(yes_set, data, memo)
        no_sub = build_decision_tree(no_set, data, memo)

        p_yes = len(yes_set) / n
        p_no = 1.0 - p_yes
        cost = (
            1.0
            + p_yes * compute_expected_cost(yes_sub, yes_set)
            + p_no * compute_expected_cost(no_sub, no_set)
        )

        if cost < best_cost:
            best_cost = cost
            best_subtree = {
                "type": "attribute",
                "attribute": attr,
                "yes": yes_sub,
                "no": no_sub,
            }

    if best_subtree is None:
        leaf = {"type": "leaf", "cars": set(possible_cars)}
        memo[key] = leaf
        return leaf

    memo[key] = best_subtree
    return best_subtree


def compute_expected_cost(tree, possible_cars):
    """Expected number of further questions under a uniform prior."""
    if tree["type"] == "leaf":
        return 0.0

    attr = tree["attribute"]
    yes_set = {c for c in possible_cars if cars[c][attr]}
    no_set = possible_cars - yes_set

    n = len(possible_cars)
    p_yes = len(yes_set) / n
    p_no = 1.0 - p_yes

    return (
        1.0
        + p_yes * compute_expected_cost(tree["yes"], yes_set)
        + p_no * compute_expected_cost(tree["no"], no_set)
    )


def ask_question(tree, hidden_car, possible_cars):
    """
    Traverse the tree, printing each question, its answer,
    the entropy drop and the remaining candidate count.
    """
    if tree["type"] == "leaf":
        candidates = tree["cars"]
        if len(candidates) == 1:
            print(f"Guessing: {next(iter(candidates))}")
        else:
            print("No further questions distinguish these. Candidates:")
            for c in candidates:
                print("  -", c)
        return candidates

    attr = tree["attribute"]
    yes_set = {c for c in possible_cars if cars[c][attr]}
    no_set = possible_cars - yes_set

    answer = cars[hidden_car][attr]
    next_set = yes_set if answer else no_set

    # Entropy before and after the question
    h_before = math.log2(len(possible_cars))
    h_after  = math.log2(len(next_set)) if next_set else 0.0
    info_gain = h_before - h_after

    print(f"Question: Is it '{attr}'?  Answer: {answer}")
    print(f"  Entropy drop: {info_gain:.3f} bits")
    print(f"  Remaining candidates: {len(next_set)}\n")   # new line

    return ask_question(
        tree["yes"] if answer else tree["no"],
        hidden_car,
        next_set
    )

if __name__ == "__main__":
    all_cars = set(cars.keys())
    decision_tree = build_decision_tree(all_cars, cars)

    hidden = "Mini Cooper"  # change as you like

    print("---- Decision Tree Query ----\n")
    final_candidates = ask_question(decision_tree, hidden, all_cars)

    print("Final candidates:", final_candidates)
    print("True car:", hidden)
