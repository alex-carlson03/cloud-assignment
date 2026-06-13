import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

DATA_PATH = "data/All_Diets.csv"

df = pd.read_csv(DATA_PATH)

macro_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]

# Clean missing numeric values using column averages
df[macro_cols] = df[macro_cols].fillna(df[macro_cols].mean())

# Avoid division by zero before creating ratios
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"].replace(0, np.nan)
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"].replace(0, np.nan)

avg_macros = df.groupby("Diet_type")[macro_cols].mean()
top_protein = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type").head(5)
highest_protein_diet = df.groupby("Diet_type")["Protein(g)"].mean().idxmax()
common_cuisines = df.groupby("Diet_type")["Cuisine_type"].agg(lambda x: x.value_counts().idxmax())

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Columns:", list(df.columns))

print("\nAverage macronutrients by diet type:")
print(avg_macros.round(2))

print("\nTop 5 protein-rich recipes for each diet type:")
print(top_protein[["Diet_type", "Recipe_name", "Cuisine_type", "Protein(g)"]].to_string(index=False))

print("\nDiet type with highest average protein:")
print(highest_protein_diet)

print("\nMost common cuisine for each diet type:")
print(common_cuisines)

# Create output folder charts
sns.set_theme(style="whitegrid")

avg_macros.plot(kind="bar", figsize=(10, 6))
plt.title("Average Macronutrients by Diet Type")
plt.ylabel("Average grams")
plt.xlabel("Diet Type")
plt.tight_layout()
plt.savefig("outputs/average_macros_bar.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.heatmap(avg_macros.round(2), annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Macronutrient Heatmap by Diet Type")
plt.tight_layout()
plt.savefig("outputs/macros_heatmap.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=top_protein,
    x="Cuisine_type",
    y="Protein(g)",
    hue="Diet_type"
)
plt.title("Top Protein-Rich Recipes by Cuisine")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("outputs/top_protein_scatter.png")
plt.close()

print("\nCharts saved in outputs folder.")
