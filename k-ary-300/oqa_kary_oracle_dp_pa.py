
#!/usr/bin/env python3
# Exact k-ary oracle via DP keyed by partial assignments (often scales better for large N).
import argparse, json, math
from functools import lru_cache
from typing import Dict, List, Any, Tuple

def bitcount(x: int) -> int: return x.bit_count()

class KaryOraclePA:
    """
    State is a tuple of length d with entries in {-1, 0..K_a-1}, where -1 means "unknown".
    Candidate set size is computed by intersecting precomputed bitmasks for assigned (a,v).
    """
    def __init__(self, objects: Dict[str, Dict[str, str]]):
        self.ids = sorted(objects.keys())
        self.n = len(self.ids)
        self.attrs = sorted({a for o in objects.values() for a in o})
        # Encode values per attribute with indices 0..K_a-1
        self.vals = {a: sorted({objects[i][a] for i in self.ids}) for a in self.attrs}
        self.val_index = {a: {v:i for i,v in enumerate(self.vals[a])} for a in self.attrs}
        self.id2idx = {oid: k for k, oid in enumerate(self.ids)}
        # Bitmasks for (a, value_index)
        self.M = {a: [0]*len(self.vals[a]) for a in self.attrs}
        for a in self.attrs:
            for v_idx, v in enumerate(self.vals[a]):
                m = 0
                for oid in self.ids:
                    if objects[oid][a] == v:
                        m |= 1 << self.id2idx[oid]
                self.M[a][v_idx] = m
        # Root state: all -1
        self.root_state = tuple([-1]*len(self.attrs))

    @lru_cache(maxsize=None)
    def mask_of(self, state: Tuple[int, ...]) -> int:
        """Compute candidate bitmask for a partial assignment state."""
        # Start with all candidates then intersect
        mask = (1 << self.n) - 1
        for a_idx, v_idx in enumerate(state):
            if v_idx >= 0:
                a = self.attrs[a_idx]
                mask &= self.M[a][v_idx]
                if mask == 0:
                    return 0
        return mask

    def _children_states(self, state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        """Return child states by assigning one new attribute value that yields a proper split."""
        S = self.mask_of(state)
        n = bitcount(S)
        kids = []
        if n <= 1: return kids
        # Try assigning any unassigned attribute
        for a_idx, v_idx in enumerate(state):
            if v_idx >= 0: 
                continue
            a = self.attrs[a_idx]
            # Consider only values that appear among current candidates
            for val_i, mv in enumerate(self.M[a]):
                child_mask = S & mv
                if child_mask and child_mask != S:
                    # New child state
                    child_state = list(state)
                    child_state[a_idx] = val_i
                    kids.append(tuple(child_state))
            # If at least one split exists on this attribute, others are not needed for branching at this step
            # (we still evaluate all attributes in the DP loop).
        return kids

    @lru_cache(maxsize=None)
    def optimal_cost(self, state: Tuple[int, ...]) -> float:
        S = self.mask_of(state)
        n = bitcount(S)
        if n <= 1: 
            return 0.0

        best = float("inf")
        # Evaluate each unassigned attribute as the next question
        for a_idx, v_idx in enumerate(state):
            if v_idx >= 0: 
                continue
            a = self.attrs[a_idx]
            # Build partitions only for values that appear and split
            parts = []
            for val_i, mv in enumerate(self.M[a]):
                child_mask = S & mv
                if child_mask and child_mask != S:
                    child_state = list(state)
                    child_state[a_idx] = val_i
                    parts.append( (child_mask, tuple(child_state)) )
            if len(parts) <= 1:
                continue
            exp_res = 0.0
            for child_mask, child_state in parts:
                w = bitcount(child_mask) / n
                exp_res += w * self.optimal_cost(child_state)
            cand = 1.0 + exp_res
            if cand < best:
                best = cand
        if best == float("inf"):
            return 0.0  # irreducible class
        return best

def main():
    ap = argparse.ArgumentParser(description="Exact k-ary oracle (partial-assignment DP)")
    ap.add_argument("--dataset", required=True, help="JSON mapping id -> {attr: value}")
    args = ap.parse_args()
    with open(args.dataset,"r") as f: objects = json.load(f)
    eng = KaryOraclePA(objects)
    opt = eng.optimal_cost(eng.root_state)
    print(f"Objects: {eng.n}, Attributes: {len(eng.attrs)}")
    print(f"Optimal expected number of queries (uniform prior): {opt:.6f}")

if __name__ == "__main__":
    main()
