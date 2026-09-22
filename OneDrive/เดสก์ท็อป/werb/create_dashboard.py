#!/usr/bin/env python3
"""
Create lightweight HTML dashboard using Chart.js (CDN) - no pip install needed
"""
import csv
import json
from collections import defaultdict

# Read audit metrics
audit_data = []
with open('audit_metrics.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    audit_data = list(reader)

# Parse data
mode_counts = defaultdict(int)
result_counts = defaultdict(int)
status_counts = defaultdict(int)
rollback_count = 0
total = len(audit_data)
confidences = [float(r['confidence']) for r in audit_data]

for r in audit_data:
    mode_counts[r['mode']] += 1
    result_counts[r['result']] += 1
    status_counts[r['status']] += 1
    if r['rollback'] == 'true':
        rollback_count += 1

success_rate = (result_counts.get('success', 0) / total * 100) if total else 0

# Generate HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Featured Charts - Self-Healing Agent Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .metric-card h3 {{
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }}
        .metric-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        .metric-card.success .value {{ color: #10b981; }}
        .metric-card.warning .value {{ color: #f59e0b; }}
        .metric-card.danger .value {{ color: #ef4444; }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .chart-container h2 {{
            color: #333;
            font-size: 16px;
            margin-bottom: 15px;
        }}
        .chart-wrapper {{
            position: relative;
            height: 300px;
        }}
        
        .table-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            grid-column: 1 / -1;
        }}
        .table-container h2 {{
            color: #333;
            font-size: 16px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #f3f4f6;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #e5e7eb;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
        }}
        tr:hover {{
            background: #f9fafb;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Featured Charts - Self-Healing Agent Dashboard</h1>
            <p>Audit Metrics & Incident Tracking (Agent POC)</p>
        </div>
        
        <!-- Metrics Cards -->
        <div class="metrics">
            <div class="metric-card success">
                <h3>Total Incidents</h3>
                <div class="value">{total}</div>
            </div>
            <div class="metric-card success">
                <h3>Success Rate</h3>
                <div class="value">{success_rate:.1f}%</div>
            </div>
            <div class="metric-card danger">
                <h3>Rollback Events</h3>
                <div class="value">{rollback_count}</div>
            </div>
            <div class="metric-card warning">
                <h3>Avg Confidence</h3>
                <div class="value">{sum(confidences) / total if total else 0:.2f}</div>
            </div>
        </div>
        
        <!-- Charts -->
        <div class="dashboard">
            <!-- Chart 1: Incidents by Mode -->
            <div class="chart-container">
                <h2>Incidents by Mode</h2>
                <div class="chart-wrapper">
                    <canvas id="modeChart"></canvas>
                </div>
            </div>
            
            <!-- Chart 2: Results Distribution -->
            <div class="chart-container">
                <h2>Results Distribution</h2>
                <div class="chart-wrapper">
                    <canvas id="resultChart"></canvas>
                </div>
            </div>
            
            <!-- Chart 3: Status Distribution -->
            <div class="chart-container">
                <h2>Status Distribution</h2>
                <div class="chart-wrapper">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
            
            <!-- Chart 4: Confidence Breakdown -->
            <div class="chart-container">
                <h2>Agent Confidence Levels</h2>
                <div class="chart-wrapper">
                    <canvas id="confidenceChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Detailed Incident Table -->
        <div class="table-container">
            <h2>Incident Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Mode</th>
                        <th>Diagnosis</th>
                        <th>Status</th>
                        <th>Result</th>
                        <th>Rollback</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
"""

for r in audit_data:
    rollback_badge = "✓" if r['rollback'] == 'true' else "-"
    html += f"""
                    <tr>
                        <td>{r['time'][:10]}</td>
                        <td><strong>{r['mode']}</strong></td>
                        <td>{r['diagnosis_class']}</td>
                        <td>{r['status']}</td>
                        <td><strong>{r['result']}</strong></td>
                        <td>{rollback_badge}</td>
                        <td>{r['confidence']}</td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Self-Healing Data Agent POC • Dashboard Generated with Chart.js</p>
        </div>
    </div>
    
    <script>
        // Data
        const modeLabels = """ + json.dumps(list(mode_counts.keys())) + """;
        const modeData = """ + json.dumps(list(mode_counts.values())) + """;
        
        const resultLabels = """ + json.dumps(list(result_counts.keys())) + """;
        const resultData = """ + json.dumps(list(result_counts.values())) + """;
        
        const statusLabels = """ + json.dumps(list(status_counts.keys())) + """;
        const statusData = """ + json.dumps(list(status_counts.values())) + """;
        
        // Chart 1: Mode
        new Chart(document.getElementById('modeChart'), {
            type: 'bar',
            data: {
                labels: modeLabels,
                datasets: [{
                    label: 'Count',
                    data: modeData,
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb'],
                    borderColor: ['#667eea', '#764ba2', '#f093fb'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
        
        // Chart 2: Results
        new Chart(document.getElementById('resultChart'), {
            type: 'doughnut',
            data: {
                labels: resultLabels,
                datasets: [{
                    data: resultData,
                    backgroundColor: ['#10b981', '#ef4444', '#f59e0b']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });
        
        // Chart 3: Status
        new Chart(document.getElementById('statusChart'), {
            type: 'bar',
            data: {
                labels: statusLabels,
                datasets: [{
                    label: 'Count',
                    data: statusData,
                    backgroundColor: '#667eea',
                    borderColor: '#667eea',
                    borderWidth: 0
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { x: { beginAtZero: true } }
            }
        });
        
        // Chart 4: Confidence
        const confidences = """ + json.dumps(confidences) + """;
        const confidenceBuckets = {};
        confidences.forEach(c => {
            const bucket = Math.round(c * 10) / 10;
            confidenceBuckets[bucket] = (confidenceBuckets[bucket] || 0) + 1;
        });
        
        new Chart(document.getElementById('confidenceChart'), {
            type: 'line',
            data: {
                labels: Object.keys(confidenceBuckets),
                datasets: [{
                    label: 'Incident Count',
                    data: Object.values(confidenceBuckets),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    </script>
</body>
</html>
"""

# Write HTML
with open('dashboard_featured_charts.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Dashboard saved to: dashboard_featured_charts.html")
print(f"  Summary: {total} incidents, {success_rate:.1f}% success, {rollback_count} rollbacks")
