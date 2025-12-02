#!/usr/bin/env python3
"""
Generate realistic baseline network traffic for anomaly detection training.
Creates normal traffic patterns: HTTP, DNS, SSH, ICMP with realistic timing.
"""

from scapy.all import IP, TCP, UDP, ICMP, DNS, DNSQR, Raw, wrpcap
import random
import time

def generate_http_traffic(num_flows=50):
    """Generate realistic HTTP request/response patterns"""
    packets = []
    
    # Simulate multiple client-server pairs
    clients = [f"192.168.1.{i}" for i in range(10, 20)]
    servers = ["93.184.216.34", "142.250.185.46", "104.16.132.229"]  # example.com, google, cloudflare
    
    for _ in range(num_flows):
        client = random.choice(clients)
        server = random.choice(servers)
        src_port = random.randint(49152, 65535)
        dst_port = 80
        
        # Three-way handshake
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='S', seq=1000))
        packets.append(IP(src=server, dst=client)/TCP(sport=dst_port, dport=src_port, flags='SA', seq=2000, ack=1001))
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='A', seq=1001, ack=2001))
        
        # HTTP GET request
        http_request = "GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n"
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='PA', seq=1001, ack=2001)/Raw(load=http_request))
        packets.append(IP(src=server, dst=client)/TCP(sport=dst_port, dport=src_port, flags='A', seq=2001, ack=1001+len(http_request)))
        
        # HTTP response
        http_response = "HTTP/1.1 200 OK\r\nContent-Length: 500\r\n\r\n" + ("x" * 500)
        packets.append(IP(src=server, dst=client)/TCP(sport=dst_port, dport=src_port, flags='PA', seq=2001, ack=1001+len(http_request))/Raw(load=http_response))
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='A', seq=1001+len(http_request), ack=2001+len(http_response)))
        
        # Connection termination
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='FA', seq=1001+len(http_request), ack=2001+len(http_response)))
        packets.append(IP(src=server, dst=client)/TCP(sport=dst_port, dport=src_port, flags='FA', seq=2001+len(http_response), ack=1002+len(http_request)))
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='A', seq=1002+len(http_request), ack=2002+len(http_response)))
    
    return packets

def generate_dns_traffic(num_queries=30):
    """Generate realistic DNS queries and responses"""
    packets = []
    
    clients = [f"192.168.1.{i}" for i in range(10, 20)]
    dns_server = "8.8.8.8"
    domains = ["google.com", "github.com", "stackoverflow.com", "example.com", "amazon.com"]
    
    for _ in range(num_queries):
        client = random.choice(clients)
        domain = random.choice(domains)
        src_port = random.randint(49152, 65535)
        txid = random.randint(1, 65535)
        
        # DNS query
        query = IP(src=client, dst=dns_server)/UDP(sport=src_port, dport=53)/DNS(id=txid, qd=DNSQR(qname=domain))
        packets.append(query)
        
        # DNS response
        response = IP(src=dns_server, dst=client)/UDP(sport=53, dport=src_port)/DNS(id=txid, qr=1, an=DNSQR(qname=domain))
        packets.append(response)
    
    return packets

def generate_ssh_traffic(num_sessions=10):
    """Generate SSH connection patterns"""
    packets = []
    
    clients = [f"192.168.1.{i}" for i in range(10, 15)]
    servers = ["192.168.1.100", "10.0.0.50"]
    
    for _ in range(num_sessions):
        client = random.choice(clients)
        server = random.choice(servers)
        src_port = random.randint(49152, 65535)
        dst_port = 22
        
        # Three-way handshake
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='S', seq=1000))
        packets.append(IP(src=server, dst=client)/TCP(sport=dst_port, dport=src_port, flags='SA', seq=2000, ack=1001))
        packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='A', seq=1001, ack=2001))
        
        # SSH data exchange (encrypted, random size packets)
        for _ in range(random.randint(10, 30)):
            size = random.randint(50, 200)
            packets.append(IP(src=client, dst=server)/TCP(sport=src_port, dport=dst_port, flags='PA')/Raw(load='X' * size))
            packets.append(IP(src=server, dst=client)/TCP(sport=dst_port, dport=src_port, flags='PA')/Raw(load='Y' * size))
    
    return packets

def generate_icmp_traffic(num_pings=20):
    """Generate ICMP ping traffic"""
    packets = []
    
    clients = [f"192.168.1.{i}" for i in range(10, 20)]
    targets = ["8.8.8.8", "1.1.1.1", "192.168.1.1"]
    
    for _ in range(num_pings):
        client = random.choice(clients)
        target = random.choice(targets)
        seq = random.randint(1, 100)
        
        # ICMP Echo Request
        packets.append(IP(src=client, dst=target)/ICMP(type=8, code=0, id=1234, seq=seq))
        
        # ICMP Echo Reply
        packets.append(IP(src=target, dst=client)/ICMP(type=0, code=0, id=1234, seq=seq))
    
    return packets

def add_realistic_timing(packets):
    """Add realistic inter-arrival times to packets"""
    # Most packets arrive with exponential distribution (mean ~0.01s)
    # This simulates bursty but normal network behavior
    timed_packets = []
    current_time = time.time()
    
    for pkt in packets:
        # Exponential inter-arrival with mean 0.01s (100 pkt/s average)
        delay = random.expovariate(100)
        current_time += delay
        pkt.time = current_time
        timed_packets.append(pkt)
    
    return timed_packets

def main():
    print("Generating realistic baseline network traffic...")
    
    # Generate different types of traffic
    http_packets = generate_http_traffic(num_flows=50)
    print(f"✓ Generated {len(http_packets)} HTTP packets")
    
    dns_packets = generate_dns_traffic(num_queries=30)
    print(f"✓ Generated {len(dns_packets)} DNS packets")
    
    ssh_packets = generate_ssh_traffic(num_sessions=10)
    print(f"✓ Generated {len(ssh_packets)} SSH packets")
    
    icmp_packets = generate_icmp_traffic(num_pings=20)
    print(f"✓ Generated {len(icmp_packets)} ICMP packets")
    
    # Combine all packets
    all_packets = http_packets + dns_packets + ssh_packets + icmp_packets
    
    # Shuffle to mix traffic types (realistic network)
    random.shuffle(all_packets)
    
    # Add realistic timing
    all_packets = add_realistic_timing(all_packets)
    
    # Write to PCAP
    output_file = '../pcaps/baseline_normal.pcap'
    wrpcap(output_file, all_packets)
    
    print(f"\n✅ Baseline traffic saved: {output_file}")
    print(f"   Total packets: {len(all_packets)}")
    print(f"   HTTP flows: 50 (with full handshakes)")
    print(f"   DNS queries: 30")
    print(f"   SSH sessions: 10")
    print(f"   ICMP pings: 20")
    print("\nThis PCAP will be used to train the anomaly detection baseline.")

if __name__ == "__main__":
    main()
