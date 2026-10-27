
import pandas as pd
from pathlib import Path

# Locate project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


def clean_text(value):
    """Standardize text casing and whitespace."""
    if pd.isna(value):
        return value
    return " ".join(str(value).strip().split())


def clean_dates(series):
    """Handle mixed date formats."""
    return pd.to_datetime(series, format="mixed", errors="coerce")


# ---------------------------------
# 1. Clean patient enquiries
# ---------------------------------
enquiries = pd.read_csv(DATA_DIR / "patient_enquiries.csv")

print("Enquiries before cleaning:", len(enquiries))

enquiries = enquiries.drop_duplicates()

enquiries["message"] = enquiries["message"].apply(clean_text)
enquiries["channel"] = enquiries["channel"].apply(clean_text)
enquiries["date"] = clean_dates(enquiries["date"])

# Fill missing values
enquiries["message"] = enquiries["message"].fillna("")
enquiries["channel"] = enquiries["channel"].fillna("Unknown")

# Standardize channel names
enquiries["channel"] = enquiries["channel"].str.title()

# Save cleaned data
enquiries.to_csv(
    OUTPUT_DIR / "cleaned_patient_enquiries.csv",
    index=False
)

print("Enquiries after cleaning:", len(enquiries))


# ---------------------------------
# 2. Clean appointments
# ---------------------------------
appointments = pd.read_csv(DATA_DIR / "appointments.csv")

print("\nAppointments before cleaning:", len(appointments))

appointments = appointments.drop_duplicates()

appointments["doctor"] = appointments["doctor"].apply(clean_text)
appointments["time_slot"] = appointments["time_slot"].apply(clean_text)
appointments["status"] = appointments["status"].apply(clean_text)

appointments["appointment_date"] = clean_dates(
    appointments["appointment_date"]
)

# Fill missing values
appointments["doctor"] = appointments["doctor"].fillna("Unknown")
appointments["time_slot"] = appointments["time_slot"].fillna("Unknown")
appointments["status"] = appointments["status"].fillna("unknown")

# Standardize values
appointments["time_slot"] = appointments["time_slot"].str.title()
appointments["status"] = appointments["status"].str.lower()

# Save cleaned data
appointments.to_csv(
    OUTPUT_DIR / "cleaned_appointments.csv",
    index=False
)

print("Appointments after cleaning:", len(appointments))

print("\nData cleaning completed successfully!")
print("Cleaned files saved in:", OUTPUT_DIR)
