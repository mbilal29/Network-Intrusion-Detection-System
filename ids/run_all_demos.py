#!/usr/bin/env python3
"""
Quick Demo Script - Runs all 4 attack demonstrations
Perfect for showcasing IDS capabilities
"""

import os
import sys
from scapy.all import IP, TCP, ICMP, DNS, DNSQR, wrpcap, rdpcap
import random
from enhanced_ids import EnhancedIDS


def demo_port_scan():
    """Demo 1: Port Scan"""
    print("\n" + "="*70)
    print("  🎯 DEMO 1: PORT SCAN ATTACK")
    print("="*70)
    
    print("\n📡 Generating nmap-style port scan (ports 1-100)...")
    packets = []
    attacker = "192.168.1.50"
    target = "192.168.1.100"
    
    for port in range(1, 101):
        pkt = IP(src=attacker, dst=target) / TCP(sport=20, dport=port, flags="S")
        packets.append(pkt)
    
    wrpcap('../pcaps/demo_port_scan.pcap', packets)
    print(f"✓ Generated {len(packets)} packets")
    
    print("\n🔍 Analyzing with IDS...")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False
    for pkt in packets:
        ids.packet_handler(pkt)
    
    print(f"\n🚨 DETECTED: {len(ids.alerts)} alerts")
    if ids.alerts:
        print(f"   • {ids.alerts[0]}")
        if len(ids.alerts) > 1:
            print(f"   ... and {len(ids.alerts)-1} more")
    

def demo_syn_flood():
    """Demo 2: SYN Flood"""
    print("\n" + "="*70)
    print("  🌊 DEMO 2: SYN FLOOD ATTACK")
    print("="*70)
    
    print("\n📡 Generating SYN flood (100 packets to port 80)...")
    packets = []
    attacker = "192.168.1.50"
    target = "192.168.1.100"
    
    for i in range(100):
        pkt = IP(src=attacker, dst=target) / TCP(sport=random.randint(1024, 65535), 
                                                   dport=80, flags="S", seq=random.randint(1000, 999999))
        packets.append(pkt)
    
    wrpcap('../pcaps/demo_syn_flood.pcap', packets)
    print(f"✓ Generated {len(packets)} packets")
    
    print("\n🔍 Analyzing with IDS...")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False
    for pkt in packets:
        ids.packet_handler(pkt)
    
    print(f"\n🚨 DETECTED: {len(ids.alerts)} alerts")
    if ids.alerts:
        print(f"   • {ids.alerts[0]}")


def demo_icmp_flood():
    """Demo 3: ICMP Flood"""
    print("\n" + "="*70)
    print("  💥 DEMO 3: ICMP PING FLOOD")
    print("="*70)
    
    print("\n📡 Generating ICMP flood (120 ping packets)...")
    packets = []
    attacker = "192.168.1.50"
    target = "192.168.1.100"
    
    for i in range(120):
        pkt = IP(src=attacker, dst=target) / ICMP(type=8, seq=i)
        packets.append(pkt)
    
    wrpcap('../pcaps/demo_icmp_flood.pcap', packets)
    print(f"✓ Generated {len(packets)} packets")
    
    print("\n🔍 Analyzing with IDS...")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False
    for pkt in packets:
        ids.packet_handler(pkt)
    
    print(f"\n🚨 DETECTED: {len(ids.alerts)} alerts")
    if ids.alerts:
        print(f"   • {ids.alerts[0]}")


def demo_dns_tunnel():
    """Demo 4: DNS Tunneling"""
    print("\n" + "="*70)
    print("  🕳️  DEMO 4: DNS TUNNELING")
    print("="*70)
    
    print("\n📡 Generating suspicious DNS queries (hex-encoded data)...")
    packets = []
    attacker = "192.168.1.50"
    dns_server = "8.8.8.8"
    
    # Generate 15 suspicious queries
    for i in range(15):
        hex_data = ''.join(random.choice('0123456789abcdef') for _ in range(45))
        suspicious_domain = f"{hex_data}.evil-tunnel.com"
        pkt = IP(src=attacker, dst=dns_server) / DNS(qd=DNSQR(qname=suspicious_domain))
        packets.append(pkt)
    
    wrpcap('../pcaps/demo_dns_tunnel.pcap', packets)
    print(f"✓ Generated {len(packets)} queries")
    
    print("\n🔍 Analyzing with IDS...")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False
    for pkt in packets:
        ids.packet_handler(pkt)
    
    print(f"\n🚨 DETECTED: {len(ids.alerts)} alerts")
    if ids.alerts:
        print(f"   • {ids.alerts[0]}")
        if len(ids.alerts) > 1:
            print(f"   ... and {len(ids.alerts)-1} more")


if __name__ == "__main__":
    print("\n" + "🛡️"*35)
    print("         NETWORK IDS - ATTACK DEMONSTRATION SUITE")
    print("🛡️"*35)
    
    demo_port_scan()
    demo_syn_flood()
    demo_icmp_flood()
    demo_dns_tunnel()
    
    print("\n" + "="*70)
    print("  ✅ ALL DEMOS COMPLETE!")
    print("="*70)
    
    print("\n📊 Summary:")
    print("   ✓ Port Scan Detection")
    print("   ✓ SYN Flood Detection")
    print("   ✓ ICMP Flood Detection")
    print("   ✓ DNS Tunneling Detection")
    
    print("\n💾 Generated PCAPs saved to: pcaps/")
    print("   • demo_port_scan.pcap")
    print("   • demo_syn_flood.pcap")
    print("   • demo_icmp_flood.pcap")
    print("   • demo_dns_tunnel.pcap")
    
    print("\n🎯 Try running: python3 demo_terminal_attacks.py")
    print("   for interactive menu-driven demos!\n")
