import pandas as pd
import os
import math

def get_metrics(case_name):
    csv_path = f'metrics_results/{case_name}_metrics.csv'
    df = pd.read_csv(csv_path)
    
    initial_error = df['distance_error'].iloc[0]
    final_error = df['distance_error'].iloc[-1]
    arrival_time = df['time_s'].iloc[-1]
    
    # Distance traveled (approximate)
    dist = 0
    for i in range(1, len(df)):
        dx = df['x'].iloc[i] - df['x'].iloc[i-1]
        dy = df['y'].iloc[i] - df['y'].iloc[i-1]
        dist += math.sqrt(dx**2 + dy**2)
        
    max_error = df['distance_error'].max()
    avg_error = df['distance_error'].mean()
    max_velocity = max(df['linear_velocity'].max(), df['angular_velocity'].abs().max())
    
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
df_results = pd.DataFrame(results)
print(df_results.to_markdown(index=False))
