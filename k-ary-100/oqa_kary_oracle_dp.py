
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oracle for k-ary Optimal Question Asking (OQA) with dynamic programming.

Given a finite set of objects labeled by multi-valued categorical attributes,
this program computes the minimal expected number of queries (under a uniform prior)
needed to identify the hidden object when each query reveals the exact value of a
chosen attribute. It also supports exporting the optimal decision tree.

This is the k-ary generalization of the binary oracle in Eq. (6)–(7) and Algorithm 1,
where a split can have m>2 branches (one per attribute value that appears in the
current candidate set).

Usage
-----
python oqa_kary_oracle_dp.py --dataset /path/to/oqa_kary100_dataset.json
# optional flags:
#   --schema /path/to/schema.json
#   --save_tree /path/to/tree.json

Output
------
Prints the optimal expected number of queries to stdout. If --save_tree is given,
also writes a JSON with the optimal decision tree.

Notes
-----
- Uniform prior over the candidate set is assumed.
- Observations are deterministic and noiseless.
- Each attribute need only be asked at most once, because a single k-ary query
  reveals its exact value; re-asking cannot further split the candidate set.

Complexity
----------
Let N be the number of objects and d the number of attributes. The DP caches by
reachable candidate subsets (represented as bitmasks), so the practical runtime
depends on how many distinct intersections of attribute-value buckets occur in the
dataset. For the 25- and 100-object tiers used in OQA, this is typically tractable.

Author: OQA k-ary oracle (DP)
"""

import argparse
import json
from functools import lru_cache
from typing import Dict, List, Tuple, Any

# ------------------ Utilities ------------------

def bit_count(x: int) -> int:
    return x.bit_count()

def ids_from_mask(mask: int, index2id: List[str]) -> List[str]:
    """Return object ids whose bit is 1 in mask."""
    out = []
    i = 0
    while mask:
        if mask & 1:
            out.append(index2id[i])
        mask >>= 1
        i += 1
    return out

# ------------------ Oracle ------------------

class KaryOracleDP:
    def __init__(self, objects: Dict[str, Dict[str, str]]):
        """
        objects: mapping id -> {attr: value}
        """
        self.ids = sorted(objects.keys())
        self.n = len(self.ids)
        self.attrs = sorted({a for obj in objects.values() for a in obj.keys()})
        # values per attribute that actually appear
        self.attr_values = {a: sorted({objects[i].get(a) for i in self.ids}) for a in self.attrs}

        # map id->index and precompute masks for every (attr, value)
        self.id2index = {oid: k for k, oid in enumerate(self.ids)}
        self.index2id = self.ids[:]  # same order

        self.mask_by_attr_val: Dict[str, Dict[str, int]] = {a: {} for a in self.attrs}
        for a in self.attrs:
            for v in self.attr_values[a]:
                m = 0
                for oid in self.ids:
                    if objects[oid].get(a) == v:
                        m |= (1 << self.id2index[oid])
                self.mask_by_attr_val[a][v] = m

        # root mask is all ones
        self.root_mask = (1 << self.n) - 1

        # will hold argmins for tree reconstruction
        self._best_attr: Dict[int, str] = {}

    def _children_for_attr(self, S: int, a: str) -> List[int]:
        """Return non-empty child masks when splitting S by attribute a."""
        children = []
        for v, mv in self.mask_by_attr_val[a].items():
            child = S & mv
            if child != 0 and child != S:  # must be a *proper* subset to contribute
                children.append(child)
        # Note: if child == S for some v, then all items in S share the same value for a,
        # which yields no split. We exclude it to avoid infinite recursion.
        return children

    @lru_cache(maxsize=None)
    def optimal_cost(self, S: int) -> float:
        """Minimal expected number of queries from candidate mask S."""
        size = bit_count(S)
        if size <= 1:
            return 0.0

        best_cost = float("inf")
        best_attr = None

        for a in self.attrs:
            parts = self._children_for_attr(S, a)
            if len(parts) <= 1:
                continue  # no split or trivial split

            # expected residual cost under uniform prior on S
            exp_res = 0.0
            for child in parts:
                exp_res += (bit_count(child) / size) * self.optimal_cost(child)
            cand = 1.0 + exp_res
            if cand < best_cost:
                best_cost = cand
                best_attr = a

        if best_attr is None:
            # No attribute can split S further (irreducible equivalence class).
            self._best_attr[S] = ""
            return 0.0

        self._best_attr[S] = best_attr
        return best_cost

    def build_optimal_tree(self, S: int = None) -> Dict[str, Any]:
        """Reconstruct the optimal decision tree as a nested dict."""
        if S is None:
            S = self.root_mask
        size = bit_count(S)
        if size <= 1:
            return {"type": "leaf", "size": size, "ids": ids_from_mask(S, self.index2id)}

        a = self._best_attr.get(S, None)
        if not a:
            # irreducible leaf (equivalence class)
            return {"type": "leaf", "size": size, "ids": ids_from_mask(S, self.index2id)}

        # group children by attribute value for readability
        children = []
        for v in self.attr_values[a]:
            child = S & self.mask_by_attr_val[a][v]
            if child == 0:
                continue
            if child == S:
                # all items share this value; shouldn't happen if _children_for_attr filtered correctly,
                # but guard to avoid loops
                continue
            subtree = self.build_optimal_tree(child)
            children.append({"value": v, "subset_size": bit_count(child), "subtree": subtree})

        return {"type": "node", "attribute": a, "size": size, "children": children}

# ------------------ CLI ------------------

def main():
    ap = argparse.ArgumentParser(description="Optimal k-ary oracle (DP) for OQA datasets")
    ap.add_argument("--dataset", required=True, help="Path to dataset JSON (id -> {attr: value})")
    ap.add_argument("--save_tree", default=None, help="Optional path to save the optimal tree JSON")
    args = ap.parse_args()

    with open(args.dataset, "r") as f:
        objects = json.load(f)

    oracle = KaryOracleDP(objects)
    opt = oracle.optimal_cost(oracle.root_mask)

    print(f"Objects: {oracle.n}, Attributes: {len(oracle.attrs)}")
    print(f"Optimal expected number of queries (uniform prior): {opt:.6f}")

    if args.save_tree:
        tree = oracle.build_optimal_tree()
        with open(args.save_tree, "w") as f:
            json.dump(tree, f, indent=2)
        print(f"Saved optimal tree to: {args.save_tree}")

if __name__ == "__main__":
    main()
