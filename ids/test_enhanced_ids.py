#!/usr/bin/env python3
"""
Test harness for Enhanced IDS with anomaly detection
Tests both signature-based and anomaly-based detection
"""

from enhanced_ids import EnhancedIDS
from scapy.all import rdpcap
import sys
import os

def test_ids_on_pcap(pcap_file, ids, test_name="Test"):
    """Test IDS on a PCAP file"""
    print("\n" + "=" * 70)
    print(f"🔍 {test_name}: {os.path.basename(pcap_file)}")
    print("=" * 70)
    
    if not os.path.exists(pcap_file):
        print(f"❌ File not found: {pcap_file}")
        return
    
    # Load packets
    try:
        packets = rdpcap(pcap_file)
        print(f"📦 Loaded {len(packets)} packets")
    except Exception as e:
        print(f"❌ Error loading PCAP: {e}")
        return
    
    # Clear previous alerts
    initial_alert_count = len(ids.alerts)
    
    # Process packets
    print("\n🔬 Processing packets...")
    for i, pkt in enumerate(packets):
        ids.packet_handler(pkt)
        if (i + 1) % 100 == 0:
            print(f"   Processed {i + 1}/{len(packets)} packets...")
    
    # Show results
    new_alerts = len(ids.alerts) - initial_alert_count
    print(f"\n✅ Processing complete: {new_alerts} new alerts generated")
    
    return new_alerts

def main():
    print("\n🛡️  ENHANCED IDS TEST SUITE")
    print("Testing both signature-based and anomaly-based detection")
    print("=" * 70)
    
    # Initialize IDS with anomaly detection
    ids = EnhancedIDS(use_anomaly_detection=True)
    
    # Train on baseline
    baseline_file = '../pcaps/baseline_normal.pcap'
    if os.path.exists(baseline_file):
        print("\n📚 Training Phase:")
        ids.anomaly_detector.train_from_pcap(baseline_file)
        ids.anomaly_detector.save_model('baseline_model.pkl')
    else:
        print(f"⚠️  Warning: Baseline file not found: {baseline_file}")
        print("Anomaly detection will not be available")
        ids.use_anomaly_detection = False
    
    # Test files
    test_cases = [
        ('../pcaps/normal.pcap', 'Normal Traffic (should have minimal alerts)'),
        ('../pcaps/portscan.pcap', 'Port Scan Attack'),
        ('../pcaps/synflood.pcap', 'SYN Flood Attack'),
        ('../pcaps/arpspoof.pcap', 'ARP Spoofing Attack'),
        ('../pcaps/mixed_attack.pcap', 'Mixed Attack Scenario'),
    ]
    
    results = {}
    
    print("\n" + "=" * 70)
    print("🧪 TESTING PHASE")
    print("=" * 70)
    
    for pcap_file, description in test_cases:
        if os.path.exists(pcap_file):
            alert_count = test_ids_on_pcap(pcap_file, ids, description)
            results[description] = alert_count
        else:
            print(f"\n⚠️  Skipping {description}: File not found")
            results[description] = 'N/A'
    
    # Final summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST RESULTS")
    print("=" * 70)
    
    ids.print_summary()
    
    print("\n📈 Test Results by Scenario:")
    for test_name, alert_count in results.items():
        print(f"  {test_name}: {alert_count} alerts")
    
    print("\n💡 Detection Capabilities:")
    print("  ✓ Signature-based detection (port scans, SYN floods, ARP spoofing)")
    print("  ✓ Anomaly-based detection (traffic volume, entropy, timing)")
    print("  ✓ Statistical modeling with baseline profiling")
    
    print("\n📝 Alerts saved to: alerts.log")
    print("=" * 70)

if __name__ == "__main__":
    main()
