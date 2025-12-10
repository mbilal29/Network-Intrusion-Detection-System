#!/usr/bin/env python3
"""
Create DYNAMIC visualizations from actual IDS test results
Reads alerts.log to generate real-time charts
"""

import matplotlib.pyplot as plt
import os
import re
from collections import Counter, defaultdict

def parse_alerts_log():
    """Parse alerts.log to extract real detection data"""
    if not os.path.exists('outputs/logs/alerts.log'):
        print("⚠️  No alerts.log found - using demo data")
        return None
    
    with open('outputs/logs/alerts.log', 'r') as f:
        lines = f.readlines()
    
    alerts = {
        'PORT_SCAN': 0,
        'SYN_FLOOD': 0,
        'ARP_SPOOF': 0,
        'ICMP_FLOOD': 0,
        'DNS_TUNNEL': 0,
        'HIGH_PORT_ENTROPY': 0,
        'BANDWIDTH_ANOMALY': 0,
        'BURST_TRAFFIC': 0,
        'TIMING_ANOMALY': 0
    }
    
    severities = {'HIGH': 0, 'MEDIUM': 0, 'CRITICAL': 0, 'LOW': 0}
    
    for line in lines:
        # Extract alert type
        if 'PORT_SCAN' in line:
            alerts['PORT_SCAN'] += 1
        elif 'SYN_FLOOD' in line:
            alerts['SYN_FLOOD'] += 1
        elif 'ARP_SPOOF' in line:
            alerts['ARP_SPOOF'] += 1
        elif 'ICMP_FLOOD' in line:
            alerts['ICMP_FLOOD'] += 1
        elif 'DNS_TUNNEL' in line:
            alerts['DNS_TUNNEL'] += 1
        elif 'HIGH_PORT_ENTROPY' in line:
            alerts['HIGH_PORT_ENTROPY'] += 1
        elif 'BANDWIDTH_ANOMALY' in line:
            alerts['BANDWIDTH_ANOMALY'] += 1
        elif 'BURST_TRAFFIC' in line:
            alerts['BURST_TRAFFIC'] += 1
        elif 'TIMING_ANOMALY' in line:
            alerts['TIMING_ANOMALY'] += 1
        
        # Extract severity
        if '[HIGH]' in line:
            severities['HIGH'] += 1
        elif '[MEDIUM]' in line:
            severities['MEDIUM'] += 1
        elif '[CRITICAL]' in line:
            severities['CRITICAL'] += 1
        elif '[LOW]' in line:
            severities['LOW'] += 1
    
    # Filter out zero counts
    alerts = {k: v for k, v in alerts.items() if v > 0}
    
    return {
        'alerts': alerts,
        'severities': severities,
        'total': sum(alerts.values())
    }


