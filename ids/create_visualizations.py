#!/usr/bin/env python3
"""
Create comprehensive visualizations for IDS performance and results
Generates charts and graphs for presentation and documentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import os
from collections import defaultdict

def create_detection_comparison_chart():
    """Compare signature vs anomaly detection across attack types"""
    
    # Data from our tests
    attacks = ['Normal', 'Port\nScan', 'SYN\nFlood', 'ARP\nSpoof', 'Mixed\nAttack', 'Entropy\nScan']
    signature_alerts = [0, 4, 1, 1, 3, 46]
    anomaly_alerts = [0, 0, 0, 0, 0, 8]
    
    x = range(len(attacks))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar([i - width/2 for i in x], signature_alerts, width, label='Signature-Based', color='#3498db')
    bars2 = ax.bar([i + width/2 for i in x], anomaly_alerts, width, label='Anomaly-Based', color='#e74c3c')
    
    ax.set_xlabel('Attack Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Alerts', fontsize=12, fontweight='bold')
    ax.set_title('IDS Detection Performance: Signature vs Anomaly-Based', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(attacks)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('detection_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: detection_comparison.png")
    plt.close()

def create_alert_distribution_pie():
    """Show distribution of alert types"""
    
    alert_types = ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF', 'HIGH_PORT_ENTROPY']
    counts = [50, 2, 1, 8]
    colors = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    explode = (0.05, 0.05, 0.05, 0.1)  # Emphasize entropy
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(counts, explode=explode, labels=alert_types, 
                                       colors=colors, autopct='%1.1f%%',
                                       startangle=90, textprops={'fontsize': 12})
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax.set_title('Alert Type Distribution Across All Tests', fontsize=14, fontweight='bold', pad=20)
    
    # Add legend with counts
    legend_labels = [f'{alert_types[i]}: {counts[i]} alerts' for i in range(len(alert_types))]
    ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
    
    plt.tight_layout()
    plt.savefig('alert_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Created: alert_distribution.png")
    plt.close()

def create_baseline_statistics_chart():
    """Visualize baseline traffic statistics"""
    
    # Baseline metrics
    metrics = ['Packet Rate\n(pkt/s)', 'Byte Rate\n(bytes/s)', 'Port Entropy', 'Inter-Arrival\n(ms)']
    means = [97.2, 11555, 3.93, 10.3]  # Last one converted to ms
    stds = [19.4, 3466, 0, 0]  # Simplified for visualization
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(metrics))
    bars = ax.bar(x, means, color=['#2ecc71', '#3498db', '#9b59b6', '#e67e22'], alpha=0.8, edgecolor='black')
    
    ax.set_xlabel('Baseline Metric', fontsize=12, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('Normal Traffic Baseline Statistics (1,052 packets)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
        height = bar.get_height()
        if std > 0:
            label = f'{mean:.1f}\n±{std:.1f}'
        else:
            label = f'{mean:.1f}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
               label, ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('baseline_statistics.png', dpi=300, bbox_inches='tight')
    print("✓ Created: baseline_statistics.png")
    plt.close()

def create_performance_metrics_chart():
    """Show throughput and processing performance"""
    
    test_cases = ['Normal\nTraffic', 'Port\nScan', 'SYN\nFlood', 'ARP\nSpoof', 'Mixed\nAttack']
    throughput = [35312, 15995, 19457, 12710, 21977]  # pkt/s
    packets = [50, 50, 200, 2, 197]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Throughput chart
    bars1 = ax1.bar(range(len(test_cases)), throughput, color='#3498db', alpha=0.8, edgecolor='black')
    ax1.set_xlabel('Test Case', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Throughput (packets/sec)', fontsize=11, fontweight='bold')
    ax1.set_title('Processing Throughput by Test Case', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(test_cases)))
    ax1.set_xticklabels(test_cases, fontsize=9)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Packets processed chart
    bars2 = ax2.bar(range(len(test_cases)), packets, color='#2ecc71', alpha=0.8, edgecolor='black')
    ax2.set_xlabel('Test Case', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Packets Processed', fontsize=11, fontweight='bold')
    ax2.set_title('Total Packets by Test Case', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(test_cases)))
    ax2.set_xticklabels(test_cases, fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('performance_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ Created: performance_metrics.png")
    plt.close()

def create_entropy_comparison():
    """Compare port entropy: normal vs attack"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Normal\nTraffic', 'Entropy\nScan Attack']
    entropy_values = [3.93, 5.91]
    colors = ['#2ecc71', '#e74c3c']
    
    bars = ax.bar(range(len(categories)), entropy_values, color=colors, alpha=0.8, edgecolor='black', width=0.5)
    
    # Add threshold line
    threshold = 4.0
    ax.axhline(y=threshold, color='orange', linestyle='--', linewidth=2, label=f'Detection Threshold ({threshold})')
    
    # Add anomaly zone
    ax.axhspan(threshold, 7, alpha=0.1, color='red', label='Anomaly Zone')
    
    ax.set_ylabel('Shannon Entropy', fontsize=12, fontweight='bold')
    ax.set_title('Port Entropy: Normal vs Attack Traffic', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 7)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels and status
    for i, (bar, val) in enumerate(zip(bars, entropy_values)):
        height = bar.get_height()
        status = '✓ Normal' if val < threshold else '⚠ Anomaly'
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
               f'{val:.2f}\n{status}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('entropy_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: entropy_comparison.png")
    plt.close()

