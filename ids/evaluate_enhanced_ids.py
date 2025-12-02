#!/usr/bin/env python3
"""
Comprehensive evaluation of Enhanced IDS
Generates detailed metrics and comparison between signature and anomaly detection
"""

from enhanced_ids import EnhancedIDS
from scapy.all import rdpcap
from collections import defaultdict
import json
import time
import os

def evaluate_pcap(pcap_file, ids, test_name):
    """Evaluate IDS performance on a PCAP file"""
    if not os.path.exists(pcap_file):
        return None
    
    print(f"\n{'='*70}")
    print(f"Testing: {test_name}")
    print(f"{'='*70}")
    
    packets = rdpcap(pcap_file)
    print(f"Loaded: {len(packets)} packets")
    
    # Clear alerts
    ids.alerts = []
    ids.alert_counts = defaultdict(lambda: 0)
    
    # Process packets
    start_time = time.time()
    for pkt in packets:
        ids.packet_handler(pkt)
    end_time = time.time()
    
    # Calculate metrics
    processing_time = end_time - start_time
    throughput = len(packets) / processing_time if processing_time > 0 else 0
    
    # Categorize alerts
    signature_alerts = sum(ids.alert_counts.get(t, 0) for t in ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF'])
    anomaly_alerts = sum(ids.alert_counts.get(t, 0) for t in ['TRAFFIC_VOLUME_ANOMALY', 'BANDWIDTH_ANOMALY', 
                                                                'HIGH_PORT_ENTROPY', 'BURST_TRAFFIC'])
    
    results = {
        'test_name': test_name,
        'packets': len(packets),
        'processing_time': processing_time,
        'throughput': throughput,
        'total_alerts': len(ids.alerts),
        'signature_alerts': signature_alerts,
        'anomaly_alerts': anomaly_alerts,
        'alerts_by_type': dict(ids.alert_counts),
        'unique_alert_types': len(ids.alert_counts)
    }
    
    print(f"\nResults:")
    print(f"  Processing time: {processing_time:.3f}s")
    print(f"  Throughput: {throughput:.0f} pkt/s")
    print(f"  Total alerts: {len(ids.alerts)}")
    print(f"  - Signature-based: {signature_alerts}")
    print(f"  - Anomaly-based: {anomaly_alerts}")
    
    if ids.alert_counts:
        print(f"\n  Alert breakdown:")
        for alert_type, count in sorted(ids.alert_counts.items()):
            print(f"    {alert_type}: {count}")
    
    return results

def main():
    print("\n" + "="*70)
    print("🔬 COMPREHENSIVE IDS EVALUATION")
    print("Comparing signature-based vs anomaly-based detection")
    print("="*70)
    
    # Initialize IDS
    ids = EnhancedIDS(use_anomaly_detection=True)
    
    # Train on baseline
    baseline_file = '../pcaps/baseline_normal.pcap'
    if os.path.exists(baseline_file):
        ids.anomaly_detector.train_from_pcap(baseline_file)
    else:
        print("⚠️  Baseline not found, anomaly detection disabled")
        ids.use_anomaly_detection = False
    
    # Test cases
    test_cases = [
        ('../pcaps/normal.pcap', 'Normal Traffic'),
        ('../pcaps/portscan.pcap', 'Port Scan'),
        ('../pcaps/synflood.pcap', 'SYN Flood'),
        ('../pcaps/arpspoof.pcap', 'ARP Spoofing'),
        ('../pcaps/mixed_attack.pcap', 'Mixed Attacks'),
    ]
    
    all_results = []
    
    # Run evaluations
    for pcap_file, test_name in test_cases:
        result = evaluate_pcap(pcap_file, ids, test_name)
        if result:
            all_results.append(result)
    
    # Summary statistics
    print("\n" + "="*70)
    print("📊 EVALUATION SUMMARY")
    print("="*70)
    
    total_packets = sum(r['packets'] for r in all_results)
    total_alerts = sum(r['total_alerts'] for r in all_results)
    total_signature = sum(r['signature_alerts'] for r in all_results)
    total_anomaly = sum(r['anomaly_alerts'] for r in all_results)
    avg_throughput = sum(r['throughput'] for r in all_results) / len(all_results) if all_results else 0
    
    print(f"\n📈 Overall Statistics:")
    print(f"  Total packets processed: {total_packets}")
    print(f"  Total alerts generated: {total_alerts}")
    print(f"  - Signature-based detection: {total_signature} ({100*total_signature/max(total_alerts,1):.1f}%)")
    print(f"  - Anomaly-based detection: {total_anomaly} ({100*total_anomaly/max(total_alerts,1):.1f}%)")
    print(f"  Average throughput: {avg_throughput:.0f} pkt/s")
    
    # Detection capabilities
    print(f"\n✅ Detection Capabilities Demonstrated:")
    all_alert_types = set()
    for r in all_results:
        all_alert_types.update(r['alerts_by_type'].keys())
    
    signature_types = [t for t in all_alert_types if t in ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF']]
    anomaly_types = [t for t in all_alert_types if t not in signature_types]
    
    if signature_types:
        print(f"\n  Signature-Based:")
        for alert_type in sorted(signature_types):
            print(f"    ✓ {alert_type}")
    
    if anomaly_types:
        print(f"\n  Anomaly-Based:")
        for alert_type in sorted(anomaly_types):
            print(f"    ✓ {alert_type}")
    
    # Performance comparison table
    print(f"\n📋 Detailed Results Table:")
    print(f"\n{'Test Case':<20} {'Packets':>8} {'Alerts':>8} {'Signature':>10} {'Anomaly':>8} {'Throughput':>12}")
    print("-" * 70)
    
    for r in all_results:
        print(f"{r['test_name']:<20} {r['packets']:>8} {r['total_alerts']:>8} "
              f"{r['signature_alerts']:>10} {r['anomaly_alerts']:>8} {r['throughput']:>10.0f} p/s")
    
    # Save results
    output = {
        'summary': {
            'total_packets': total_packets,
            'total_alerts': total_alerts,
            'signature_alerts': total_signature,
            'anomaly_alerts': total_anomaly,
            'avg_throughput': avg_throughput
        },
        'detailed_results': all_results,
        'capabilities': {
            'signature_based': sorted(signature_types),
            'anomaly_based': sorted(anomaly_types)
        }
    }
    
    with open('evaluation_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Results saved to: evaluation_results.json")
    print("="*70)

if __name__ == "__main__":
    main()
