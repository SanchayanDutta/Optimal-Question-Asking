# 25_ANIMALS OQA Dataset

This package contains a 25-item ANIMALS attribute table and ready-to-use prompts for running Optimal Question Asking (OQA) API experiments.

## Contents
- `data/25_animals.json` — canonical boolean attribute table.
- `data/items.txt` — list of animal names.
- `data/attributes.txt` — list of attribute names.
- `data/equivalence_classes.json` — items grouped by identical attribute vectors.
- `metadata.json` — dataset metadata.
- `prompts/prompt_plain.txt` — plain-text game prompt.
- `prompts/prompt_strict_json.txt` — strict JSON-output prompt for programmatic evaluation.
- `prompts/prompt_system.txt` — a short system role to stabilize outputs.

## Game protocol
- Hidden target is sampled uniformly from `data/items.txt`.
- The agent asks yes/no questions about attributes. Answers are truthful and noise-free.
- The dialog ends when a single candidate (or a single equivalence class) remains.
- External tools are disallowed.

## Dataset stats
- Items: 25
- Attributes: 14
- Duplicates present: True
- Equivalence classes: 22

## Quickstart (pseudo)
1. Send `prompts/prompt_system.txt` as the system message.
2. Send `prompts/prompt_plain.txt` or `prompts/prompt_strict_json.txt` as the user message.
3. Loop:
   - Read the model's `question` (or parse it from text).
   - Answer "Yes"/"No" from `data/25_animals.json` given the hidden target.
   - Feed the answer back to the model.
   - Stop when only one candidate (or class) remains.

## Notes
- Attributes must be asked as yes/no questions, and only from `data/attributes.txt`.
- For API experiments, the strict JSON prompt simplifies parsing and scoring.
