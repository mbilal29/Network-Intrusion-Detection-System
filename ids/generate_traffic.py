#!/usr/bin/env python3
"""
Generate synthetic attack traffic for testing IDS
Creates PCAP files that simulate various attacks
"""

from scapy.all import IP, TCP, ARP, Ether, wrpcap, ICMP
import random

def generate_port_scan(target_ip="10.0.0.30", scanner_ip="10.0.0.20", num_ports=50):
    """Generate port scan traffic"""
    print(f"Generating port scan: {scanner_ip} → {target_ip} ({num_ports} ports)")
    packets = []
    
    for port in range(1, num_ports + 1):
        # SYN packet to different ports
        pkt = IP(src=scanner_ip, dst=target_ip) / TCP(dport=port, flags='S')
        packets.append(pkt)
    
    return packets

def generate_syn_flood(target_ip="10.0.0.30", attacker_ip="10.0.0.20", num_syns=200):
    """Generate SYN flood attack"""
    print(f"Generating SYN flood: {attacker_ip} → {target_ip} ({num_syns} SYNs)")
    packets = []
    
    for _ in range(num_syns):
        src_port = random.randint(10000, 65000)
        pkt = IP(src=attacker_ip, dst=target_ip) / TCP(sport=src_port, dport=80, flags='S')
        packets.append(pkt)
    
    return packets

def generate_arp_spoof():
    """Generate ARP spoofing attempt"""
    print("Generating ARP spoof attack")
    packets = []
    
    victim_ip = "10.0.0.30"
    victim_mac = "aa:bb:cc:dd:ee:ff"
    
    # Legitimate ARP reply
    pkt1 = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, psrc=victim_ip, hwsrc=victim_mac)
    packets.append(pkt1)
    
    # Spoofed ARP reply (different MAC for same IP)
    fake_mac = "11:22:33:44:55:66"
    pkt2 = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, psrc=victim_ip, hwsrc=fake_mac)
    packets.append(pkt2)
    
    return packets

def generate_normal_traffic(num_packets=50):
    """Generate normal traffic baseline"""
    print(f"Generating normal traffic ({num_packets} packets)")
    packets = []
    
    hosts = ["10.0.0.10", "10.0.0.20", "10.0.0.30"]
    
    for _ in range(num_packets):
        src = random.choice(hosts)
        dst = random.choice([h for h in hosts if h != src])
        
        # Mix of TCP, UDP, ICMP
        traffic_type = random.choice(['tcp', 'icmp'])
        
        if traffic_type == 'tcp':
            pkt = IP(src=src, dst=dst) / TCP(sport=random.randint(1024, 65535), 
                                             dport=random.choice([80, 443, 22, 8080]),
                                             flags='A')
        else:
            pkt = IP(src=src, dst=dst) / ICMP()
        
        packets.append(pkt)
    
    return packets

def main():
    import os
    
    # Create pcaps directory
    pcap_dir = "../pcaps"
    if not os.path.exists(pcap_dir):
        os.makedirs(pcap_dir)
        print(f"Created directory: {pcap_dir}")
    
    print("\n" + "="*70)
    print("🔬 GENERATING SYNTHETIC ATTACK TRAFFIC")
    print("="*70 + "\n")
    
    # Generate different attack scenarios
    scenarios = [
        ("portscan.pcap", generate_port_scan()),
        ("synflood.pcap", generate_syn_flood()),
        ("arpspoof.pcap", generate_arp_spoof()),
        ("normal.pcap", generate_normal_traffic()),
    ]
    
    # Mixed attack scenario
    print("\nGenerating mixed attack scenario...")
    mixed = []
    mixed.extend(generate_normal_traffic(30))
    mixed.extend(generate_port_scan(num_ports=25))
    mixed.extend(generate_normal_traffic(20))
    mixed.extend(generate_syn_flood(num_syns=100))
    mixed.extend(generate_normal_traffic(20))
    mixed.extend(generate_arp_spoof())
    scenarios.append(("mixed_attack.pcap", mixed))
    
    # Write PCAP files
    print("\n" + "-"*70)
    print("Writing PCAP files...")
    print("-"*70 + "\n")
    
    for filename, packets in scenarios:
        filepath = os.path.join(pcap_dir, filename)
        wrpcap(filepath, packets)
        print(f"✅ {filepath:<30} ({len(packets):>3} packets)")
    
    print("\n" + "="*70)
    print("✅ GENERATION COMPLETE")
    print("="*70)
    print(f"\nGenerated {len(scenarios)} PCAP files in: {pcap_dir}/")
    print("\nTest them with:")
    print("  python3 test_pcap.py ../pcaps/portscan.pcap")
    print("  python3 test_pcap.py ../pcaps/synflood.pcap")
    print("  python3 test_pcap.py ../pcaps/mixed_attack.pcap")
    print()

if __name__ == "__main__":
    main()
