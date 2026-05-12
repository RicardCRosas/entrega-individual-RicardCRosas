import csv
import os

def build_dashboard_dom():
    import extract_summary_std
    cases = ['case_A', 'case_B', 'case_C']
    results = [extract_summary_std.get_metrics(c) for c in cases]
    
    table_rows = ""
    for r in results:
        if r:
            table_rows += f"<tr><td>{r['Case']}</td><td>{r['Initial Error']}</td><td>{r['Final Error']}</td><td>{r['Arrival Time (s)']}</td><td>{r['Distance Traveled']}</td><td>{r['Max Error']}</td><td>{r['Avg Error']}</td><td>{r['Max Velocity']}</td></tr>"
            
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: #111827; color: #fff; margin: 0; padding: 40px; }}
            .container {{ max-width: 1100px; margin: 0 auto; }}
            h1 {{ color: #60A5FA; text-align: center; margin-bottom: 30px; }}
            h2 {{ color: #E5E7EB; border-bottom: 1px solid #374151; padding-bottom: 10px; margin-top: 40px; }}
            .panel {{ background: #1F2937; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #374151; }}
            th {{ background-color: #374151; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
            .card {{ background: #1F2937; padding: 15px; border-radius: 10px; text-align: center; }}
            .card img {{ max-width: 100%; height: 250px; background: #fff; padding: 5px; border-radius: 5px; }}
            h3 {{ margin-top: 0; color: #D1D5DB; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ROS 2 Go to Goal - Metrics Dashboard</h1>
            
            <div class="panel">
                <h2>Comparative Statistics</h2>
                <table>
                    <thead>
                        <tr><th>Case</th><th>Initial Error</th><th>Final Error</th><th>Arrival Time (s)</th><th>Distance Traveled</th><th>Max Error</th><th>Avg Error</th><th>Max Velocity</th></tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>

            <div class="panel">
                <h2>Case C (Best Controller) Analysis</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Trajectory</h3>
                        <img src="metrics_results/case_C_trajectory.png" />
                    </div>
                    <div class="card">
                        <h3>Error vs Time</h3>
                        <img src="metrics_results/case_C_error_vs_time.png" />
                    </div>
                    <div class="card">
                        <h3>Linear Velocity</h3>
                        <img src="metrics_results/case_C_linear_velocity.png" />
                    </div>
                    <div class="card">
                        <h3>Angular Velocity</h3>
                        <img src="metrics_results/case_C_angular_velocity.png" />
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    with open('statistics_dom.html', 'w') as f:
        f.write(html)

build_dashboard_dom()
