#!/usr/bin/env python3
"""
ENHANCED IDS WITH ANOMALY DETECTION
Implements both signature-based and anomaly-based detection
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, wrpcap, rdpcap, DNS, DNSQR
import time
import math
import json
import pickle
import os
from collections import defaultdict
from datetime import datetime

# ============================================================================
# DETECTION THRESHOLDS - EASY TO MODIFY FOR TESTING
# ============================================================================
# Signature-Based Detection Thresholds
PORT_SCAN_THRESHOLD = 5          # Alert after scanning X unique ports
SYN_FLOOD_THRESHOLD = 50          # Alert after X SYN packets without responses
SYN_FLOOD_RATIO = 0.1             # Alert if SYN/ACK ratio below X (10% responses)
ICMP_FLOOD_THRESHOLD = 50         # Alert after X ICMP packets in time window
ICMP_FLOOD_WINDOW = 5             # Time window in seconds for ICMP flood detection
DNS_TUNNEL_MIN_LENGTH = 30        # Alert if DNS subdomain longer than X characters
DNS_TUNNEL_HEX_THRESHOLD = 0.6    # Alert if subdomain has >X% hexadecimal characters

# Anomaly-Based Detection Thresholds
ANOMALY_Z_THRESHOLD = 3.0         # Alert if z-score exceeds X standard deviations
PORT_ENTROPY_MULTIPLIER = 1.3     # Alert if entropy > baseline * X
ANOMALY_WINDOW_DURATION = 10      # Time window in seconds for anomaly detection

# ============================================================================

class AnomalyDetector:
    """Statistical anomaly detection engine"""
    
    def __init__(self):
        self.baseline = {
            'packet_rate': {'mean': 0, 'std': 0},
            'byte_rate': {'mean': 0, 'std': 0},
            'packet_sizes': [],
            'port_entropy': 0,
            'inter_arrival_times': [],
            'syn_ack_ratio': {'mean': 0, 'std': 0},
            'flow_asymmetry': {'mean': 0, 'std': 0}
        }
        self.trained = False
        
        # Auto-load baseline model if it exists
        if os.path.exists('baseline_model.pkl'):
            try:
                self.load_model('baseline_model.pkl')
            except Exception as e:
                print(f"⚠️  Failed to load baseline model: {e}")
        
    def calculate_entropy(self, values):
        """Calculate Shannon entropy of a distribution"""
        if not values:
            return 0
        
        # Count frequencies
        freq = defaultdict(int)
        for v in values:
            freq[v] += 1
        
        # Calculate entropy
        total = len(values)
        entropy = 0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        return entropy
    
    def calculate_stats(self, values):
        """Calculate mean and standard deviation"""
        if not values:
            return {'mean': 0, 'std': 0}
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = math.sqrt(variance)
        
        return {'mean': mean, 'std': std}
    
    def z_score(self, value, mean, std):
        """Calculate z-score (number of standard deviations from mean)"""
        if std == 0:
            return 0
        # Convert to float to handle Decimal types from Scapy
        return abs(float(value) - float(mean)) / float(std)
    
    def train_from_pcap(self, pcap_file):
        """Train baseline model from normal traffic PCAP"""
        print(f"\n🎓 Training anomaly detector from {pcap_file}...")
        
        packets = rdpcap(pcap_file)
        
        # Extract features
        packet_times = []
        packet_sizes = []
        dst_ports = []
        syn_count = 0
        syn_ack_count = 0
        flow_packets = defaultdict(lambda: {'sent': 0, 'recv': 0})
        
        for i, pkt in enumerate(packets):
            # Convert to float immediately to avoid Decimal issues
            packet_times.append(float(pkt.time))
            packet_sizes.append(len(pkt))
            
            if TCP in pkt:
                dst_ports.append(pkt[TCP].dport)
                
                # Count SYN/SYN-ACK for baseline ratio
                flags = pkt[TCP].flags
                if flags & 0x02:  # SYN
                    syn_count += 1
                if flags & 0x12 == 0x12:  # SYN-ACK
                    syn_ack_count += 1
                
                # Track flow asymmetry
                if IP in pkt:
                    flow_key = f"{pkt[IP].src}-{pkt[IP].dst}"
                    flow_packets[flow_key]['sent'] += 1
        
        # Calculate inter-arrival times
        inter_arrival = []
        for i in range(1, len(packet_times)):
            # Convert to float to handle Decimal types
            inter_arrival.append(float(packet_times[i]) - float(packet_times[i-1]))
        
        # Calculate baseline statistics
        duration = float(packet_times[-1] - packet_times[0]) if len(packet_times) > 1 else 1.0
        
        packet_rate = len(packets) / duration
        self.baseline['packet_rate'] = {
            'mean': packet_rate,
            'std': packet_rate * 0.2  # 20% variation assumed normal
        }
        
        total_bytes = sum(packet_sizes)
        byte_rate = total_bytes / duration
        self.baseline['byte_rate'] = {
            'mean': byte_rate,
            'std': byte_rate * 0.3  # 30% variation assumed normal
        }
        
        self.baseline['packet_sizes'] = self.calculate_stats(packet_sizes)
        self.baseline['port_entropy'] = self.calculate_entropy(dst_ports)
        self.baseline['inter_arrival_times'] = self.calculate_stats(inter_arrival)
        
        # SYN/ACK ratio baseline
        syn_ack_ratio = syn_ack_count / max(syn_count, 1)
        self.baseline['syn_ack_ratio'] = {
            'mean': syn_ack_ratio,
            'std': 0.2  # Allow 20% deviation
        }
        
        # Flow asymmetry baseline
        asymmetries = []
        for flow_stats in flow_packets.values():
            total = flow_stats['sent'] + flow_stats['recv']
            if total > 0:
                asymmetry = abs(flow_stats['sent'] - flow_stats['recv']) / total
                asymmetries.append(asymmetry)
        self.baseline['flow_asymmetry'] = self.calculate_stats(asymmetries) if asymmetries else {'mean': 0, 'std': 0.3}
        
        self.trained = True
        
        print(f"✅ Training complete!")
        print(f"   Baseline packet rate: {self.baseline['packet_rate']['mean']:.1f} ± {self.baseline['packet_rate']['std']:.1f} pkt/s")
        print(f"   Baseline byte rate: {self.baseline['byte_rate']['mean']:.0f} ± {self.baseline['byte_rate']['std']:.0f} bytes/s")
        print(f"   Port entropy: {self.baseline['port_entropy']:.2f}")
        print(f"   Mean inter-arrival: {self.baseline['inter_arrival_times']['mean']:.4f}s")
        print(f"   SYN/ACK ratio: {self.baseline['syn_ack_ratio']['mean']:.2f}")
        
    def save_model(self, filename='baseline_model.pkl'):
        """Save trained baseline model"""
        with open(filename, 'wb') as f:
            pickle.dump(self.baseline, f)
        print(f"💾 Model saved to {filename}")
    
    def load_model(self, filename='baseline_model.pkl'):
        """Load trained baseline model"""
        with open(filename, 'rb') as f:
            self.baseline = pickle.load(f)
        self.trained = True
        print(f"📂 Model loaded from {filename}")


class EnhancedIDS:
    """IDS with both signature-based and anomaly-based detection"""
    
    def __init__(self, use_anomaly_detection=True):
        # Signature-based detection state
        self.port_scan_tracker = defaultdict(set)
        self.syn_tracker = defaultdict(int)
        self.syn_ack_tracker = defaultdict(int)
        self.arp_table = {}
        self.flow_stats = defaultdict(lambda: {'packets': 0, 'bytes': 0, 'start': time.time()})
        
        # Anomaly detection
        self.anomaly_detector = AnomalyDetector() if use_anomaly_detection else None
        self.use_anomaly_detection = use_anomaly_detection
        
        # Anomaly tracking
        self.window_packets = []
        self.window_start = time.time()
        self.window_duration = ANOMALY_WINDOW_DURATION
        self.dst_ports_window = []
        self.inter_arrival_window = []
        self.last_packet_time = None
        self.syn_window_start = time.time()
        self.syn_alerted = set()  # Track which IPs we've already alerted for SYN flood
        
        # ICMP flood tracking
        self.icmp_tracker = defaultdict(list)  # {src_ip: [timestamps]}
        self.icmp_window = ICMP_FLOOD_WINDOW
        self.icmp_alerted = set()  # Track which IPs we've already alerted for ICMP flood
        
        # DNS tunneling tracking
        self.dns_queries = []  # Track DNS queries for analysis
        
        # Thresholds (loaded from global constants at top of file)
        self.PORT_SCAN_THRESHOLD = PORT_SCAN_THRESHOLD
        self.SYN_FLOOD_THRESHOLD = SYN_FLOOD_THRESHOLD
        self.SYN_FLOOD_RATIO = SYN_FLOOD_RATIO
        self.ICMP_FLOOD_THRESHOLD = ICMP_FLOOD_THRESHOLD
        self.DNS_TUNNEL_MIN_LENGTH = DNS_TUNNEL_MIN_LENGTH
        self.DNS_TUNNEL_HEX_THRESHOLD = DNS_TUNNEL_HEX_THRESHOLD
        self.ANOMALY_Z_THRESHOLD = ANOMALY_Z_THRESHOLD
        self.PORT_ENTROPY_MULTIPLIER = PORT_ENTROPY_MULTIPLIER
        
        # Alerts
        self.alerts = []
        self.alert_counts = defaultdict(int)
        
        # Verbose output control
        self.verbose = True  # Can be set to False to suppress packet-level output
        
    def alert(self, alert_type, details, severity="MEDIUM"):
        """Generate and store an alert"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] [{severity}] {alert_type}: {details}"
        print(f"\n🚨 {alert_msg}")
        self.alerts.append(alert_msg)
        self.alert_counts[alert_type] += 1
        
        os.makedirs('outputs/logs', exist_ok=True)
        with open('outputs/logs/alerts.log', 'a') as f:
            f.write(alert_msg + '\n')
    
    # Signature-based detection methods
    def detect_port_scan(self, src_ip):
        """Signature-based: Detect port scanning"""
        unique_ports = len(self.port_scan_tracker[src_ip])
        if unique_ports > self.PORT_SCAN_THRESHOLD:
            self.alert("PORT_SCAN", f"{src_ip} scanned {unique_ports} ports", "HIGH")
            self.port_scan_tracker[src_ip].clear()
    
    def detect_syn_flood(self, src_ip):
        """Signature-based: Detect SYN flood attacks"""
        current_time = time.time()
        
        # Reset window every 5 seconds
        if current_time - self.syn_window_start > 5:
            self.syn_tracker.clear()
            self.syn_ack_tracker.clear()
            self.syn_window_start = current_time
            self.syn_alerted.clear()
        
        # Only alert once per IP per window
        if self.syn_tracker[src_ip] > self.SYN_FLOOD_THRESHOLD and src_ip not in self.syn_alerted:
            syn_ack_ratio = self.syn_ack_tracker[src_ip] / max(self.syn_tracker[src_ip], 1)
            if syn_ack_ratio < self.SYN_FLOOD_RATIO:
                self.alert("SYN_FLOOD", 
                          f"{src_ip} sent {self.syn_tracker[src_ip]} SYNs (ratio: {syn_ack_ratio:.2f})",
                          "CRITICAL")
                self.syn_alerted.add(src_ip)
    
    def detect_arp_spoof(self, ip, mac):
        """Signature-based: Detect ARP spoofing"""
        if ip in self.arp_table and self.arp_table[ip] != mac:
            self.alert("ARP_SPOOF",
                      f"IP {ip} MAC changed: {self.arp_table[ip]} → {mac}",
                      "HIGH")
        self.arp_table[ip] = mac
    
    def detect_icmp_flood(self, src_ip):
        """Signature-based: Detect ICMP flood attacks"""
        current_time = time.time()
        # Add current timestamp
        self.icmp_tracker[src_ip].append(current_time)
        # Remove old timestamps outside the window
        self.icmp_tracker[src_ip] = [
            ts for ts in self.icmp_tracker[src_ip] 
            if current_time - ts <= self.icmp_window
        ]
        # Check if threshold exceeded
        if len(self.icmp_tracker[src_ip]) > self.ICMP_FLOOD_THRESHOLD:
            if src_ip not in self.icmp_alerted:
                self.alert("ICMP_FLOOD",
                          f"ICMP flood from {src_ip}: {len(self.icmp_tracker[src_ip])} packets in {self.icmp_window}s",
                          "HIGH")
                self.icmp_alerted.add(src_ip)
    
    def detect_dns_tunnel(self, query_name):
        """Signature-based: Detect DNS tunneling attempts"""
        if not query_name:
            return
        
        # Check for suspiciously long subdomains (common in DNS tunneling)
        parts = query_name.split('.')
        for part in parts[:-2]:  # Exclude TLD and domain
            if len(part) > self.DNS_TUNNEL_MIN_LENGTH:
                # Check for hex-encoded data patterns
                hex_chars = sum(1 for c in part[:32] if c in '0123456789abcdefABCDEF-')
                hex_ratio = hex_chars / min(len(part), 32)
                if hex_ratio > self.DNS_TUNNEL_HEX_THRESHOLD:  # Uses global threshold
                    self.alert("DNS_TUNNEL",
                              f"Suspicious DNS query with long subdomain: {query_name[:80]}",
                              "MEDIUM")
                    return
    
    # Anomaly-based detection methods
    def detect_traffic_volume_anomaly(self):
        """Anomaly-based: Detect unusual traffic volume"""
        if not self.anomaly_detector or not self.anomaly_detector.trained:
            return
        
        current_time = time.time()
        window_age = current_time - self.window_start
        
        if window_age >= self.window_duration and len(self.window_packets) > 0:
            # Calculate current rates
            packet_rate = len(self.window_packets) / window_age
            total_bytes = sum(len(pkt) for pkt in self.window_packets)
            byte_rate = total_bytes / window_age
            
            # Check packet rate anomaly
            baseline_pkt = self.anomaly_detector.baseline['packet_rate']
            z_score_pkt = self.anomaly_detector.z_score(
                packet_rate, baseline_pkt['mean'], baseline_pkt['std']
            )
            
            if z_score_pkt > self.ANOMALY_Z_THRESHOLD:
                self.alert("TRAFFIC_VOLUME_ANOMALY",
                          f"Packet rate: {packet_rate:.1f} pkt/s (baseline: {baseline_pkt['mean']:.1f}±{baseline_pkt['std']:.1f}, z={z_score_pkt:.2f})",
                          "MEDIUM")
            
            # Check byte rate anomaly
            baseline_byte = self.anomaly_detector.baseline['byte_rate']
            z_score_byte = self.anomaly_detector.z_score(
                byte_rate, baseline_byte['mean'], baseline_byte['std']
            )
            
            if z_score_byte > self.ANOMALY_Z_THRESHOLD:
                self.alert("BANDWIDTH_ANOMALY",
                          f"Byte rate: {byte_rate:.0f} B/s (baseline: {baseline_byte['mean']:.0f}±{baseline_byte['std']:.0f}, z={z_score_byte:.2f})",
                          "MEDIUM")
            
            # Reset window
            self.window_packets = []
            self.window_start = current_time
    
    def detect_port_entropy_anomaly(self):
        """Anomaly-based: Detect scanning via port entropy"""
        if not self.anomaly_detector or not self.anomaly_detector.trained:
            return
        
        if len(self.dst_ports_window) > 20:  # Need enough samples
            current_entropy = self.anomaly_detector.calculate_entropy(self.dst_ports_window)
            baseline_entropy = self.anomaly_detector.baseline['port_entropy']
            
            # High entropy indicates scanning (many different ports)
            # Uses PORT_ENTROPY_MULTIPLIER from global config
            if current_entropy > baseline_entropy * self.PORT_ENTROPY_MULTIPLIER and current_entropy > 3.5:
                self.alert("HIGH_PORT_ENTROPY",
                          f"Port entropy: {current_entropy:.2f} (baseline: {baseline_entropy:.2f}) - possible scanning",
                          "MEDIUM")
                self.dst_ports_window = []
    
    def detect_timing_anomaly(self):
        """Anomaly-based: Detect unusual inter-arrival patterns"""
        if not self.anomaly_detector or not self.anomaly_detector.trained:
            return
        
        if len(self.inter_arrival_window) > 10:
            avg_inter_arrival = sum(self.inter_arrival_window) / len(self.inter_arrival_window)
            baseline = self.anomaly_detector.baseline['inter_arrival_times']
            
            z_score = self.anomaly_detector.z_score(
                avg_inter_arrival, baseline['mean'], baseline['std']
            )
            
            # Very low inter-arrival = burst attack
            if z_score > self.ANOMALY_Z_THRESHOLD and avg_inter_arrival < baseline['mean'] * 0.5:
                self.alert("BURST_TRAFFIC",
                          f"Rapid packet burst detected: {avg_inter_arrival*1000:.2f}ms avg (baseline: {baseline['mean']*1000:.2f}ms, z={z_score:.2f})",
                          "MEDIUM")
                self.inter_arrival_window = []
    
    def packet_handler(self, pkt):
        """Main packet processing function"""
        current_time = time.time()
        
        # Update anomaly detection windows
        if self.use_anomaly_detection:
            self.window_packets.append(pkt)
            
            if self.last_packet_time:
                inter_arrival = current_time - self.last_packet_time
                self.inter_arrival_window.append(inter_arrival)
                if len(self.inter_arrival_window) > 50:
                    self.inter_arrival_window.pop(0)
            
            self.last_packet_time = current_time
            
            # Run anomaly checks
            self.detect_traffic_volume_anomaly()
            self.detect_timing_anomaly()
        
        # TCP packet analysis
        if TCP in pkt and IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            dst_port = pkt[TCP].dport
            flags = pkt[TCP].flags
            
            # Track for anomaly detection
            if self.use_anomaly_detection:
                self.dst_ports_window.append(dst_port)
                if len(self.dst_ports_window) > 100:
                    self.dst_ports_window.pop(0)
                self.detect_port_entropy_anomaly()
            
            # Signature-based: Port scan detection
            self.port_scan_tracker[src_ip].add(dst_port)
            self.detect_port_scan(src_ip)
            
            # Signature-based: SYN flood detection
            if flags & 0x02:  # SYN flag
                self.syn_tracker[src_ip] += 1
                self.detect_syn_flood(src_ip)
            
            if flags & 0x12 == 0x12:  # SYN-ACK
                self.syn_ack_tracker[dst_ip] += 1
            
            if self.verbose:
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
            src_ip = pkt[IP].src
            # Detect ICMP floods (type 8 = echo request)
            if pkt[ICMP].type == 8:
                self.detect_icmp_flood(src_ip)
            if self.verbose:
                print(f"[ICMP] {src_ip} → {pkt[IP].dst} (type {pkt[ICMP].type})")
        
        # DNS packets
        elif DNS in pkt and pkt.haslayer(DNSQR):
            query_name = pkt[DNSQR].qname.decode('utf-8', errors='ignore')
            self.dns_queries.append(query_name)
            self.detect_dns_tunnel(query_name)
            if self.verbose:
                print(f"[DNS Query] {query_name}")
    
    def _get_flag_string(self, flags):
        """Convert TCP flags to readable string"""
        flag_names = []
        if flags & 0x01: flag_names.append('FIN')
        if flags & 0x02: flag_names.append('SYN')
        if flags & 0x04: flag_names.append('RST')
        if flags & 0x08: flag_names.append('PSH')
        if flags & 0x10: flag_names.append('ACK')
        return '|'.join(flag_names) if flag_names else str(flags)
    
    def print_summary(self):
        """Print detection summary"""
        print("\n" + "=" * 70)
        print("📊 DETECTION SUMMARY")
        print("=" * 70)
        print(f"\n🚨 Total Alerts: {len(self.alerts)}")
        
        if self.alert_counts:
            print("\n📈 Alerts by Type:")
            for alert_type, count in sorted(self.alert_counts.items()):
                print(f"  {alert_type}: {count}")
        
        print(f"\n📊 Statistics:")
        print(f"  Unique IPs tracked: {len(self.port_scan_tracker)}")
        print(f"  ARP table entries: {len(self.arp_table)}")
        
        if self.use_anomaly_detection and self.anomaly_detector.trained:
            print(f"  Anomaly detection: ENABLED ✓")
        else:
            print(f"  Anomaly detection: DISABLED")
        
        if self.alerts:
            print("\n🚨 Recent Alerts:")
            for alert in self.alerts[-10:]:
                print(f"  {alert}")

if __name__ == "__main__":
    print("\n🛡️  ENHANCED IDS WITH ANOMALY DETECTION")
    print("=" * 70)
    
    # Example usage
    ids = EnhancedIDS(use_anomaly_detection=True)
    
    # Train from baseline
    ids.anomaly_detector.train_from_pcap('../pcaps/baseline_normal.pcap')
    
    print("\n✅ IDS ready to process traffic")
    print("Use test_enhanced_ids.py to test with PCAP files\n")
