#!/usr/bin/env python3
# Exact k-ary oracle via dynamic programming + per-turn curves.
# Dataset format: JSON mapping id -> {attr: value, ...}

import argparse, json, math
from functools import lru_cache
from typing import Dict, List, Any, Tuple

# ---------------- Utilities ----------------

def bitcount(x: int) -> int:
    return x.bit_count()

def ids_from_mask(mask: int, index2id: List[str]) -> List[str]:
    out, i = [], 0
    while mask:
        if mask & 1:
            out.append(index2id[i])
        mask >>= 1
        i += 1
    return out

# ---------------- Oracle ----------------

class KaryOracleDP:
    """
    Oracle for multi-valued (k-ary) attributes.
    Assumptions: uniform prior over objects, noiseless answers.
    """
    def __init__(self, objects: Dict[str, Dict[str, str]]):
        self.ids = sorted(objects.keys())
        self.n = len(self.ids)
        self.attrs = sorted({a for o in objects.values() for a in o.keys()})
        self.attr_vals = {a: sorted({objects[i].get(a) for i in self.ids}) for a in self.attrs}

        self.id2idx = {oid: k for k, oid in enumerate(self.ids)}
        self.idx2id = self.ids[:]

        # Precompute bitmasks for every (attr, value)
        self.mask_by_attr_val: Dict[str, Dict[str, int]] = {a: {} for a in self.attrs}
        for a in self.attrs:
            for v in self.attr_vals[a]:
                m = 0
                for oid in self.ids:
                    if objects[oid].get(a) == v:
                        m |= 1 << self.id2idx[oid]
                self.mask_by_attr_val[a][v] = m

        self.root = (1 << self.n) - 1
        self._best_attr: Dict[int, str] = {}

    # Split S into non-empty proper children for attribute a
    def _children(self, S: int, a: str) -> List[int]:
        kids = []
        for v, mv in self.mask_by_attr_val[a].items():
            sub = S & mv
            if sub != 0 and sub != S:
                kids.append(sub)
        return kids

    # Is S a leaf (|S|<=1 or no attribute yields a proper split)?
    def _is_leaf(self, S: int) -> bool:
        if bitcount(S) <= 1:
            return True
        for a in self.attrs:
            if len(self._children(S, a)) > 1:
                return False
        return True

    @lru_cache(maxsize=None)
    def optimal_cost(self, S: int) -> float:
        """Minimal expected queries from candidate mask S."""
        size = bitcount(S)
        if size <= 1:
            return 0.0

        best = float("inf")
        best_a = None
        for a in self.attrs:
            parts = self._children(S, a)
            if len(parts) <= 1:
                continue
            exp_res = 0.0
            for child in parts:
                exp_res += (bitcount(child) / size) * self.optimal_cost(child)
            cand = 1.0 + exp_res
            if cand < best:
                best, best_a = cand, a

        if best_a is None:
            # Irreducible equivalence class
            self._best_attr[S] = ""
            return 0.0

        self._best_attr[S] = best_a
        return best

    def build_optimal_tree(self, S: int = None) -> Dict[str, Any]:
        """Reconstruct one optimal tree."""
        if S is None:
            S = self.root
        size = bitcount(S)
        if size <= 1:
            return {"type": "leaf", "size": size, "ids": ids_from_mask(S, self.idx2id)}
        a = self._best_attr.get(S, "")
        if not a:
            return {"type": "leaf", "size": size, "ids": ids_from_mask(S, self.idx2id)}
        children = []
        for v, mv in self.mask_by_attr_val[a].items():
            child = S & mv
            if child == 0 or child == S:
                continue
            children.append({
                "value": v,
                "subset_size": bitcount(child),
                "subtree": self.build_optimal_tree(child)
            })
        return {"type": "node", "attribute": a, "size": size, "children": children}

    # --------- New: per-turn expected candidates and entropy curves ---------

    def expected_curve(self, max_turns: int = None) -> Dict[str, List[float]]:
        """
        Simulate the optimal policy as a distribution over states with absorbing leaves.
        Returns dict with lists aligned by dialog turn:
          - 'turn': [0, 1, ..., T]
          - 'E_candidates': E[|S_t|]
          - 'E_entropy_bits': E[log2 |S_t|]
          - 'leaf_mass': total probability mass already at leaves by turn t
        """
        # Ensure policy filled
        _ = self.optimal_cost(self.root)

        def entropy_bits(S: int) -> float:
            n = bitcount(S)
            return 0.0 if n <= 1 else math.log2(n)

        # Distribution over states at current turn: {mask -> prob}
        dist = {self.root: 1.0}
        turns, E_size, E_H, leaf_mass = [], [], [], []

        t = 0
        while True:
            # Record expectations at this turn
            turns.append(t)
            E_size.append(sum(p * bitcount(S) for S, p in dist.items()))
            E_H.append(sum(p * entropy_bits(S) for S, p in dist.items()))
            leaf_mass.append(sum(p for S, p in dist.items() if self._is_leaf(S)))

            # Stop if all mass is in leaves
            if leaf_mass[-1] >= 1.0 - 1e-12:
                break
            if max_turns is not None and t >= max_turns:
                break

            # Push distribution one step along the optimal policy
            next_dist: Dict[int, float] = {}
            for S, pS in dist.items():
                size = bitcount(S)
                if self._is_leaf(S):
                    # Absorbing
                    next_dist[S] = next_dist.get(S, 0.0) + pS
                    continue
                a = self._best_attr.get(S, "")
                if not a:
                    # Treat as absorbing if no split cached (safety)
                    next_dist[S] = next_dist.get(S, 0.0) + pS
                    continue
                parts = self._children(S, a)
                for child in parts:
                    w = pS * (bitcount(child) / size)
                    next_dist[child] = next_dist.get(child, 0.0) + w
            dist = next_dist
            t += 1

        return {
            "turn": turns,
            "E_candidates": E_size,
            "E_entropy_bits": E_H,
            "leaf_mass": leaf_mass
        }

