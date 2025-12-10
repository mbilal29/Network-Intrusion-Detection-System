#!/usr/bin/env python3
"""
Terminal-based Attack Demo
Run individual attacks from terminal and analyze with IDS in real-time
Perfect for live demonstrations!
"""

import os
import sys
import time
import subprocess
from enhanced_ids import EnhancedIDS
from scapy.all import *

def print_banner(text):
    """Print styled banner"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def demo_port_scan():
    """Demo 1: Port Scan Attack"""
    print_banner("DEMO 1: PORT SCAN ATTACK")
    
    print("🎯 Simulating nmap-style port scan...")
    print("   Target: 192.168.1.100")
    print("   Ports: 1-100")
    print()
    
    # Generate port scan packets
    packets = []
    attacker = "192.168.1.50"
    target = "192.168.1.100"
    
    print("📡 Scanning ports:", end=" ", flush=True)
    for port in range(1, 101):
        pkt = IP(src=attacker, dst=target) / TCP(dport=port, flags="S")
        packets.append(pkt)
        if port % 10 == 0:
            print(f"{port}", end="...", flush=True)
    
    print("\n\n💾 Saving capture: demo_port_scan.pcap")
    wrpcap('../pcaps/demo_port_scan.pcap', packets)
    
    # Analyze with IDS (suppress verbose packet output)
    print("🔍 Analyzing with IDS...\n")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False  # Disable verbose packet printing
    packets = rdpcap('../pcaps/demo_port_scan.pcap')
    for pkt in packets:
        ids.packet_handler(pkt)
    
    # Show results
    print(f"\n🚨 DETECTION RESULTS:")
    print(f"   Total Alerts: {len(ids.alerts)}")
    for alert in ids.alerts[:3]:  # Show first 3
        print(f"   • {alert}")
    
    return len(ids.alerts)


def demo_syn_flood():
    """Demo 2: SYN Flood Attack"""
    print_banner("DEMO 2: SYN FLOOD ATTACK")
    
    print("🎯 Simulating SYN flood attack...")
    print("   Target: 192.168.1.100:80")
    print("   Rate: 100 packets")
    print()
    
    packets = []
    attacker = "192.168.1.50"
    target = "192.168.1.100"
    
    print("💥 Flooding:", end=" ", flush=True)
    for i in range(100):
        pkt = IP(src=attacker, dst=target) / TCP(dport=80, flags="S")
        packets.append(pkt)
        if i % 20 == 0:
            print("█", end="", flush=True)
    
    print("\n\n💾 Saving capture: demo_syn_flood.pcap")
    wrpcap('../pcaps/demo_syn_flood.pcap', packets)
    
    # Analyze with IDS (suppress verbose packet output)
    print("🔍 Analyzing with IDS...\n")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False  # Disable verbose packet printing
    packets = rdpcap('../pcaps/demo_syn_flood.pcap')
    for pkt in packets:
        ids.packet_handler(pkt)
    
    # Show results
    print(f"\n🚨 DETECTION RESULTS:")
    print(f"   Total Alerts: {len(ids.alerts)}")
    for alert in ids.alerts:
        print(f"   • {alert}")
    
    return len(ids.alerts)


def demo_icmp_flood():
    """Demo 3: ICMP Ping Flood"""
    print_banner("DEMO 3: ICMP PING FLOOD")
    
    print("🎯 Simulating ping flood attack...")
    print("   Target: 192.168.1.100")
    print("   Type: ICMP Echo Request")
    print()
    
    packets = []
    attacker = "192.168.1.50"
    target = "192.168.1.100"
    
    print("🏓 Flooding:", end=" ", flush=True)
    for i in range(120):
        pkt = IP(src=attacker, dst=target) / ICMP(type=8)
        packets.append(pkt)
        if i % 20 == 0:
            print("█", end="", flush=True)
    
    print("\n\n💾 Saving capture: demo_icmp_flood.pcap")
    wrpcap('../pcaps/demo_icmp_flood.pcap', packets)
    
    # Analyze with IDS (suppress verbose packet output)
    print("🔍 Analyzing with IDS...\n")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False  # Disable verbose packet printing
    packets = rdpcap('../pcaps/demo_icmp_flood.pcap')
    for pkt in packets:
        ids.packet_handler(pkt)
    
    # Show results
    print(f"\n🚨 DETECTION RESULTS:")
    print(f"   Total Alerts: {len(ids.alerts)}")
    for alert in ids.alerts:
        print(f"   • {alert}")
    
    return len(ids.alerts)


def demo_dns_tunnel():
    """Demo 4: DNS Tunneling"""
    print_banner("DEMO 4: DNS TUNNELING ATTACK")
    
    print("🎯 Simulating DNS tunneling exfiltration...")
    print("   Method: Hex-encoded subdomains")
    print("   Domain: evil-c2.com")
    print()
    
    packets = []
    attacker = "192.168.1.50"
    dns_server = "8.8.8.8"
    
    # Generate suspicious DNS queries with long hex subdomains
    print("📡 Generating tunneling queries:", end=" ", flush=True)
    for i in range(15):
        # Generate random hex string (simulating data exfiltration)
        hex_data = ''.join(random.choice('0123456789abcdef') for _ in range(32))
        query = f"{hex_data}.evil-c2.com."
        
        pkt = IP(src=attacker, dst=dns_server) / UDP(dport=53) / DNS(
            rd=1, qd=DNSQR(qname=query)
        )
        packets.append(pkt)
        if i % 3 == 0:
            print("█", end="", flush=True)
    
    print("\n\n💾 Saving capture: demo_dns_tunnel.pcap")
    wrpcap('../pcaps/demo_dns_tunnel.pcap', packets)
    
    # Analyze with IDS (suppress verbose packet output)
    print("🔍 Analyzing with IDS...\n")
    ids = EnhancedIDS(use_anomaly_detection=False)
    ids.verbose = False  # Disable verbose packet printing
    packets = rdpcap('../pcaps/demo_dns_tunnel.pcap')
    for pkt in packets:
        ids.packet_handler(pkt)
    
    # Show results
    print(f"\n🚨 DETECTION RESULTS:")
    print(f"   Total Alerts: {len(ids.alerts)}")
    for alert in ids.alerts[:5]:  # Show first 5
        print(f"   • {alert}")
    
    return len(ids.alerts)


def interactive_menu():
    """Interactive demo menu"""
    while True:
        print("\n" + "=" * 70)
        print("  🛡️  NETWORK IDS - LIVE ATTACK DEMONSTRATION")
        print("=" * 70)
        print("\nSelect an attack to demonstrate:\n")
        print("  1) Port Scan (nmap-style)")
        print("  2) SYN Flood Attack")
        print("  3) ICMP Ping Flood")
        print("  4) DNS Tunneling")
        print("  5) Run All Demos")
        print("  6) Exit")
        print()
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == '1':
            demo_port_scan()
            input("\nPress Enter to continue...")
        elif choice == '2':
            demo_syn_flood()
            input("\nPress Enter to continue...")
        elif choice == '3':
            demo_icmp_flood()
            input("\nPress Enter to continue...")
        elif choice == '4':
            demo_dns_tunnel()
            input("\nPress Enter to continue...")
        elif choice == '5':
            total_alerts = 0
            total_alerts += demo_port_scan()
            input("\nPress Enter for next demo...")
            total_alerts += demo_syn_flood()
            input("\nPress Enter for next demo...")
            total_alerts += demo_icmp_flood()
            input("\nPress Enter for next demo...")
            total_alerts += demo_dns_tunnel()
            
            print("\n" + "=" * 70)
            print(f"  ✅ ALL DEMOS COMPLETE - Total Alerts: {total_alerts}")
            print("=" * 70)
            input("\nPress Enter to continue...")
        elif choice == '6':
            print("\n👋 Exiting demo. Stay secure!\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    print("\n🚀 Starting IDS Attack Demonstration System...")
    time.sleep(1)
    
    # Check if baseline exists
    if not os.path.exists('baseline_model.pkl'):
        print("\n⚠️  Warning: baseline_model.pkl not found")
        print("   Anomaly detection will not be available")
    
    interactive_menu()
