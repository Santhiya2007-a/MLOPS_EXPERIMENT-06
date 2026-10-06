import time

from prometheus_client import Gauge, start_http_server

from drift_detection import run_detection


# --------------------------------------------------
# Prometheus Metrics
# --------------------------------------------------

DRIFT_DETECTED = Gauge(
    "data_drift_detected",
    "Data drift status"
)

DRIFTED_COLUMNS = Gauge(
    "drifted_columns",
    "Number of drifted columns"
)

TOTAL_COLUMNS = Gauge(
    "total_columns",
    "Total columns checked"
)


# --------------------------------------------------
# Run Drift Detection
# --------------------------------------------------

def update_metrics():

    summary = run_detection()

    # Get number of drifted columns
    drifted_columns = int(
        summary["drifted_columns"]
    )

    # Total columns
    total_columns = int(
        summary["total_columns"]
    )

    # --------------------------------------------------
    # Determine overall drift
    #
    # If at least 50% of columns are drifted,
    # consider the dataset drifted.
    # --------------------------------------------------

    drift_detected = (
        drifted_columns / total_columns >= 0.5
    )

    # --------------------------------------------------
    # Update Prometheus metrics
    # --------------------------------------------------

    DRIFT_DETECTED.set(
        1 if drift_detected else 0
    )

    DRIFTED_COLUMNS.set(
        drifted_columns
    )

    TOTAL_COLUMNS.set(
        total_columns
    )

    print()
    print("========== PROMETHEUS METRICS ==========")
    print(
        f"data_drift_detected = "
        f"{1 if drift_detected else 0}"
    )
    print(
        f"drifted_columns = "
        f"{drifted_columns}"
    )
    print(
        f"total_columns = "
        f"{total_columns}"
    )
    print("=========================================")
    print()


# --------------------------------------------------
# Update metrics
# --------------------------------------------------

update_metrics()


# --------------------------------------------------
# Start HTTP Server
# --------------------------------------------------

start_http_server(8006)

print(
    "Metrics server running at:"
)

print(
    "http://localhost:8006/metrics"
)


# --------------------------------------------------
# Keep Server Running
# --------------------------------------------------

try:

    while True:
        time.sleep(5)

except KeyboardInterrupt:

    print(
        "\nMetrics server stopped."
    )