#!/usr/bin/env python3
"""
Test IDS with PCAP files
Usage: python3 test_pcap.py <pcap_file>
"""

from simple_ids import SimpleIDS
from scapy.all import rdpcap
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_pcap.py <pcap_file>")
        print("\nExample:")
        print("  python3 test_pcap.py ../pcaps/portscan.pcap")
        sys.exit(1)
    
    pcap_file = sys.argv[1]
    
    if not os.path.exists(pcap_file):
        print(f"Error: File '{pcap_file}' not found")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🧪 IDS PCAP TESTING MODE")
    print("="*70)
    
    # Load packets
    print(f"\n📦 Loading packets from: {pcap_file}")
    try:
        packets = rdpcap(pcap_file)
        print(f"✅ Loaded {len(packets)} packets\n")
    except Exception as e:
        print(f"❌ Error loading PCAP: {e}")
        sys.exit(1)
    
    # Create IDS instance
    ids = SimpleIDS()
    
    # Process packets
    print("🔍 Analyzing packets...\n")
    for i, pkt in enumerate(packets):
        ids.packet_handler(pkt)
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(packets)} packets...", end='\r')
    
    print(f"\n✅ Processed {len(packets)} packets\n")
    
    # Print summary
    ids.print_summary()
    
    print("\n📄 Alerts saved to: alerts.log")
    print("="*70)

if __name__ == "__main__":
    main()
