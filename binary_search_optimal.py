#!/usr/bin/env python3
"""
Binary-search guessing game
---------------------------
The program selects a secret integer in [1, 63] and then
pinpoints it by repeatedly asking questions of the form
“Is the number ≤ k?”.  Each answer is generated
internally—no user input is needed.

The log shows:
  • the current question,
  • the yes/no answer,
  • the remaining candidates.
"""

import random
from math import ceil, log2

def binary_search_game(N: int = 63, verbose: bool = True) -> int:
    secret = random.randint(1, N)
    low, high = 1, N
    turns = 0

    if verbose:
        print(f"Secret number (hidden): {secret}\n")

    while low < high:
        # Choose the midpoint so the two halves are as equal as possible
        k = (low + high) // 2
        turns += 1

        # Ask the comparator question
        question = f"Is the number ≤ {k}?"
        answer = "yes" if secret <= k else "no"

        if verbose:
            print(f"Q{turns}: {question}")
            print(f"A : {answer}")

        # Update the search interval
        if secret <= k:
            high = k
        else:
            low = k + 1

        if verbose:
            remaining = list(range(low, high + 1))
            print(f"Remaining candidates: {remaining}\n")

    if verbose:
        optimal_turns = ceil(log2(N))
        print(f"The number is {low} (found in {turns} questions; "
              f"optimal is {optimal_turns}).")

    return low  # the identified secret


if __name__ == "__main__":
    binary_search_game()
