import pandas as pd
import os

# ------------------------------------------------------------------
# Data Quality Checker Function
# ------------------------------------------------------------------
def check_data_quality(df, required_columns, name="Dataset"):
    """
    Checks data quality of a DataFrame.
    Returns a dictionary with quality information.
    """
    quality_report = {}

    # 1) Missing columns
    missing = [c for c in required_columns if c not in df.columns]
    quality_report["missing_columns"] = missing

    # 2) Missing values per column
    quality_report["missing_values"] = df.isnull().sum().to_dict()

    # 3) Data types
    quality_report["dtypes"] = df.dtypes.astype(str).to_dict()

    # 4) Basic statistics
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    quality_report["basic_stats"] = df[numeric_cols].describe().to_dict()

    # 5) PLZ check
    if "PLZ" in df.columns:
        quality_report["invalid_PLZ"] = int(df[~df["PLZ"].between(10000, 14200)].shape[0])
    elif "plz" in df.columns:
        quality_report["invalid_PLZ"] = int(df[~df["plz"].between(10000, 14200)].shape[0])

    # 6) Latitude check
    if "Breitengrad" in df.columns:
        df["Breitengrad"] = pd.to_numeric(df["Breitengrad"], errors='coerce')
        quality_report["invalid_lat"] = int(df[(df["Breitengrad"] < -90) | (df["Breitengrad"] > 90)].shape[0])
    elif "lat" in df.columns:
        df["lat"] = pd.to_numeric(df["lat"], errors='coerce')
        quality_report["invalid_lat"] = int(df[(df["lat"] < -90) | (df["lat"] > 90)].shape[0])

    # 7) Longitude check
    if "Längengrad" in df.columns:
        df["Längengrad"] = pd.to_numeric(df["Längengrad"], errors='coerce')
        quality_report["invalid_lon"] = int(df[(df["Längengrad"] < -180) | (df["Längengrad"] > 180)].shape[0])
    elif "lon" in df.columns:
        df["lon"] = pd.to_numeric(df["lon"], errors='coerce')
        quality_report["invalid_lon"] = int(df[(df["lon"] < -180) | (df["lon"] > 180)].shape[0])

    # 8) Value distributions for numeric columns
    distributions = {}
    for col in numeric_cols:
        distributions[col] = df[col].value_counts().to_dict()
    quality_report["distributions"] = distributions

    return quality_report


# ------------------------------------------------------------------
# Helper function: display nicely
# ------------------------------------------------------------------
def display_quality_report(report, dataset_name="Dataset"):
    print(f"\n=== Data Quality Report: {dataset_name} ===\n")

    # Missing columns
    print("Missing Columns:")
    if report["missing_columns"]:
        print("  ", report["missing_columns"])
    else:
        print("  None ✅")

    # Missing values
    print("\nMissing Values per Column:")
    df_mv = pd.DataFrame.from_dict(report["missing_values"], orient='index', columns=['missing_values'])
    print(df_mv)

    # Data types
    print("\nData Types:")
    df_types = pd.DataFrame.from_dict(report["dtypes"], orient='index', columns=['dtype'])
    print(df_types)

    # Invalid PLZ / coordinates
    print("\nInvalid PLZ / Coordinates:")
    for key in ["invalid_PLZ", "invalid_lat", "invalid_lon"]:
        if key in report:
            print(f"  {key}: {report[key]}")

    # Basic stats
    print("\nBasic Statistics (numeric columns):")
    df_stats = pd.DataFrame(report["basic_stats"])
    print(df_stats)

    # Distributions (show top 5 values per column)
    print("\nValue Distributions (top 5 per numeric column):")
    for col, dist in report["distributions"].items():
        top5 = dict(sorted(dist.items(), key=lambda x: x[1], reverse=True)[:5])
        print(f"  {col}: {top5}")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Set working directory if needed
    currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(currentWorkingDirectory)

    # Load datasets
    df_lstat = pd.read_csv(os.path.join("..","datasets", "Ladesaeulenregister.csv"),
                           sep=';', encoding='latin-1', skiprows=10, header=0)
    df_residents = pd.read_csv(os.path.join("..", "datasets", "plz_einwohner.csv"),
                               encoding='latin-1')

    # Define required columns
    required_lstat = ["Postleitzahl", "Bundesland", "Breitengrad", "Längengrad",
                       "Nennleistung Ladeeinrichtung [kW]"]
    required_residents = ["plz", "einwohner", "lat", "lon"]

    # Check data quality
    quality_lstat = check_data_quality(df_lstat, required_lstat, name="Charging Stations")
    quality_resid = check_data_quality(df_residents, required_residents, name="Residents")

    # Display nicely
    display_quality_report(quality_lstat, "Charging Stations")
    display_quality_report(quality_resid, "Residents")
