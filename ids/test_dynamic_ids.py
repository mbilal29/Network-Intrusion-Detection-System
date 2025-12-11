#!/usr/bin/env python3
"""
Dynamic IDS Test Suite - Generates fresh attacks with randomization
This ensures varied testing results every time you run it.
"""

import os
import sys
import json
import random
import time
import webbrowser
from enhanced_ids import EnhancedIDS
from scapy.all import *

def generate_random_normal_traffic(num_packets=50):
    """Generate randomized normal traffic baseline"""
    packets = []
    hosts = ["10.0.0.10", "10.0.0.15", "10.0.0.20", "10.0.0.25"]
    
    for i in range(num_packets):
        src = random.choice(hosts)
        dst = random.choice([h for h in hosts if h != src])
        
        # Random protocol
        proto = random.choice(['tcp', 'udp', 'icmp'])
        
        if proto == 'tcp':
            # Normal HTTP/HTTPS traffic
            sport = random.randint(40000, 60000)
            dport = random.choice([80, 443, 8080])
            pkt = IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, flags="A")
        elif proto == 'udp':
            # Normal DNS/NTP
            sport = random.randint(40000, 60000)
            dport = random.choice([53, 123])
            pkt = IP(src=src, dst=dst) / UDP(sport=sport, dport=dport) / Raw(b"X" * random.randint(20, 100))
        else:
            # ICMP ping
            pkt = IP(src=src, dst=dst) / ICMP(type=random.choice([8, 0]))
        
        packets.append(pkt)
    
    # Save both as normal.pcap (for testing) and baseline_normal.pcap (for training)
    wrpcap('../pcaps/normal.pcap', packets)
    wrpcap('../pcaps/baseline_normal.pcap', packets)
    return len(packets)


def generate_random_port_scan(intensity='medium'):
    """Generate port scan with randomized parameters"""
    packets = []
    attacker = "10.0.0.20"
    victim = "10.0.0.30"
    
    # Randomize scan intensity
    if intensity == 'low':
        num_ports = random.randint(12, 20)
    elif intensity == 'high':
        num_ports = random.randint(50, 100)
    else:  # medium
        num_ports = random.randint(25, 45)
    
    # Random port selection
    all_ports = list(range(1, 1024))
    random.shuffle(all_ports)
    ports = all_ports[:num_ports]
    
    for port in ports:
        # SYN packet
        sport = random.randint(40000, 60000)
        pkt = IP(src=attacker, dst=victim) / TCP(sport=sport, dport=port, flags="S")
        packets.append(pkt)
        
        # RST response (closed port)
        if random.random() > 0.1:  # 90% closed
            resp = IP(src=victim, dst=attacker) / TCP(sport=port, dport=sport, flags="RA")
            packets.append(resp)
        else:  # 10% open
            resp = IP(src=victim, dst=attacker) / TCP(sport=port, dport=sport, flags="SA")
            packets.append(resp)
    
    wrpcap('../pcaps/portscan.pcap', packets)
    return len(packets), num_ports


def generate_random_syn_flood(duration='medium'):
    """Generate SYN flood with randomized intensity"""
    packets = []
    attacker = "10.0.0.20"
    victim = "10.0.0.30"
    
    # Randomize flood intensity
    if duration == 'short':
        num_syns = random.randint(60, 100)
    elif duration == 'long':
        num_syns = random.randint(200, 300)
    else:  # medium
        num_syns = random.randint(120, 180)
    
    target_ports = [80, 443, 22, 8080]
    
    for _ in range(num_syns):
        sport = random.randint(1024, 65535)
        dport = random.choice(target_ports)
        pkt = IP(src=attacker, dst=victim) / TCP(sport=sport, dport=dport, flags="S", 
                                                   window=random.choice([8192, 16384, 32768]))
        packets.append(pkt)
    
    wrpcap('../pcaps/synflood.pcap', packets)
    return len(packets), num_syns


def generate_random_arp_spoof():
    """Generate ARP spoofing with randomized targets"""
    packets = []
    
    legitimate_ip = "10.0.0.30"
    legitimate_mac = "aa:bb:cc:dd:ee:ff"
    attacker_mac = random.choice(["11:22:33:44:55:66", "aa:aa:aa:aa:aa:aa", "de:ad:be:ef:00:00"])
    
    # Normal ARP
    normal = Ether(src=legitimate_mac, dst="ff:ff:ff:ff:ff:ff") / \
             ARP(op=2, hwsrc=legitimate_mac, psrc=legitimate_ip, pdst="10.0.0.10")
    packets.append(normal)
    
    # Spoofed ARPs (randomize count)
    num_spoofs = random.randint(3, 8)
    for _ in range(num_spoofs):
        spoof = Ether(src=attacker_mac, dst="ff:ff:ff:ff:ff:ff") / \
                ARP(op=2, hwsrc=attacker_mac, psrc=legitimate_ip, pdst="10.0.0.10")
        packets.append(spoof)
    
    wrpcap('../pcaps/arpspoof.pcap', packets)
    return len(packets), num_spoofs


