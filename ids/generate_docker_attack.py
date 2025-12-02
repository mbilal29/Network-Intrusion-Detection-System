#!/usr/bin/env python3
"""Generate a realistic attack PCAP simulating Docker container traffic."""

from scapy.all import *
import random

packets = []

# Simulated IPs (Docker network 10.0.0.0/24)
attacker_ip = "10.0.0.20"
victim_ip = "10.0.0.30"
ids_ip = "10.0.0.10"

# Simulated MACs
attacker_mac = "02:42:0a:00:00:14"
victim_mac = "02:42:0a:00:00:1e"

print("Generating Docker attack simulation PCAP...")

# 1. Port scan (TCP SYN to ports 1-100)
print(f"Simulating port scan: {attacker_ip} -> {victim_ip}")
for port in range(1, 101):
    pkt = Ether(src=attacker_mac, dst=victim_mac) / \
          IP(src=attacker_ip, dst=victim_ip) / \
          TCP(sport=random.randint(40000, 60000), dport=port, flags="S", seq=random.randint(1, 100000))
    packets.append(pkt)
    
    # Simulate RST responses for closed ports
    if port not in [80, 443, 22]:  # Most ports closed
        response = Ether(src=victim_mac, dst=attacker_mac) / \
                   IP(src=victim_ip, dst=attacker_ip) / \
                   TCP(sport=port, dport=pkt[TCP].sport, flags="RA", seq=0, ack=pkt[TCP].seq+1)
        packets.append(response)

# 2. SYN flood on port 80
print(f"Simulating SYN flood: {attacker_ip} -> {victim_ip}:80")
for i in range(200):
    src_port = random.randint(40000, 60000)
    pkt = Ether(src=attacker_mac, dst=victim_mac) / \
          IP(src=attacker_ip, dst=victim_ip) / \
          TCP(sport=src_port, dport=80, flags="S", seq=random.randint(1, 100000))
    packets.append(pkt)

# 3. UDP scan on common ports
print(f"Simulating UDP scan: {attacker_ip} -> {victim_ip}")
for port in [53, 123, 161, 69, 514]:
    pkt = Ether(src=attacker_mac, dst=victim_mac) / \
          IP(src=attacker_ip, dst=victim_ip) / \
          UDP(sport=random.randint(40000, 60000), dport=port)
    packets.append(pkt)
    
    # ICMP port unreachable response
    response = Ether(src=victim_mac, dst=attacker_mac) / \
               IP(src=victim_ip, dst=attacker_ip) / \
               ICMP(type=3, code=3) / \
               IP(src=attacker_ip, dst=victim_ip) / \
               UDP(sport=pkt[UDP].sport, dport=port)
    packets.append(response)

# 4. Add some normal traffic between IDS and victim (monitoring)
print(f"Adding normal monitoring traffic: {ids_ip} <-> {victim_ip}")
for i in range(10):
    # ICMP ping from IDS to victim
    ping = Ether(src="02:42:0a:00:00:0a", dst=victim_mac) / \
           IP(src=ids_ip, dst=victim_ip) / \
           ICMP(type=8, id=random.randint(1, 1000), seq=i)
    packets.append(ping)
    
    # ICMP reply
    reply = Ether(src=victim_mac, dst="02:42:0a:00:00:0a") / \
            IP(src=victim_ip, dst=ids_ip) / \
            ICMP(type=0, id=ping[ICMP].id, seq=i)
    packets.append(reply)

# Write PCAP
output_file = "../pcaps/docker_real_attack.pcap"
wrpcap(output_file, packets)

print(f"\n✓ Generated {len(packets)} packets")
print(f"✓ Saved to: {output_file}")
print(f"\nAttack breakdown:")
print(f"  - Port scan: 100 ports (TCP SYN)")
print(f"  - SYN flood: 200 packets to port 80")
print(f"  - UDP scan: 5 ports")
print(f"  - Normal traffic: 20 ICMP packets")
print(f"\nThis simulates real Docker container attack traffic on the 10.0.0.0/24 network.")
