# OQA k-ary 200-object dataset

This package contains a 200-object multi-valued (k-ary) attribute dataset for Optimal Question Asking (OQA),
plus an exact dynamic-program oracle with per-turn entropy curves.

- Attributes: color, shape, material, size, pattern, origin, use_case, energy
- Each attribute takes at least two distinct values across the 200 objects
- Greedy EIG baseline expected depth: 3.81 queries
- Exact oracle (uniform prior, noiseless): 3.76 queries

Files
- oqa_kary200_schema.json
- oqa_kary200_dataset.json
- oqa_kary200_dataset.csv
- oqa_kary200_candidates.txt
- oqa_kary200_greedy_tree.json
- oqa_kary_oracle_dp.py
- oqa_kary200_oracle_curve.csv
- oqa_kary200_oracle_entropy.png
