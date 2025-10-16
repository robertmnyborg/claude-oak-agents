from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Generate Performance Dashboard

Creates HTML dashboard with charts showing agent performance.
"""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from datetime import datetime

def generate_dashboard():
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    # TODO: Use plotly or matplotlib to create charts
    # For now, generate simple HTML report

    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>OaK Agents Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .metric {{ background: #f0f0f0; padding: 20px; margin: 10px 0; border-radius: 5px; }}
        .agent {{ margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50; }}
    </style>
</head>
<body>
    <h1>Claude OaK Agents Dashboard</h1>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>

    <div class="metric">
        <h2>Summary</h2>
        <p>Total Invocations: {stats['total_invocations']}</p>
        <p>Unique Agents: {len(stats['agents'])}</p>
    </div>

    <h2>Agent Performance</h2>
'''

    for agent_name, agent_stats in sorted(stats['agents'].items(),
                                         key=lambda x: x[1]['invocation_count'],
                                         reverse=True):
        html += f'''
    <div class="agent">
        <h3>{agent_name}</h3>
        <p>Invocations: {agent_stats['invocation_count']}</p>
        <p>Success Rate: {agent_stats['success_rate']*100:.1f}%</p>
        <p>Average Quality: {agent_stats['average_quality']:.2f}/5.0</p>
        <p>Average Duration: {agent_stats['average_duration_seconds']:.0f}s</p>
    </div>
'''

    html += '''
</body>
</html>
'''

    output_file = PROJECT_ROOT / "reports" / f"dashboard_{datetime.now().strftime('%Y-%m-%d')}.html"
    with open(output_file, "w") as f:
        f.write(html)

    print(f"✓ Dashboard generated: {output_file}")
    print(f"  Open with: open {output_file}")

if __name__ == "__main__":
    generate_dashboard()
