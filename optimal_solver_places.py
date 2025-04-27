import math

# ---------- Decision tree construction ----------

def build_decision_tree(possible_items, data, memo=None):
    """Globally optimal yes-no tree that minimizes expected questions."""
    if memo is None:
        memo = {}

    if len(possible_items) == 1:
        return {"type": "leaf", "items": set(possible_items)}

    key = frozenset(possible_items)
    if key in memo:
        return memo[key]

    # Gather every attribute that appears in this subset
    attributes = set()
    for item in possible_items:
        attributes.update(data[item].keys())

    if not attributes:
        leaf = {"type": "leaf", "items": set(possible_items)}
        memo[key] = leaf
        return leaf

    n = len(possible_items)
    best_subtree = None
    best_cost = float("inf")

    for attr in attributes:
        yes_set = {i for i in possible_items if data[i][attr]}
        no_set = possible_items - yes_set
        if not yes_set or not no_set:
            continue  # attribute gives no split

        yes_sub = build_decision_tree(yes_set, data, memo)
        no_sub = build_decision_tree(no_set, data, memo)

        p_yes = len(yes_set) / n
        p_no = 1.0 - p_yes
        cost = 1.0 + p_yes * expected_cost(yes_sub, yes_set, data) \
                    + p_no  * expected_cost(no_sub, no_set, data)

        if cost < best_cost:
            best_cost = cost
            best_subtree = {
                "type": "attribute",
                "attribute": attr,
                "yes": yes_sub,
                "no": no_sub,
            }

    if best_subtree is None:
        leaf = {"type": "leaf", "items": set(possible_items)}
        memo[key] = leaf
        return leaf

    memo[key] = best_subtree
    return best_subtree


def expected_cost(tree, possible_items, data):
    """Expected number of further questions under a uniform prior."""
    if tree["type"] == "leaf":
        return 0.0

    attr = tree["attribute"]
    yes_set = {i for i in possible_items if data[i][attr]}
    no_set = possible_items - yes_set

    n = len(possible_items)
    p_yes = len(yes_set) / n
    p_no = 1.0 - p_yes

    return 1.0 + p_yes * expected_cost(tree["yes"], yes_set, data) \
               + p_no  * expected_cost(tree["no"],  no_set,  data)


# ---------- Interactive querying ----------

def ask_question(tree, hidden_item, possible_items, data):
    """
    Walk the tree, printing each question, its answer and
    the entropy drop achieved by that question.
    """
    if tree["type"] == "leaf":
        candidates = tree["items"]
        if len(candidates) == 1:
            print(f"Guessing: {next(iter(candidates))}")
        else:
            print("No further questions distinguish these. Candidates:")
            for i in candidates:
                print("  -", i)
        return candidates

    attr = tree["attribute"]
    yes_set = {i for i in possible_items if data[i][attr]}
    no_set = possible_items - yes_set

    answer = data[hidden_item][attr]
    next_set = yes_set if answer else no_set

    # Information gain
    h_before = math.log2(len(possible_items))
    h_after = math.log2(len(next_set)) if next_set else 0.0
    info_gain = h_before - h_after

    print(f"Question: Is it '{attr}'?  Answer: {answer}")
    print(f"  Entropy drop: {info_gain:.3f} bits\n")

    return ask_question(tree["yes"] if answer else tree["no"],
                        hidden_item,
                        next_set,
                        data)


# ---------- Demo ----------

if __name__ == "__main__":
    # 'places' must be defined elsewhere before running this script
    all_places = set(places.keys())
    decision_tree = build_decision_tree(all_places, places)

    hidden = "Rome"     # choose any key from the 'places' dict

    print("---- Decision Tree Query ----\n")
    final_candidates = ask_question(decision_tree, hidden, all_places, places)

    print("Final candidates:", final_candidates)
    print("True place:", hidden)
