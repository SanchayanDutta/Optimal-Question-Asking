# 25_ANIMALS OQA Dataset

This package contains a 25‑item ANIMALS attribute table and ready‑to‑use prompts for running Optimal Question Asking (OQA) API experiments.

## Contents
- `data/25_animals.json` — canonical boolean attribute table.
- `data/items.txt` — list of animal names.
- `data/attributes.txt` — list of attribute names.
- `data/equivalence_classes.json` — items grouped by identical attribute vectors.
- `metadata.json` — dataset metadata.
- `prompts/prompt_plain.txt` — plain‑text game prompt.
- `prompts/prompt_strict_json.txt` — strict JSON‑output prompt for programmatic evaluation.
- `prompts/prompt_system.txt` — short system role to stabilize outputs.
- `plots/25_animals_entropy_summary.csv` — per‑step entropy means and standard deviations.
- `plots/25_animals_entropy_summary.json` — JSON version of the summary with a small metadata block.
- `plots/25_animals_entropy_seeds.csv` — 10 samples per model×step to illustrate variation.
- `plots/25_animals_entropy_plot.png` — line plot with error bars.
- `plots/make_plot.py` — script that recreates the figure from the CSV.
- `plots/README.txt` — short notes for the plots bundle.

> Note: The `plots` folder is optional and provided for convenience when reproducing figures.

## Game protocol
- Hidden target is sampled uniformly from `data/items.txt`.
- The agent asks yes/no questions about attributes. Answers are truthful and noise‑free.
- The dialog ends when a single candidate (or a single equivalence class) remains.
- External tools are disallowed.

## Dataset stats
- Items: 25  
- Attributes: 14  
- Duplicates present: True  
- Equivalence classes: 22

## Quickstart (pseudo)
1. Send `prompts/prompt_system.txt` as the system message.
2. Send `prompts/prompt_plain.txt` **or** `prompts/prompt_strict_json.txt` as the user message.
3. Loop:
   - Read the model’s question (or parse the JSON).
   - Answer “Yes” or “No” from `data/25_animals.json` given the hidden target.
   - Feed the answer back to the model.
   - Stop when only one candidate (or class) remains.

## Notes
- Questions must be yes/no and must refer to attributes in `data/attributes.txt`.
- For programmatic runs, the strict JSON prompt simplifies parsing and scoring.

## Plots bundle (optional)
If you want to reproduce the figure:
- Use `plots/make_plot.py` which reads the summary CSV in the same folder and writes `25_animals_entropy_plot.png`.
- `plots/25_animals_entropy_seeds.csv` contains 10 samples per model×step for variability analysis.
