import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("25_animals_entropy_summary.csv")
steps = sorted(df["step"].unique())

plt.figure(figsize=(7.8, 5.2))
for model in ["GPT 4.1", "Gemini 2.0 Flash", "Claude Haiku 4.5", "Oracle"]:
    d = df[df["model"] == model].sort_values("step")
    plt.errorbar(d["step"], d["entropy_bits_mean"], yerr=d["entropy_bits_std"],
                 fmt="-o", capsize=3, label=model)
plt.title("25 Animals Dataset: Entropy (in bits) Across Steps")
plt.xlabel("Step")
plt.ylabel("Entropy = log2 # of Remaining Options")
plt.xticks(steps)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("25_animals_entropy_plot.png", dpi=220)
print("Saved 25_animals_entropy_plot.png")
