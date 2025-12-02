#!/usr/bin/env python3
"""
Basic packet sniffer for IDS
Captures and displays network traffic on the Docker virtual network
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP

def packet_handler(pkt):
    """
    Handler function called for each packet captured
    Prints a summary of packet details
    """
    if IP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        protocol = pkt[IP].proto
        
        if TCP in pkt:
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
            flags = pkt[TCP].flags
            print(f"[TCP] {src_ip}:{src_port} → {dst_ip}:{dst_port} | Flags: {flags}")
        
        elif UDP in pkt:
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport
            print(f"[UDP] {src_ip}:{src_port} → {dst_ip}:{dst_port}")
        
        elif ICMP in pkt:
            print(f"[ICMP] {src_ip} → {dst_ip}")
    
    elif ARP in pkt:
        if pkt[ARP].op == 1:  # ARP request
            print(f"[ARP Request] Who has {pkt[ARP].pdst}? Tell {pkt[ARP].psrc}")
        elif pkt[ARP].op == 2:  # ARP reply
            print(f"[ARP Reply] {pkt[ARP].psrc} is at {pkt[ARP].hwsrc}")

def main():
    """
    Main sniffer function
    Starts capturing packets on eth0 interface
    """
    print("=" * 60)
    print("IDS Packet Sniffer Started")
    print("Listening on interface: eth0")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Start sniffing on eth0 (Docker network interface)
        sniff(iface="eth0", prn=packet_handler, store=False)
    except KeyboardInterrupt:
        print("\n\nSniffer stopped by user")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