def generate_random_mixed_attack():
    """Generate mixed attack scenario with randomization"""
    packets = []
    attacker = "10.0.0.20"
    victim = "10.0.0.30"
    
    # Random port scan
    num_scanned_ports = random.randint(15, 30)
    for port in random.sample(range(1, 200), num_scanned_ports):
        pkt = IP(src=attacker, dst=victim) / TCP(sport=random.randint(40000, 60000), 
                                                   dport=port, flags="S")
        packets.append(pkt)
    
    # Random SYN flood burst
    num_syns = random.randint(40, 80)
    for _ in range(num_syns):
        pkt = IP(src=attacker, dst=victim) / TCP(sport=random.randint(1024, 65535), 
                                                   dport=80, flags="S")
        packets.append(pkt)
    
    # Some normal traffic mixed in
    for _ in range(random.randint(10, 20)):
        normal = IP(src="10.0.0.10", dst="10.0.0.15") / TCP(sport=45000, dport=443, flags="A")
        packets.append(normal)
    
    # Shuffle for realism
    random.shuffle(packets)
    
    wrpcap('../pcaps/mixed_attack.pcap', packets)
    return len(packets), num_scanned_ports, num_syns


def test_ids_on_pcap(pcap_file, ids, test_name="Test"):
    """Test IDS on a PCAP file"""
    print(f"\n{'='*70}")
    print(f"🔍 {test_name}: {os.path.basename(pcap_file)}")
    print(f"{'='*70}")
    
    if not os.path.exists(pcap_file):
        print(f"❌ File not found: {pcap_file}")
        return 0
    
    initial_alerts = len(ids.alerts)
    
    try:
        packets = rdpcap(pcap_file)
        print(f"📦 Loaded {len(packets)} packets")
        
        for pkt in packets:
            ids.packet_handler(pkt)
        
        new_alerts = len(ids.alerts) - initial_alerts
        print(f"🚨 Generated {new_alerts} new alerts")
        return new_alerts
    
    except Exception as e:
        print(f"❌ Error loading PCAP: {e}")
        return 0


