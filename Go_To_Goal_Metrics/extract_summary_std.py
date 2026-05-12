import csv
import math
import os

def get_metrics(case_name):
    csv_path = f'metrics_results/{case_name}_metrics.csv'
    if not os.path.exists(csv_path):
        return None
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        return None
    
    initial_error = float(rows[0]['distance_error'])
    final_error = float(rows[-1]['distance_error'])
    arrival_time = float(rows[-1]['time_s'])
    
    dist = 0
    for i in range(1, len(rows)):
        dx = float(rows[i]['x']) - float(rows[i-1]['x'])
        dy = float(rows[i]['y']) - float(rows[i-1]['y'])
        dist += math.sqrt(dx**2 + dy**2)
        
    max_error = max(float(r['distance_error']) for r in rows)
    avg_error = sum(float(r['distance_error']) for r in rows) / len(rows)
    
    max_v = max(float(r['linear_velocity']) for r in rows)
    max_w = max(abs(float(r['angular_velocity'])) for r in rows)
    max_velocity = max(max_v, max_w)
    
    return {
        "Case": case_name,
        "Initial Error": f"{initial_error:.4f}",
        "Final Error": f"{final_error:.4f}",
        "Arrival Time (s)": f"{arrival_time:.4f}",
        "Distance Traveled": f"{dist:.4f}",
        "Max Error": f"{max_error:.4f}",
        "Avg Error": f"{avg_error:.4f}",
        "Max Velocity": f"{max_velocity:.4f}"
    }

cases = ['case_A', 'case_B', 'case_C']
results = [get_metrics(c) for c in cases]

print("| Case | Initial Error | Final Error | Arrival Time (s) | Distance Traveled | Max Error | Avg Error | Max Velocity |")
print("|---|---|---|---|---|---|---|---|")
for r in results:
    if r:
        print(f"| {r['Case']} | {r['Initial Error']} | {r['Final Error']} | {r['Arrival Time (s)']} | {r['Distance Traveled']} | {r['Max Error']} | {r['Avg Error']} | {r['Max Velocity']} |")