# ---------------- CLI ----------------

def main():
    ap = argparse.ArgumentParser(description="Optimal k-ary oracle (DP) + per-turn curves")
    ap.add_argument("--dataset", required=True, help="JSON: {id: {attr: value}}")
    ap.add_argument("--save_tree", default=None, help="Optional JSON path for the optimal tree")
    ap.add_argument("--curve_csv", default=None, help="Optional CSV path for per-turn expectations")
    args = ap.parse_args()

    with open(args.dataset, "r") as f:
        objects = json.load(f)

    oracle = KaryOracleDP(objects)
    opt = oracle.optimal_cost(oracle.root)
    print(f"Objects: {oracle.n}, Attributes: {len(oracle.attrs)}")
    print(f"Optimal expected number of queries (uniform prior): {opt:.6f}")

    if args.save_tree:
        tree = oracle.build_optimal_tree()
        with open(args.save_tree, "w") as f:
            json.dump(tree, f, indent=2)
        print(f"Saved optimal tree to: {args.save_tree}")

    # Per-turn curve
    curve = oracle.expected_curve()
    print("\nPer-turn expectations (first few rows):")
    for i in range(min(6, len(curve['turn']))):
        print(f"t={curve['turn'][i]:2d}  "
              f"E[|S_t|]={curve['E_candidates'][i]:7.3f}  "
              f"E[H_t]={curve['E_entropy_bits'][i]:6.3f} bits  "
              f"leaf_mass={curve['leaf_mass'][i]:.3f}")

    if args.curve_csv:
        import csv
        with open(args.curve_csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["turn", "E_candidates", "E_entropy_bits", "leaf_mass"])
            for t, n, h, m in zip(curve["turn"], curve["E_candidates"], curve["E_entropy_bits"], curve["leaf_mass"]):
                w.writerow([t, n, h, m])
        print(f"Saved per-turn curve to: {args.curve_csv}")

if __name__ == "__main__":
    main()