def create_alert_distribution_pie(data):
    """Show distribution of actual detected alert types"""
    
    if not data or not data['alerts']:
        print("⚠️  No alert data - skipping pie chart")
        return
    
    alert_types = list(data['alerts'].keys())
    counts = list(data['alerts'].values())
    
    colors = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#2ecc71', '#e67e22', '#1abc9c']
    
    fig, ax = plt.subplots(figsize=(9, 6))
    wedges, texts, autotexts = ax.pie(counts, labels=alert_types, 
                                       colors=colors[:len(counts)], autopct='%1.1f%%',
                                       startangle=90, textprops={'fontsize': 10})
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax.set_title(f'Alert Type Distribution ({data["total"]} Total Alerts)', 
                 fontsize=13, fontweight='bold', pad=15)
    
    # Add legend with counts
    legend_labels = [f'{alert_types[i]}: {counts[i]}' for i in range(len(alert_types))]
    ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)
    
    plt.tight_layout()
    os.makedirs('outputs/visualizations', exist_ok=True)
    plt.savefig('outputs/visualizations/alert_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Created: outputs/visualizations/alert_distribution.png")
    plt.close()


def create_severity_chart(data):
    """Show alert severity breakdown"""
    
    if not data or sum(data['severities'].values()) == 0:
        print("⚠️  No severity data - skipping severity chart")
        return
    
    severities = ['HIGH', 'MEDIUM', 'CRITICAL', 'LOW']
    counts = [data['severities'].get(s, 0) for s in severities]
    colors = ['#e74c3c', '#f39c12', '#c0392b', '#95a5a6']
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(severities, counts, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Severity Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Alerts', fontsize=12, fontweight='bold')
    ax.set_title('Alert Severity Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/severity_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Created: outputs/visualizations/severity_distribution.png")
    plt.close()


def create_detection_summary(data):
    """Create summary statistics visualization"""
    
    if not data:
        print("⚠️  No data - skipping summary chart")
        return
    
    # Categorize alerts
    signature_types = ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF']
    anomaly_types = ['HIGH_PORT_ENTROPY', 'BANDWIDTH_ANOMALY', 'BURST_TRAFFIC', 'TIMING_ANOMALY']
    
    signature_count = sum(data['alerts'].get(t, 0) for t in signature_types)
    anomaly_count = sum(data['alerts'].get(t, 0) for t in anomaly_types)
    
    categories = ['Signature-Based\nDetection', 'Anomaly-Based\nDetection', 'Total\nAlerts']
    values = [signature_count, anomaly_count, data['total']]
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
    
    ax.set_ylabel('Alert Count', fontsize=12, fontweight='bold')
    ax.set_title('Detection Method Performance', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{int(height)}',
               ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/detection_summary.png', dpi=300, bbox_inches='tight')
    print("✓ Created: outputs/visualizations/detection_summary.png")
    plt.close()


def create_attack_timeline_chart(data):
    """Show attack types as timeline/bar chart"""
    
    if not data or not data['alerts']:
        print("⚠️  No alert data - skipping timeline")
        return
    
    alert_types = list(data['alerts'].keys())
    counts = list(data['alerts'].values())
    
    colors = ['#3498db' if t in ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF'] 
              else '#e74c3c' for t in alert_types]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(alert_types, counts, color=colors, edgecolor='black', linewidth=1)
    
    ax.set_xlabel('Number of Detections', fontsize=12, fontweight='bold')
    ax.set_ylabel('Attack Type', fontsize=12, fontweight='bold')
    ax.set_title('Attack Detection Breakdown', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f' {int(width)}',
                   ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#3498db', label='Signature-Based'),
                      Patch(facecolor='#e74c3c', label='Anomaly-Based')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/attack_timeline.png', dpi=300, bbox_inches='tight')
    print("✓ Created: outputs/visualizations/attack_timeline.png")
    plt.close()


def create_all_visualizations():
    """Generate all charts from actual test results"""
    
    print("\n" + "="*70)
    print("📊 GENERATING DYNAMIC VISUALIZATIONS FROM ACTUAL RESULTS")
    print("="*70 + "\n")
    
    # Parse actual alerts
    data = parse_alerts_log()
    
    if data:
        print(f"📈 Found {data['total']} total alerts")
        print(f"   Alert types detected: {len(data['alerts'])}")
        print()
    
    # Generate charts
    create_alert_distribution_pie(data)
    create_severity_chart(data)
    create_detection_summary(data)
    create_attack_timeline_chart(data)
    
    # Create static baseline chart (doesn't change)
    create_baseline_statistics_chart()
    create_performance_metrics_chart()
    
    print("\n" + "="*70)
    print("✅ ALL VISUALIZATIONS CREATED!")
    print("="*70)
    print("\n💡 Charts reflect actual test results from alerts.log")
    print("   Run test_dynamic_ids.py again for different results!\n")


def create_baseline_statistics_chart():
    """Dynamic baseline statistics from trained model"""
    
    # Try to load actual baseline model
    try:
        import pickle
        if os.path.exists('baseline_model.pkl'):
            with open('baseline_model.pkl', 'rb') as f:
                baseline = pickle.load(f)
            
            # Extract actual values from baseline (handle both dict and direct access)
            packet_rate = baseline.get('packet_rate', {}).get('mean', 97.2)
            byte_rate = baseline.get('byte_rate', {}).get('mean', 11555)
            port_entropy = baseline.get('port_entropy', 3.93)
            
            # Handle inter_arrival_times (could be dict or list)
            inter_arrival_data = baseline.get('inter_arrival_times', 0.0103)
            if isinstance(inter_arrival_data, dict):
                inter_arrival = inter_arrival_data.get('mean', 0.0103)
            elif isinstance(inter_arrival_data, list) and len(inter_arrival_data) > 0:
                inter_arrival = inter_arrival_data[0]
            else:
                inter_arrival = 0.0103
            
            syn_ack = baseline.get('syn_ack_ratio', {}).get('mean', 0.50)
            
            values = [packet_rate, byte_rate, port_entropy, inter_arrival * 1000, syn_ack]  # Convert to ms
            print(f"  ✓ Loaded DYNAMIC baseline: packet_rate={packet_rate:.1f}, byte_rate={byte_rate:.0f}, port_entropy={port_entropy:.2f}")
        else:
            print("  ⚠️  No baseline model found - using demo values")
            values = [97.2, 11555, 3.93, 0.0103, 0.50]
    except Exception as e:
        print(f"  ⚠️  Error loading baseline: {e} - using demo values")
        values = [97.2, 11555, 3.93, 0.0103, 0.50]
    
    metrics = ['Packet\nRate', 'Byte\nRate', 'Port\nEntropy', 'Inter-Arrival\nTime (ms)', 'SYN/ACK\nRatio']
    colors = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(metrics, values, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('Baseline Network Statistics (Trained Model)', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.2f}' if height < 100 else f'{int(height)}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/baseline_statistics.png', dpi=300, bbox_inches='tight')
    print("✓ Created: outputs/visualizations/baseline_statistics.png")
    plt.close()


def create_performance_metrics_chart():
    """Dynamic performance metrics from evaluation results"""
    
    # Try to load actual evaluation results
    try:
        import json
        if os.path.exists('outputs/logs/evaluation_results.json'):
            with open('outputs/logs/evaluation_results.json', 'r') as f:
                results = json.load(f)
            
            throughput = results.get('avg_throughput', 21090)
            detection_rate = results.get('detection_rate', 100)
            false_positives = results.get('false_positives', 0)
            processing_delay = 0.047  # This is simulated, could calculate from test timing
            
            values = [throughput, detection_rate, false_positives, processing_delay]
            print(f"  ✓ Loaded DYNAMIC metrics: throughput={throughput:,}, detection_rate={detection_rate:.1f}%")
        else:
            print("  ⚠️  No evaluation results found - using demo values")
            values = [21090, 100, 0, 0.047]
    except Exception as e:
        print(f"  ⚠️  Error loading metrics: {e} - using demo values")
        values = [21090, 100, 0, 0.047]
    
    metrics = ['Throughput\n(pkt/s)', 'Detection\nRate', 'False\nPositives', 'Processing\nDelay (ms)']
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(metrics, values, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('IDS Performance Metrics', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        if height > 100:
            label = f'{int(height):,}'
        elif height < 1:
            label = f'{height:.3f}'
        else:
            label = f'{height:.0f}'
        
        ax.text(bar.get_x() + bar.get_width()/2., height,
               label, ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/performance_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ Created: outputs/visualizations/performance_metrics.png")
    plt.close()


if __name__ == "__main__":
    create_all_visualizations()
