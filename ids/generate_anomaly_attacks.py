#!/usr/bin/env python3
"""
Generate advanced attack traffic that triggers anomaly detection
Creates attacks with statistical anomalies in volume, entropy, and timing
"""

from scapy.all import IP, TCP, UDP, ICMP, Raw, wrpcap
import random

def generate_volume_spike_attack():
    """Generate traffic volume spike (10x normal rate)"""
    packets = []
    clients = [f"192.168.1.{i}" for i in range(10, 15)]
    server = "93.184.216.34"
    
    # Burst of 500 packets in short time (triggers volume anomaly)
    for _ in range(500):
        client = random.choice(clients)
        src_port = random.randint(49152, 65535)
        dst_port = random.choice([80, 443, 8080])
        
        # HTTP GET packets
        pkt = IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='PA')/Raw(load="GET / HTTP/1.1\r\n\r\n")
        packets.append(pkt)
    
    return packets

def generate_entropy_scan():
    """Generate high-entropy port scan (triggers entropy anomaly)"""
    packets = []
    attacker = "192.168.1.100"
    target = "192.168.1.50"
    
    # Scan many random ports (high entropy)
    ports = list(range(1, 500))  # 500 different ports
    random.shuffle(ports)
    
    for port in ports:
        pkt = IP(src=attacker, dst=target)/TCP(sport=random.randint(40000, 50000), dport=port, flags='S')
        packets.append(pkt)
    
    return packets

def generate_burst_attack():
    """Generate rapid burst with identical packet structure (triggers timing anomaly)"""
    packets = []
    attacker = "192.168.1.99"
    target = "10.0.0.1"
    
    # 300 identical packets with very low inter-arrival time
    for i in range(300):
        pkt = IP(src=attacker, dst=target)/TCP(sport=12345, dport=80, flags='S', seq=1000+i)
        # Set timestamps very close together (0.0001s apart = 10,000 pkt/s)
        pkt.time = 1000.0 + (i * 0.0001)
        packets.append(pkt)
    
    return packets

def generate_bandwidth_hog():
    """Generate large packet sizes (triggers bandwidth anomaly)"""
    packets = []
    attacker = "192.168.1.98"
    target = "10.0.0.2"
    
    # 100 packets with 1400 byte payload (MTU-size)
    for i in range(100):
        payload = "X" * 1400  # Large payload
        pkt = IP(src=attacker, dst=target)/TCP(sport=40000+i, dport=80, flags='PA')/Raw(load=payload)
        packets.append(pkt)
    
    return packets

def generate_asymmetric_flow():
    """Generate one-way communication (triggers flow asymmetry)"""
    packets = []
    attacker = "192.168.1.97"
    target = "10.0.0.3"
    
    # 200 packets in one direction only (no responses)
    for i in range(200):
        pkt = IP(src=attacker, dst=target)/TCP(sport=50000, dport=443, flags='PA')/Raw(load="data")
        packets.append(pkt)
    
    return packets

def main():
    print("Generating advanced anomaly-triggering attacks...\n")
    
    # Generate different attack types
    volume_packets = generate_volume_spike_attack()
    print(f"✓ Volume spike attack: {len(volume_packets)} packets (10x normal rate)")
    
    entropy_packets = generate_entropy_scan()
    print(f"✓ High-entropy scan: {len(entropy_packets)} packets (500 different ports)")
    
    burst_packets = generate_burst_attack()
    print(f"✓ Burst attack: {len(burst_packets)} packets (microsecond timing)")
    
    bandwidth_packets = generate_bandwidth_hog()
    print(f"✓ Bandwidth attack: {len(bandwidth_packets)} packets (MTU-size payloads)")
    
    asymmetric_packets = generate_asymmetric_flow()
    print(f"✓ Asymmetric flow: {len(asymmetric_packets)} packets (one-way only)")
    
    # Save individual attacks
    wrpcap('../pcaps/volume_spike.pcap', volume_packets)
    wrpcap('../pcaps/entropy_scan.pcap', entropy_packets)
    wrpcap('../pcaps/burst_attack.pcap', burst_packets)
    wrpcap('../pcaps/bandwidth_attack.pcap', bandwidth_packets)
    wrpcap('../pcaps/asymmetric_flow.pcap', asymmetric_packets)
    
    print("\n✅ Advanced attack PCAPs generated:")
    print("   - volume_spike.pcap (traffic volume anomaly)")
    print("   - entropy_scan.pcap (port entropy anomaly)")
    print("   - burst_attack.pcap (timing anomaly)")
    print("   - bandwidth_attack.pcap (bandwidth anomaly)")
    print("   - asymmetric_flow.pcap (flow asymmetry anomaly)")
    
    print("\nThese attacks are designed to trigger anomaly detection specifically!")

if __name__ == "__main__":
    main()
