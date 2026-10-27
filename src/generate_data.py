
import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

# Keep the dataset reproducible
random.seed(42)

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# -----------------------------
# 1. Generate 200 enquiries
# -----------------------------
messages = [
    "I want to book an appointment",
    "Please cancel my appointment",
    "I have a question about my bill",
    "I need an appointment as soon as possible",
    "Can I reschedule my visit?",
    "What are your clinic timings?",
    "I want to know the consultation fee",
    "Please confirm my booking",
    "I need help with my appointment",
    "I have a billing issue"
]

channels = ["Website", "Email", "Phone", "WhatsApp"]

enquiries = []

start_date = datetime(2026, 1, 1)

for i in range(1, 201):
    enquiry_date = start_date + timedelta(days=random.randint(0, 270))

    enquiries.append({
        "enquiry_id": f"ENQ{i:03d}",
        "message": random.choice(messages),
        "date": enquiry_date.strftime("%Y-%m-%d"),
        "channel": random.choice(channels)
    })

enquiries_df = pd.DataFrame(enquiries)

# Add intentional data-quality issues
enquiries_df.loc[5, "message"] = None
enquiries_df.loc[12, "channel"] = None
enquiries_df.loc[20, "date"] = "27/08/2026"
enquiries_df.loc[25, "channel"] = "whatsapp"

# Add duplicate rows
enquiries_df = pd.concat(
    [enquiries_df, enquiries_df.iloc[[2, 8]]],
    ignore_index=True
)

enquiries_df.to_csv(
    DATA_DIR / "patient_enquiries.csv",
    index=False
)

# -----------------------------
# 2. Generate 300 appointments
# -----------------------------
doctors = [
    "Dr. Sharma",
    "Dr. Patil",
    "Dr. Mehta",
    "Dr. Joshi"
]

time_slots = [
    "Morning",
    "Afternoon",
    "Evening"
]

statuses = [
    "attended",
    "cancelled",
    "no-show"
]

appointments = []

for i in range(1, 301):
    appointment_date = start_date + timedelta(
        days=random.randint(0, 270)
    )

    appointments.append({
        "appointment_id": f"APT{i:03d}",
        "patient_id": f"PAT{random.randint(1, 180):03d}",
        "appointment_date": appointment_date.strftime("%Y-%m-%d"),
        "doctor": random.choice(doctors),
        "time_slot": random.choice(time_slots),
        "status": random.choice(statuses)
    })

appointments_df = pd.DataFrame(appointments)

# Add intentional data-quality issues
appointments_df.loc[10, "doctor"] = None
appointments_df.loc[15, "status"] = "No-Show"
appointments_df.loc[22, "appointment_date"] = "15/09/2026"
appointments_df.loc[30, "time_slot"] = "morning"

# Add duplicate rows
appointments_df = pd.concat(
    [appointments_df, appointments_df.iloc[[4, 9]]],
    ignore_index=True
)

appointments_df.to_csv(
    DATA_DIR / "appointments.csv",
    index=False
)

print("Synthetic datasets created successfully!")
print(f"Enquiries rows: {len(enquiries_df)}")
print(f"Appointment rows: {len(appointments_df)}")
print(f"Files saved in: {DATA_DIR}")
