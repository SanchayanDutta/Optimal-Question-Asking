# OQA k-ary 150-object dataset

This package contains a 150-object multi-valued (k-ary) attribute dataset for Optimal Question Asking (OQA),
plus an exact dynamic-program oracle with per-turn entropy curves.

- Attributes: color, shape, material, size, pattern, origin, use_case, energy
- Each attribute takes at least two distinct values across the 150 objects
- Greedy EIG baseline expected depth: 3.63 queries
- Exact oracle (uniform prior, noiseless): 3.58 queries

Files
- oqa_kary150_schema.json
- oqa_kary150_dataset.json
- oqa_kary150_dataset.csv
- oqa_kary150_candidates.txt
- oqa_kary150_greedy_tree.json
- oqa_kary_oracle_dp.py
- oqa_kary150_oracle_curve.csv
- oqa_kary150_oracle_entropy.png
