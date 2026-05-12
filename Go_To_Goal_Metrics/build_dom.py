import csv
import os

def build_execution_dom():
    points = []
    with open('metrics_results/case_C_metrics.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            points.append([float(row['x']), float(row['y'])])
            
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; display: flex; justify-content: center; align-items: center; background: #333; height: 100vh; font-family: sans-serif; }}
            .window {{ width: 600px; height: 600px; background: #4556FF; border: 4px solid #555; border-radius: 10px; position: relative; overflow: hidden; }}
            .titlebar {{ background: #555; color: white; padding: 5px 10px; font-size: 14px; font-weight: bold; text-align: center; }}
            canvas {{ position: absolute; top: 30px; left: 0; }}
            .turtle {{ width: 40px; height: 40px; position: absolute; transform: translate(-50%, -50%); transition: top 0.1s, left 0.1s; z-index: 10; font-size: 30px; text-align: center; line-height: 40px; }}
        </style>
    </head>
    <body>
        <div class="window">
            <div class="titlebar">turtlesim - Case C (Best Controller)</div>
            <canvas id="canvas" width="600" height="570"></canvas>
            <div class="turtle" id="turtle">🐢</div>
        </div>
        <script>
            const points = {points};
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const turtle = document.getElementById('turtle');
            
            // Turtlesim coordinate system is typically 0 to 11.08, origin bottom-left
            function scale(p) {{
                const x = (p[0] / 11.08) * 600;
                const y = 570 - ((p[1] / 11.08) * 570);
                return [x, y];
            }}

            ctx.beginPath();
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 3;
            
            if(points.length > 0) {{
                let start = scale(points[0]);
                ctx.moveTo(start[0], start[1]);
                for(let i=1; i<points.length; i++) {{
                    let p = scale(points[i]);
                    ctx.lineTo(p[0], p[1]);
                }}
                ctx.stroke();
                
                let end = scale(points[points.length-1]);
                turtle.style.left = end[0] + 'px';
                turtle.style.top = (end[1] + 30) + 'px';
            }}
        </script>
    </body>
    </html>
    """
    with open('turtlesim_execution_dom.html', 'w') as f:
        f.write(html)

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
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white p-10 font-sans">
        <div class="max-w-6xl mx-auto">
            <h1 class="text-4xl font-bold mb-8 text-blue-400">ROS 2 Go to Goal - Metrics Dashboard</h1>
            
            <div class="bg-gray-800 p-6 rounded-xl shadow-lg mb-8">
                <h2 class="text-2xl font-semibold mb-4 text-gray-200">Comparative Statistics</h2>
                <div class="overflow-x-auto">
                    <table class="table-auto w-full text-left">
                        <thead>
                            <tr><th>Case</th><th>Initial Error</th><th>Final Error</th><th>Arrival Time (s)</th><th>Distance Traveled</th><th>Max Error</th><th>Avg Error</th><th>Max Velocity</th></tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <h2 class="text-2xl font-semibold mb-4 text-gray-200">Case C (Best Controller) Analysis</h2>
            <div class="grid grid-cols-2 gap-6">
                <div class="bg-gray-800 p-4 rounded-xl flex flex-col items-center">
                    <h3 class="text-lg font-medium mb-2">Trajectory</h3>
                    <img src="metrics_results/case_C_trajectory.png" class="max-h-64 rounded bg-white" />
                </div>
                <div class="bg-gray-800 p-4 rounded-xl flex flex-col items-center">
                    <h3 class="text-lg font-medium mb-2">Error vs Time</h3>
                    <img src="metrics_results/case_C_error_vs_time.png" class="max-h-64 rounded bg-white" />
                </div>
                <div class="bg-gray-800 p-4 rounded-xl flex flex-col items-center">
                    <h3 class="text-lg font-medium mb-2">Linear Velocity</h3>
                    <img src="metrics_results/case_C_linear_velocity.png" class="max-h-64 rounded bg-white" />
                </div>
                <div class="bg-gray-800 p-4 rounded-xl flex flex-col items-center">
                    <h3 class="text-lg font-medium mb-2">Angular Velocity</h3>
                    <img src="metrics_results/case_C_angular_velocity.png" class="max-h-64 rounded bg-white" />
                </div>
            </div>
        </div>
        <style>
            th {{ background-color: #374151; padding: 12px; border-bottom: 2px solid #4B5563; }}
            td {{ padding: 12px; border-bottom: 1px solid #374151; }}
        </style>
    </body>
    </html>
    """
    with open('statistics_dom.html', 'w') as f:
        f.write(html)

build_execution_dom()
build_dashboard_dom()
print("DOM files generated.")
