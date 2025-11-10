
#!/usr/bin/env python3
# Exact k-ary oracle via DP + per-turn expected candidates/entropy curves.

import argparse, json, math
from functools import lru_cache
from typing import Dict, List, Any

def bitcount(x: int) -> int:
    return x.bit_count()

class KaryOracleDP:
    def __init__(self, objects: Dict[str, Dict[str, str]]):
        self.ids = sorted(objects.keys())
        self.n = len(self.ids)
        self.attrs = sorted({a for o in objects.values() for a in o})
        self.attr_vals = {a: sorted({objects[i][a] for i in self.ids}) for a in self.attrs}
        self.id2idx = {oid: k for k, oid in enumerate(self.ids)}
        # Precompute bitmasks for (attr, value)
        self.M = {a: {} for a in self.attrs}
        for a in self.attrs:
            for v in self.attr_vals[a]:
                m = 0
                for oid in self.ids:
                    if objects[oid][a] == v:
                        m |= 1 << self.id2idx[oid]
                self.M[a][v] = m
        self.root = (1 << self.n) - 1
        self._best_attr: Dict[int, str] = {}

    def _children(self, S: int, a: str) -> List[int]:
        kids = []
        for v, mv in self.M[a].items():
            sub = S & mv
            if sub and sub != S:
                kids.append(sub)
        return kids

    def _is_leaf(self, S: int) -> bool:
        if bitcount(S) <= 1:
            return True
        for a in self.attrs:
            if len(self._children(S, a)) > 1:
                return False
        return True

    @lru_cache(maxsize=None)
    def optimal_cost(self, S: int) -> float:
        n = bitcount(S)
        if n <= 1:
            return 0.0
        best, best_a = float("inf"), None
        for a in self.attrs:
            parts = self._children(S, a)
            if len(parts) <= 1:
                continue
            exp_res = 0.0
            for child in parts:
                exp_res += (bitcount(child)/n) * self.optimal_cost(child)
            cand = 1.0 + exp_res
            if cand < best:
                best, best_a = cand, a
        if best_a is None:
            self._best_attr[S] = ""
            return 0.0
        self._best_attr[S] = best_a
        return best

    def expected_curve(self):
        """Return dict with lists: turn, E_candidates, E_entropy_bits, leaf_mass."""
        import math
        _ = self.optimal_cost(self.root)  # fill policy
        def H(S):
            n = bitcount(S)
            return 0.0 if n <= 1 else math.log2(n)

        dist = {self.root: 1.0}
        turns, E_n, E_H, leaf_mass = [], [], [], []
        t = 0
        while True:
            turns.append(t)
            E_n.append(sum(p*bitcount(S) for S, p in dist.items()))
            E_H.append(sum(p*H(S) for S, p in dist.items()))
            leaf_mass.append(sum(p for S, p in dist.items() if self._is_leaf(S)))
            if leaf_mass[-1] >= 1.0 - 1e-12:
                break
            next_dist = {}
            for S, pS in dist.items():
                n = bitcount(S)
                if self._is_leaf(S):
                    next_dist[S] = next_dist.get(S, 0.0) + pS
                    continue
                a = self._best_attr.get(S, "")
                if not a:
                    next_dist[S] = next_dist.get(S, 0.0) + pS
                    continue
                parts = self._children(S, a)
                for child in parts:
                    w = pS * (bitcount(child)/n)
                    next_dist[child] = next_dist.get(child, 0.0) + w
            dist = next_dist
            t += 1
        return {"turn": turns, "E_candidates": E_n, "E_entropy_bits": E_H, "leaf_mass": leaf_mass}

def main():
    ap = argparse.ArgumentParser(description="k-ary oracle with per-turn curves")
    ap.add_argument("--dataset", required=True, help="JSON mapping id -> {attr: value}")
    ap.add_argument("--save_tree", default=None, help="(unused in this compact build)")
    ap.add_argument("--curve_csv", default=None, help="CSV path to save per-turn expectations")
    args = ap.parse_args()

    with open(args.dataset, "r") as f:
        objects = json.load(f)

    eng = KaryOracleDP(objects)
    opt = eng.optimal_cost(eng.root)
    print(f"Objects: {eng.n}, Attributes: {len(eng.attrs)}")
    print(f"Optimal expected number of queries (uniform prior): {opt:.6f}")

    curve = eng.expected_curve()
    if args.curve_csv:
        import csv
        with open(args.curve_csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["turn","E_candidates","E_entropy_bits","leaf_mass"])
            for t, n, h, m in zip(curve["turn"], curve["E_candidates"], curve["E_entropy_bits"], curve["leaf_mass"]):
                w.writerow([t, f"{n:.6f}", f"{h:.6f}", f"{m:.6f}"])

if __name__ == "__main__":
    main()
