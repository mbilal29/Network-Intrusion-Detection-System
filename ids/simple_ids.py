#!/usr/bin/env python3
"""
SIMPLIFIED IDS FOR LOCAL TESTING
Since Docker repos are down, this runs locally on your Mac
Captures real network traffic and implements detection logic
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, wrpcap, rdpcap
import time
from collections import defaultdict
from datetime import datetime

class SimpleIDS:
    def __init__(self):
        # Detection state
        self.port_scan_tracker = defaultdict(set)  # src_ip -> set of dst_ports
        self.syn_tracker = defaultdict(int)  # src_ip -> SYN count
        self.syn_ack_tracker = defaultdict(int)  # src_ip -> SYN-ACK count
        self.arp_table = {}  # ip -> mac mapping
        self.flow_stats = defaultdict(lambda: {'packets': 0, 'bytes': 0, 'start': time.time()})
        
        # Thresholds
        self.PORT_SCAN_THRESHOLD = 10  # ports
        self.PORT_SCAN_WINDOW = 5  # seconds
        self.SYN_FLOOD_THRESHOLD = 50  # SYNs per second
        self.syn_window_start = time.time()
        
        # Alerts
        self.alerts = []
        
    def alert(self, alert_type, details):
        """Generate and store an alert"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] ALERT: {alert_type} - {details}"
        print(f"\n🚨 {alert_msg}")
        self.alerts.append(alert_msg)
        
        # Write to file
        with open('alerts.log', 'a') as f:
            f.write(alert_msg + '\n')
    
    def detect_port_scan(self, src_ip):
        """Detect port scanning behavior"""
        unique_ports = len(self.port_scan_tracker[src_ip])
        if unique_ports > self.PORT_SCAN_THRESHOLD:
            self.alert("PORT SCAN", f"{src_ip} probed {unique_ports} different ports")
            self.port_scan_tracker[src_ip].clear()  # Reset after alert
    
    def detect_syn_flood(self, src_ip):
        """Detect SYN flood attacks"""
        current_time = time.time()
        
        # Reset counters every second
        if current_time - self.syn_window_start > 1:
            if self.syn_tracker[src_ip] > self.SYN_FLOOD_THRESHOLD:
                syn_ack_ratio = self.syn_ack_tracker[src_ip] / max(self.syn_tracker[src_ip], 1)
                if syn_ack_ratio < 0.1:
                    self.alert("SYN FLOOD", 
                             f"{src_ip} sent {self.syn_tracker[src_ip]} SYNs with ratio {syn_ack_ratio:.2f}")
            
            # Reset
            self.syn_tracker.clear()
            self.syn_ack_tracker.clear()
            self.syn_window_start = current_time
    
    def detect_arp_spoof(self, ip, mac):
        """Detect ARP spoofing"""
        if ip in self.arp_table:
            if self.arp_table[ip] != mac:
                self.alert("ARP SPOOF", 
                         f"IP {ip} changed from MAC {self.arp_table[ip]} to {mac}")
        self.arp_table[ip] = mac
    
    def packet_handler(self, pkt):
        """Main packet processing function"""
        
        # TCP packet analysis
        if TCP in pkt and IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            dst_port = pkt[TCP].dport
            flags = pkt[TCP].flags
            
            # Track flows
            flow_key = f"{src_ip}→{dst_ip}:{dst_port}"
            self.flow_stats[flow_key]['packets'] += 1
            self.flow_stats[flow_key]['bytes'] += len(pkt)
            
            # Port scan detection
            self.port_scan_tracker[src_ip].add(dst_port)
            self.detect_port_scan(src_ip)
            
            # SYN flood detection
            if flags & 0x02:  # SYN flag
                self.syn_tracker[src_ip] += 1
                self.detect_syn_flood(src_ip)
            
            if flags & 0x12:  # SYN-ACK
                self.syn_ack_tracker[dst_ip] += 1
            
            # Display packet
            flag_str = self._get_flag_string(flags)
            print(f"[TCP] {src_ip}:{pkt[TCP].sport} → {dst_ip}:{dst_port} [{flag_str}]")
        
        # ARP packet analysis
        elif ARP in pkt:
            if pkt[ARP].op == 2:  # ARP reply
                ip = pkt[ARP].psrc
                mac = pkt[ARP].hwsrc
                self.detect_arp_spoof(ip, mac)
                print(f"[ARP Reply] {ip} is at {mac}")
        
        # ICMP packets
        elif ICMP in pkt and IP in pkt:
            print(f"[ICMP] {pkt[IP].src} → {pkt[IP].dst}")
    
    def _get_flag_string(self, flags):
        """Convert TCP flags to readable string"""
        flag_map = {
            0x02: 'SYN',
            0x10: 'ACK',
            0x12: 'SYN-ACK',
            0x01: 'FIN',
            0x04: 'RST',
            0x08: 'PSH'
        }
        return flag_map.get(flags, str(flags))
    
    def start(self, interface=None, count=0):
        """Start the IDS"""
        print("=" * 70)
        print("🛡️  SIMPLE IDS STARTED")
        print("=" * 70)
        print(f"Monitoring: {interface if interface else 'all interfaces'}")
        print("Press Ctrl+C to stop\n")
        
        try:
            if interface:
                sniff(iface=interface, prn=self.packet_handler, store=False, count=count)
            else:
                sniff(prn=self.packet_handler, store=False, count=count)
        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print(f"IDS STOPPED - {len(self.alerts)} alerts generated")
            print("=" * 70)
            self.print_summary()
    
    def print_summary(self):
        """Print detection summary"""
        print("\n📊 DETECTION SUMMARY:")
        print(f"  Total Alerts: {len(self.alerts)}")
        print(f"  Unique IPs Scanned: {len(self.port_scan_tracker)}")
        print(f"  ARP Table Entries: {len(self.arp_table)}")
        print(f"  Active Flows: {len(self.flow_stats)}")
        
        if self.alerts:
            print("\n🚨 Recent Alerts:")
            for alert in self.alerts[-10:]:  # Last 10 alerts
                print(f"  {alert}")

if __name__ == "__main__":
    import sys
    
    print("\n🚀 Starting IDS in LOCAL MODE (Docker is down)")
    print("This will capture real traffic on your Mac\n")
    
    # Run with limited packet capture for testing
    ids = SimpleIDS()
    
    # You need sudo to capture packets
    import os
    if os.geteuid() != 0:
        print("⚠️  WARNING: You need to run with sudo to capture packets:")
        print(f"   sudo python3 {sys.argv[0]}\n")
    
    # Start capturing (will run until Ctrl+C)
    ids.start()
