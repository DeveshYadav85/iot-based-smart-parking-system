import os
import random
import time
from datetime import datetime, timedelta
import pandas as pd

ZONES = ["A", "B", "C", "D", "E"]
SLOTS_PER_ZONE = 4
TOTAL_SLOTS = 20

def generate_dataset(num_runs=200, output_path="/Users/deveshyadav/Desktop/smartparking_project/data/parking_dataset.csv"):
    print(f"Generating synthetic dataset with {num_runs} runs...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []
    base_time = datetime(2026, 1, 1, 8, 0, 0)
    for run_id in range(1, num_runs + 1):
        current_occupied = random.randint(2, 6)
        for step in range(192):
            ts = base_time + timedelta(days=run_id - 1, minutes=step * 2.5)
            hour_float = ts.hour + ts.minute / 60.0
            if 8.0 <= hour_float < 9.5:
                delta = random.choice([0, 1, 1, 2, -1])
            elif 9.5 <= hour_float < 12.0:
                delta = random.choice([0, 1, -1, 0, 0])
            elif 12.0 <= hour_float < 13.5:
                delta = random.choice([-1, -2, 1, 0, -1])
            elif 13.5 <= hour_float < 15.0:
                delta = random.choice([1, 0, 0, -1, 1])
            else:
                delta = random.choice([-1, -2, -1, 0])
            current_occupied = max(1, min(TOTAL_SLOTS, current_occupied + delta))
            zone_occ = {}
            remaining = current_occupied
            for z in ZONES:
                val = min(SLOTS_PER_ZONE, max(0, int(round(remaining / (len(ZONES) - ZONES.index(z)))) + random.choice([-1, 0, 1])))
                val = min(SLOTS_PER_ZONE, min(remaining, max(0, val)))
                zone_occ[z] = val
                remaining -= val
            if remaining > 0:
                for z in ZONES:
                    add = min(SLOTS_PER_ZONE - zone_occ[z], remaining)
                    zone_occ[z] += add
                    remaining -= add
                    if remaining <= 0: break
            rows.append({
                "run_id": run_id,
                "step": step,
                "timestamp": ts.isoformat(),
                "hour": ts.hour,
                "minute": ts.minute,
                "day_of_week": ts.weekday(),
                "total_occupied": current_occupied,
                "total_available": TOTAL_SLOTS - current_occupied,
                "occupancy_rate": round(current_occupied / TOTAL_SLOTS, 4),
                "zone_A_occ": zone_occ["A"],
                "zone_B_occ": zone_occ["B"],
                "zone_C_occ": zone_occ["C"],
                "zone_D_occ": zone_occ["D"],
                "zone_E_occ": zone_occ["E"]
            })
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")
    return df

if __name__ == "__main__":
    generate_dataset()
