from pathlib import Path
from sklearn.datasets import load_iris


# Project folder location
PROJECT_DIR = Path(__file__).resolve().parent

# Data folder location
DATA_DIR = PROJECT_DIR / "data"


# Load Iris dataset
iris = load_iris(as_frame=True)


# Create reference dataset
reference = iris.frame.rename(columns={"target": "species"})


# Convert target numbers into species names
reference["species"] = reference["species"].map(
    dict(enumerate(iris.target_names))
)


# Create a copy for current data
current = reference.copy()


# Introduce data drift
current["sepal length (cm)"] = (
    current["sepal length (cm)"] + 0.65
)

current["sepal width (cm)"] = (
    current["sepal width (cm)"] - 0.25
)

current["petal length (cm)"] = (
    current["petal length (cm)"] * 1.12
)


# Create data folder if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)


# Save reference data
reference.to_csv(
    DATA_DIR / "reference_data.csv",
    index=False
)


# Save current data
current.to_csv(
    DATA_DIR / "current_data.csv",
    index=False
)


# Display results
print(
    "Reference data created:",
    DATA_DIR / "reference_data.csv"
)

print(
    "Current data created:",
    DATA_DIR / "current_data.csv"
)

print("Rows generated: 150 reference, 150 current")