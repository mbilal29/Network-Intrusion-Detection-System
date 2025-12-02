#!/usr/bin/env python3
"""
EVALUATION SCRIPT
Analyzes IDS performance and generates statistics
"""

from scapy.all import rdpcap
from simple_ids import SimpleIDS
import time
import json


def evaluate_pcap(pcap_file, attack_type):
    """Evaluate IDS performance on a PCAP file"""
    print(f"\n{'='*70}")
    print(f"📊 EVALUATING: {attack_type}")
    print(f"{'='*70}")
    
    # Clear previous alerts
    open('alerts.log', 'w').close()
    
    # Load packets
    packets = rdpcap(pcap_file)
    print(f"✅ Loaded {len(packets)} packets from {pcap_file}")
    
    # Create IDS instance
    ids = SimpleIDS()
    
    # Process packets and measure time
    start_time = time.time()
    alert_count = 0
    
    for packet in packets:
        ids.packet_handler(packet)
        # Count alerts by checking log file size change
    
    processing_time = time.time() - start_time
    
    # Read alerts
    try:
        with open('alerts.log', 'r') as f:
            alerts = f.readlines()
            alert_count = len(alerts)
    except FileNotFoundError:
        alerts = []
        alert_count = 0
    
    # Calculate metrics
    packets_per_second = len(packets) / processing_time if processing_time > 0 else 0
    detection_rate = (alert_count / len(packets)) * 100 if len(packets) > 0 else 0
    
    print(f"\n📈 METRICS:")
    print(f"  Total Packets: {len(packets)}")
    print(f"  Alerts Generated: {alert_count}")
    print(f"  Processing Time: {processing_time:.3f} seconds")
    print(f"  Throughput: {packets_per_second:.1f} packets/sec")
    print(f"  Detection Rate: {detection_rate:.2f}%")
    
    if alerts:
        print(f"\n🚨 ALERTS DETECTED:")
        for alert in alerts[:5]:  # Show first 5
            print(f"  {alert.strip()}")
        if len(alerts) > 5:
            print(f"  ... and {len(alerts)-5} more alerts")
    
    return {
        'attack_type': attack_type,
        'total_packets': len(packets),
        'alerts': alert_count,
        'processing_time': processing_time,
        'throughput': packets_per_second,
        'detection_rate': detection_rate
    }


def main():
    print("="*70)
    print("🔬 IDS EVALUATION SUITE")
    print("="*70)
    
    results = []
    
    # Evaluate each attack type
    test_cases = [
        ('../pcaps/portscan.pcap', 'Port Scan Attack'),
        ('../pcaps/synflood.pcap', 'SYN Flood Attack'),
        ('../pcaps/arpspoof.pcap', 'ARP Spoofing Attack'),
        ('../pcaps/normal.pcap', 'Normal Traffic (Baseline)'),
        ('../pcaps/mixed_attack.pcap', 'Mixed Attack Scenario')
    ]
    
    for pcap_file, attack_type in test_cases:
        try:
            result = evaluate_pcap(pcap_file, attack_type)
            results.append(result)
            time.sleep(0.5)  # Brief pause between tests
        except FileNotFoundError:
            print(f"⚠️  Warning: {pcap_file} not found")
        except Exception as e:
            print(f"❌ Error processing {pcap_file}: {e}")
    
    # Generate summary
    print("\n" + "="*70)
    print("📊 OVERALL EVALUATION SUMMARY")
    print("="*70)
    
    print(f"\n{'Attack Type':<30} {'Packets':<10} {'Alerts':<10} {'Detection %':<12}")
    print("-"*70)
    
    total_packets = 0
    total_alerts = 0
    
    for result in results:
        print(f"{result['attack_type']:<30} "
              f"{result['total_packets']:<10} "
              f"{result['alerts']:<10} "
              f"{result['detection_rate']:<12.2f}")
        total_packets += result['total_packets']
        total_alerts += result['alerts']
    
    print("-"*70)
    print(f"{'TOTALS':<30} {total_packets:<10} {total_alerts:<10}")
    
    # Calculate average throughput
    avg_throughput = sum(r['throughput'] for r in results) / len(results) if results else 0
    
    print(f"\n📈 PERFORMANCE METRICS:")
    print(f"  Total Packets Analyzed: {total_packets}")
    print(f"  Total Alerts Generated: {total_alerts}")
    print(f"  Average Throughput: {avg_throughput:.1f} packets/sec")
    if total_packets > 0:
        print(f"  Overall Detection Rate: {(total_alerts/total_packets*100):.2f}%")
    
    # Save results to JSON
    with open('evaluation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: evaluation_results.json")
    print("="*70)


if __name__ == '__main__':
    main()
