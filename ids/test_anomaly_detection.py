#!/usr/bin/env python3
"""
Test anomaly detection specifically on advanced attacks
"""

from enhanced_ids import EnhancedIDS
from scapy.all import rdpcap
import os

def test_anomaly_pcap(pcap_file, ids, test_name):
    """Test IDS anomaly detection"""
    print(f"\n{'='*70}")
    print(f"Testing: {test_name}")
    print(f"File: {os.path.basename(pcap_file)}")
    print(f"{'='*70}")
    
    if not os.path.exists(pcap_file):
        print(f"❌ File not found")
        return
    
    packets = rdpcap(pcap_file)
    print(f"Loaded: {len(packets)} packets\n")
    
    # Clear alerts
    ids.alerts = []
    ids.alert_counts = {}
    from collections import defaultdict
    ids.alert_counts = defaultdict(int)
    
    # Process (suppress packet output)
    for pkt in packets:
        ids.packet_handler(pkt)
    
    # Results
    signature_alerts = ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF']
    anomaly_alerts = ['TRAFFIC_VOLUME_ANOMALY', 'BANDWIDTH_ANOMALY', 
                      'HIGH_PORT_ENTROPY', 'BURST_TRAFFIC']
    
    sig_count = sum(ids.alert_counts.get(t, 0) for t in signature_alerts)
    anom_count = sum(ids.alert_counts.get(t, 0) for t in anomaly_alerts)
    
    print(f"\n📊 Results:")
    print(f"  Total alerts: {len(ids.alerts)}")
    print(f"  - Signature-based: {sig_count}")
    print(f"  - Anomaly-based: {anom_count}")
    
    if ids.alert_counts:
        print(f"\n  Alert types:")
        for alert_type, count in sorted(ids.alert_counts.items()):
            category = "📍 Signature" if alert_type in signature_alerts else "📈 Anomaly"
            print(f"    {category}: {alert_type} ({count})")
    
    # Show sample alerts
    if ids.alerts:
        print(f"\n  Sample alerts:")
        for alert in ids.alerts[:5]:
            print(f"    {alert}")

def main():
    print("\n" + "="*70)
    print("🧪 ANOMALY DETECTION TEST SUITE")
    print("Testing statistical anomaly detection capabilities")
    print("="*70)
    
    # Initialize with anomaly detection
    ids = EnhancedIDS(use_anomaly_detection=True)
    
    # Train on baseline
    baseline = '../pcaps/baseline_normal.pcap'
    if os.path.exists(baseline):
        ids.anomaly_detector.train_from_pcap(baseline)
    else:
        print("❌ Baseline not found!")
        return
    
    # Test advanced attacks
    tests = [
        ('../pcaps/volume_spike.pcap', 'Traffic Volume Spike'),
        ('../pcaps/entropy_scan.pcap', 'High-Entropy Port Scan'),
        ('../pcaps/burst_attack.pcap', 'Rapid Burst Attack'),
        ('../pcaps/bandwidth_attack.pcap', 'Bandwidth Anomaly'),
    ]
    
    results = {}
    for pcap_file, test_name in tests:
        test_anomaly_pcap(pcap_file, ids, test_name)
        results[test_name] = len(ids.alerts)
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 ANOMALY DETECTION SUMMARY")
    print(f"{'='*70}")
    
    print(f"\n✅ Anomaly Detection Capabilities:")
    all_anomaly_types = set()
    for alert in ids.alerts:
        for atype in ['TRAFFIC_VOLUME_ANOMALY', 'BANDWIDTH_ANOMALY', 
                      'HIGH_PORT_ENTROPY', 'BURST_TRAFFIC']:
            if atype in alert:
                all_anomaly_types.add(atype)
    
    if all_anomaly_types:
        for atype in sorted(all_anomaly_types):
            print(f"  ✓ {atype}")
    else:
        print("  ⚠️  No anomaly alerts generated (may need tuning)")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