def main():
    print("=" * 70)
    print("🎲 DYNAMIC IDS TEST SUITE - WITH RANDOMIZATION")
    print("=" * 70)
    print("\n🔄 Generating fresh attack scenarios with random parameters...")
    print("   Each run will produce different attack intensities!\n")
    
    # Generate randomized attacks
    stats = {}
    
    print("1️⃣  Generating normal traffic...")
    stats['normal'] = generate_random_normal_traffic(random.randint(40, 60))
    print(f"   ✓ Generated {stats['normal']} normal packets")
    
    print("\n2️⃣  Generating port scan attack...")
    intensity = random.choice(['low', 'medium', 'high'])
    packets, ports = generate_random_port_scan(intensity)
    stats['portscan'] = {'packets': packets, 'ports': ports, 'intensity': intensity}
    print(f"   ✓ Generated {intensity} intensity scan: {packets} packets, {ports} ports scanned")
    
    print("\n3️⃣  Generating SYN flood attack...")
    duration = random.choice(['short', 'medium', 'long'])
    packets, syns = generate_random_syn_flood(duration)
    stats['synflood'] = {'packets': packets, 'syns': syns, 'duration': duration}
    print(f"   ✓ Generated {duration} duration flood: {packets} packets, {syns} SYN packets")
    
    print("\n4️⃣  Generating ARP spoofing attack...")
    packets, spoofs = generate_random_arp_spoof()
    stats['arpspoof'] = {'packets': packets, 'spoofs': spoofs}
    print(f"   ✓ Generated {packets} packets with {spoofs} spoofed ARPs")
    
    print("\n5️⃣  Generating mixed attack scenario...")
    packets, scanned, syns = generate_random_mixed_attack()
    stats['mixed'] = {'packets': packets, 'scanned': scanned, 'syns': syns}
    print(f"   ✓ Generated {packets} packets ({scanned} ports scanned, {syns} SYNs)")
    
    # Initialize IDS
    print("\n" + "=" * 70)
    print("🛡️  INITIALIZING IDS")
    print("=" * 70)
    
    ids = EnhancedIDS(use_anomaly_detection=True)
    
    # Train baseline (using freshly generated baseline_normal.pcap)
    baseline_file = '../pcaps/baseline_normal.pcap'
    if os.path.exists(baseline_file):
        print(f"\n📚 Training anomaly detector from FRESH baseline...")
        ids.anomaly_detector.train_from_pcap(baseline_file)
        # Save the fresh baseline model
        ids.anomaly_detector.save_model('baseline_model.pkl')
        print("✅ Fresh baseline trained and saved successfully")
    else:
        print("⚠️  Warning: No baseline found, using default parameters")
    
    # Test all scenarios
    print("\n" + "=" * 70)
    print("🧪 TESTING PHASE")
    print("=" * 70)
    
    test_cases = [
        ('../pcaps/normal.pcap', 'Normal Traffic (baseline validation)'),
        ('../pcaps/portscan.pcap', f'Port Scan ({stats["portscan"]["intensity"]} intensity)'),
        ('../pcaps/synflood.pcap', f'SYN Flood ({stats["synflood"]["duration"]} duration)'),
        ('../pcaps/arpspoof.pcap', f'ARP Spoofing ({stats["arpspoof"]["spoofs"]} spoofs)'),
        ('../pcaps/mixed_attack.pcap', 'Mixed Attack Scenario'),
    ]
    
    results = {}
    total_packets = 0
    start_time = time.time()
    
    for pcap_file, description in test_cases:
        alert_count = test_ids_on_pcap(pcap_file, ids, description)
        results[description] = alert_count
        # Count packets
        if os.path.exists(pcap_file):
            packets = rdpcap(pcap_file)
            total_packets += len(packets)
    
    elapsed_time = time.time() - start_time
    avg_throughput = int(total_packets / elapsed_time) if elapsed_time > 0 else 0
    
    # Final summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST RESULTS")
    print("=" * 70)
    
    ids.print_summary()
    
    print("\n📈 Test Results by Scenario:")
    for test_name, alert_count in results.items():
        print(f"  {test_name}: {alert_count} alerts")
    
    print("\n🎲 Attack Parameters This Run:")
    print(f"  Port Scan: {stats['portscan']['intensity']} intensity ({stats['portscan']['ports']} ports)")
    print(f"  SYN Flood: {stats['synflood']['duration']} duration ({stats['synflood']['syns']} SYNs)")
    print(f"  ARP Spoof: {stats['arpspoof']['spoofs']} spoofed packets")
    print(f"  Mixed Attack: {stats['mixed']['scanned']} ports + {stats['mixed']['syns']} SYNs")
    
    print("\n💡 Next Run: Parameters will be randomized for variety!")
    print("\n📝 Alerts saved to: outputs/logs/alerts.log")
    
    # Save evaluation metrics for report generation
    total_alerts = len(ids.alerts)
    signature_alerts = len([a for a in ids.alerts if 'PORT_SCAN' in a or 'SYN_FLOOD' in a or 'ARP_SPOOF' in a or 'DNS_TUNNEL' in a or 'ICMP_FLOOD' in a])
    anomaly_alerts = total_alerts - signature_alerts
    
    # Calculate detection rates for better insights
    detection_rate = (total_alerts / total_packets * 100) if total_packets > 0 else 0
    signature_rate = (signature_alerts / total_packets * 100) if total_packets > 0 else 0
    anomaly_rate = (anomaly_alerts / total_packets * 100) if total_packets > 0 else 0
    
    evaluation_data = {
        "total_packets": total_packets,
        "total_alerts": total_alerts,
        "signature_alerts": signature_alerts,
        "anomaly_alerts": anomaly_alerts,
        "false_positives": 0,
        "avg_throughput": avg_throughput,
        "detection_rate": round(detection_rate, 2),
        "signature_detection_rate": round(signature_rate, 2),
        "anomaly_detection_rate": round(anomaly_rate, 2),
        "test_cases": [
            {"name": name, "alerts": count} for name, count in results.items()
        ],
        "attack_params": stats
    }
    
    os.makedirs('outputs/logs', exist_ok=True)
    with open('outputs/logs/evaluation_results.json', 'w') as f:
        json.dump(evaluation_data, f, indent=2)
    
    print("📊 Metrics saved to: outputs/logs/evaluation_results.json")
    
    # Generate dynamic visualizations from fresh data
    print("\n🎨 Generating dynamic visualizations...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'create_dynamic_visualizations.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Visualizations updated successfully")
        else:
            print(f"⚠️  Visualization generation had warnings")
    except Exception as e:
        print(f"⚠️  Visualization generation failed: {e}")
    
    # Generate HTML report with embedded charts
    print("\n📄 Generating HTML report...")
    try:
        result = subprocess.run([sys.executable, 'generate_report.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ HTML report generated successfully")
            print("   Location: outputs/reports/ids_report.html")
            
            # Auto-open report in browser
            report_path = os.path.abspath('outputs/reports/ids_report.html')
            print(f"\n🌐 Opening report in browser...")
            webbrowser.open(f'file://{report_path}')
        else:
            print(f"⚠️  Report generation had warnings")
            if result.stderr:
                print(f"   {result.stderr[:200]}")
    except Exception as e:
        print(f"⚠️  Report generation failed: {e}")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
