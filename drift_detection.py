import json
from pathlib import Path

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


# --------------------------------------------------
# Columns to check for drift
# --------------------------------------------------

FEATURE_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)"
]


# --------------------------------------------------
# Drift detection function
# --------------------------------------------------

def run_detection():

    # Load reference data
    reference = pd.read_csv(
        DATA_DIR / "reference_data.csv"
    )

    # Load current data
    current = pd.read_csv(
        DATA_DIR / "current_data.csv"
    )

    # Select only the 4 feature columns
    reference_features = reference[FEATURE_COLUMNS]
    current_features = current[FEATURE_COLUMNS]

    # Create Evidently Data Drift Report
    report = Report(
        metrics=[
            DataDriftPreset(
                columns=FEATURE_COLUMNS,
                drift_share=0.5
            )
        ]
    )

    # Run comparison
    snapshot = report.run(
        current_features,
        reference_features
    )

    # Save HTML report
    snapshot.save_html(
        str(PROJECT_DIR / "drift_report.html")
    )

    # Convert report to dictionary
    result = snapshot.dict()

    # --------------------------------------------------
    # Find number of drifted columns
    # --------------------------------------------------

    drifted_columns = 0

    for metric in result.get("metrics", []):

        value = metric.get("value", {})

        if isinstance(value, dict):

            if "count" in value:
                drifted_columns = int(
                    value["count"]
                )

            if "number_of_drifted_columns" in value:
                drifted_columns = int(
                    value["number_of_drifted_columns"]
                )

    # --------------------------------------------------
    # Dataset drift
    # --------------------------------------------------

    total_columns = len(FEATURE_COLUMNS)

    drift_share = (
        drifted_columns / total_columns
    )

    # Data drift is detected when at least 50%
    # of the checked columns are drifted
    drift_detected = drift_share >= 0.5

    # --------------------------------------------------
    # Create summary
    # --------------------------------------------------

    summary = {
        "reference_rows": len(reference),
        "current_rows": len(current),
        "drift_detected": bool(drift_detected),
        "drifted_columns": drifted_columns,
        "total_columns": total_columns
    }

    # --------------------------------------------------
    # Save JSON summary
    # --------------------------------------------------

    with open(
        PROJECT_DIR / "drift_summary.json",
        "w"
    ) as file:

        json.dump(
            summary,
            file,
            indent=2
        )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print(
        f"Reference rows: {len(reference)}"
    )

    print(
        f"Current rows: {len(current)}"
    )

    print(
        f"Drift detected: "
        f"{'YES' if drift_detected else 'NO'}"
    )

    print(
        f"Drifted columns: {drifted_columns}"
    )

    print(
        f"Total columns: {total_columns}"
    )

    print(
        f"HTML report saved to: "
        f"{PROJECT_DIR / 'drift_report.html'}"
    )

    return summary


# --------------------------------------------------
# Run directly
# --------------------------------------------------

if __name__ == "__main__":
    run_detection()