def create_detection_timeline():
    """Show detection capabilities timeline"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Detection types and when they trigger
    detections = [
        ('Port Scan\n(Signature)', 0.5, '#3498db'),
        ('SYN Flood\n(Signature)', 1.0, '#3498db'),
        ('ARP Spoof\n(Signature)', 1.5, '#3498db'),
        ('High Entropy\n(Anomaly)', 2.0, '#e74c3c'),
        ('Volume Spike\n(Anomaly)', 2.5, '#e74c3c'),
        ('Timing Burst\n(Anomaly)', 3.0, '#e74c3c'),
    ]
    
    for i, (name, pos, color) in enumerate(detections):
        marker = 'o' if 'Signature' in name else '^'
        size = 200
        ax.scatter([pos], [0], s=size, c=color, marker=marker, alpha=0.8, edgecolors='black', linewidths=2)
        ax.text(pos, 0.3, name, ha='center', fontsize=9, fontweight='bold')
    
    ax.set_xlim(-0.2, 3.5)
    ax.set_ylim(-1, 1)
    ax.set_title('IDS Detection Capabilities', fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    # Add legend
    sig_patch = mpatches.Patch(color='#3498db', label='Signature-Based Detection')
    ano_patch = mpatches.Patch(color='#e74c3c', label='Anomaly-Based Detection')
    ax.legend(handles=[sig_patch, ano_patch], loc='lower center', fontsize=11, ncol=2)
    
    plt.tight_layout()
    plt.savefig('detection_capabilities.png', dpi=300, bbox_inches='tight')
    print("✓ Created: detection_capabilities.png")
    plt.close()

def create_all_visualizations():
    """Generate all visualization charts"""
    print("\n" + "="*70)
    print("📊 GENERATING VISUALIZATIONS FOR PRESENTATION")
    print("="*70 + "\n")
    
    create_detection_comparison_chart()
    create_alert_distribution_pie()
    create_baseline_statistics_chart()
    create_performance_metrics_chart()
    create_entropy_comparison()
    create_detection_timeline()
    
    print("\n✅ All visualizations created successfully!")
    print("   Files saved in current directory:")
    print("   - detection_comparison.png")
    print("   - alert_distribution.png")
    print("   - baseline_statistics.png")
    print("   - performance_metrics.png")
    print("   - entropy_comparison.png")
    print("   - detection_capabilities.png")
    print("\n💡 Use these in your presentation and report!")

if __name__ == "__main__":
    create_all_visualizations()
