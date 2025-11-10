# OQA k-ary 300-object dataset

This package contains a 300-object multi-valued (k-ary) attribute dataset for Optimal Question Asking (OQA),
plus two exact oracle programs you can run in Google Colab to compute optimal expected queries and (optionally) per-turn entropy curves.

- Attributes: color, shape, material, size, pattern, origin, use_case, energy
- Each attribute takes at least two distinct values across the 300 objects
- Files mirror earlier tiers for drop-in use

Files
- oqa_kary300_schema.json
- oqa_kary300_dataset.json
- oqa_kary300_dataset.csv
- oqa_kary300_candidates.txt
- oqa_kary300_prompt.txt
- oqa_kary_oracle_dp.py        # subset-mask DP with optional per-turn curve CSV
- oqa_kary_oracle_dp_pa.py     # partial-assignment DP (often scales better for larger N)
