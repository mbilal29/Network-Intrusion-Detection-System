# IDS Architecture & System Design

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Docker Virtual Network (ids-net)              │
│                    10.0.0.0/24                          │
└─────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   IDS NODE      │  │   ATTACKER      │  │    VICTIM       │
│   10.0.0.10     │  │   10.0.0.20     │  │   10.0.0.30     │
│                 │  │                 │  │                 │
│ • Scapy         │  │ • Nmap          │  │ • HTTP Server   │
│ • PyShark       │  │ • hping3        │  │ • SSH           │
│ • Detector      │  │ • Scapy         │  │ • Normal        │
│ • Logger        │  │ • arpspoof      │  │   Services      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 🔍 What Each Component Does

### 1. IDS Node (10.0.0.10) - Python Container

This is **your defensive machine** that:

#### Components to Build:
1. **Sniffer** (`sniffer.py`) ✅ DONE
   - Captures all packets on `eth0`
   - Parses L2/L3/L4 headers
   - Extracts: IPs, ports, protocols, flags, MACs

2. **Detection Engine** (`detection_engine.py`) ⬜ NEXT
   - Receives parsed packets
   - Maintains state (flows, connections, ARP table)
   - Runs detection rules
   - Generates alerts

3. **Flow Tracker** (`flow_tracker.py`)
   - Groups packets by (src_ip, dst_ip, src_port, dst_port, protocol)
   - Tracks per-flow statistics:
     - Packet count
     - Byte count
     - Duration
     - Flags seen
     - Timing patterns

4. **Anomaly Detector** (`anomaly_detector.py`)
   - Statistical analysis
   - Entropy calculations
   - Threshold-based alerts

5. **Logger** (`logger.py`)
   - Writes alerts to `logs/alerts.log`
   - Writes flow data to `logs/traffic.csv`
   - Timestamped, structured output

---

### 2. Attacker Node (10.0.0.20) - Kali Linux

This is the **red team machine** that generates attacks:

#### Installed Tools:
- **nmap** - Port scanning
- **hping3** - SYN flooding, packet crafting
- **Scapy (Python)** - ARP spoofing, custom packets
- **arpspoof** - ARP poisoning
- **dns2tcp** (optional) - DNS tunneling

#### Attack Scenarios You'll Run:
1. **Port Scan**
   ```bash
   nmap -sS 10.0.0.30        # SYN scan
   nmap -sT 10.0.0.30        # Full connect scan
   nmap -p 1-1000 10.0.0.30  # Range scan
   ```

2. **SYN Flood**
   ```bash
   hping3 --flood --syn -p 80 10.0.0.30
   ```

3. **ARP Spoofing**
   ```python
   from scapy.all import *
   send(ARP(op=2, psrc="10.0.0.10", pdst="10.0.0.30", hwdst="ff:ff:ff:ff:ff:ff"))
   ```

---

### 3. Victim Node (10.0.0.30) - Ubuntu

This is the **target machine**:

#### Role:
- Responds to normal traffic (ping, HTTP, SSH)
- Target of attacks
- Generates legitimate baseline traffic

#### Setup:
```bash
# Start simple HTTP server
python3 -m http.server 8080

# Or run SSH
service ssh start
```

---

## 🧠 Detection Logic You'll Implement

### Signature-Based Detection

#### 1. Port Scan Detection
**Pattern:** Many SYN packets to different ports from one source

**Logic:**
```python
# Pseudo-code
if (unique_ports_hit[src_ip] > 10) and (time_window < 5 seconds):
    alert("Port Scan Detected", src_ip)
```

**What to track:**
- Per-source: set of destination ports
- Time window (sliding window of last N seconds)
- SYN packets without completed handshakes

---

#### 2. SYN Flood Detection
**Pattern:** Very high rate of SYN packets with low SYN/ACK ratio

**Logic:**
```python
# Pseudo-code
syn_count = count(TCP.flags == 'S')
ack_count = count(TCP.flags == 'SA')  # SYN-ACK

if (syn_count > 100/sec) and (ack_count / syn_count < 0.1):
    alert("SYN Flood Detected", src_ip)
```

**What to track:**
- SYN packet rate per source
- SYN-ACK responses
- Time windows (1 sec, 5 sec, 10 sec)

---

#### 3. ARP Spoofing Detection
**Pattern:** IP address maps to multiple MAC addresses

**Logic:**
```python
# Pseudo-code
if (ip_to_mac_table[ip] exists) and (new_mac != stored_mac):
    alert("ARP Spoof Detected", ip, old_mac, new_mac)
```

**What to track:**
- ARP table: {IP → MAC}
- Unsolicited ARP replies
- Frequency of ARP updates

---

### Anomaly-Based Detection

#### 1. Traffic Volume Anomalies
**What to measure:**
- Packets per second (per host)
- Bytes per second
- Connection attempts per second

**Detection:**
```python
# Z-score method
z_score = (current_rate - mean_rate) / std_dev
if abs(z_score) > 3:
    alert("Traffic Anomaly", host, feature)
```

---

#### 2. Entropy-Based Detection
**Concept:** Attackers create predictable patterns

**Measure entropy of:**
- Destination ports (port scanning → high entropy)
- Destination IPs (DDoS → low entropy)
- Packet sizes

**Formula:**
```python
import numpy as np

def calculate_entropy(values):
    _, counts = np.unique(values, return_counts=True)
    probabilities = counts / counts.sum()
    return -np.sum(probabilities * np.log2(probabilities))
```

**Detection:**
```python
port_entropy = calculate_entropy(destination_ports)
if port_entropy > 4.0:  # Threshold
    alert("High Port Entropy - Possible Scan")
```

---

#### 3. Behavioral Anomalies
**Per-host baselines:**
- Average packets/sec
- Typical port usage
- Connection duration patterns

**Detection:**
- Compare current vs. historical behavior
- Flag deviations beyond threshold

---

## 📊 Data Structures You Need

### 1. Flow Table
```python
flows = {
    (src_ip, dst_ip, src_port, dst_port, proto): {
        'packet_count': int,
        'byte_count': int,
        'start_time': float,
        'last_seen': float,
        'flags_seen': set(),  # {'S', 'A', 'F', ...}
        'syn_count': int,
        'ack_count': int
    }
}
```

### 2. Host Statistics
```python
host_stats = {
    src_ip: {
        'unique_dst_ports': set(),
        'packet_rate': float,  # pkts/sec
        'byte_rate': float,    # bytes/sec
        'connection_attempts': int,
        'last_updated': float
    }
}
```

### 3. ARP Table
```python
arp_table = {
    ip_address: {
        'mac': str,
        'first_seen': float,
        'last_updated': float,
        'update_count': int
    }
}
```

---

## 🔄 Packet Processing Pipeline

```
Packet Arrives on eth0
        │
        ▼
┌───────────────────┐
│  Scapy Sniffer    │  ← sniffer.py
│  (packet_handler) │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Parse Packet     │  ← Extract IPs, ports, flags
│  Fields           │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Update Flow      │  ← flow_tracker.py
│  State            │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Run Detection    │  ← detection_engine.py
│  Rules            │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Generate Alert?  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Log to File      │  ← logger.py
└───────────────────┘
```

---

## 🚀 Implementation Order (What YOU Should Build)

### Phase 1: Core Infrastructure (Today)
1. ✅ `sniffer.py` - Basic packet capture
2. ⬜ Test with real traffic
3. ⬜ `logger.py` - Simple file logging

### Phase 2: Flow Tracking (Day 2)
4. ⬜ `flow_tracker.py` - Group packets into flows
5. ⬜ Track per-host statistics
6. ⬜ Maintain ARP table

### Phase 3: Signature Detection (Day 3-4)
7. ⬜ `detection_engine.py` - Main detection logic
8. ⬜ Implement port scan detection
9. ⬜ Implement SYN flood detection
10. ⬜ Implement ARP spoof detection

### Phase 4: Anomaly Detection (Day 5)
11. ⬜ `anomaly_detector.py` - Statistical analysis
12. ⬜ Calculate entropy
13. ⬜ Z-score thresholds
14. ⬜ Behavioral baseline

### Phase 5: Integration & Testing (Day 6-7)
15. ⬜ Connect all components
16. ⬜ Run full attack scenarios
17. ⬜ Measure performance
18. ⬜ Generate graphs
19. ⬜ Write report

---

## 📚 Key Scapy Packet Fields

### TCP Packet:
```python
if TCP in pkt:
    src_port = pkt[TCP].sport
    dst_port = pkt[TCP].dport
    flags = pkt[TCP].flags  # 'S', 'A', 'SA', 'F', 'R', 'P'
    seq = pkt[TCP].seq
    ack = pkt[TCP].ack
    window = pkt[TCP].window
```

### IP Packet:
```python
if IP in pkt:
    src_ip = pkt[IP].src
    dst_ip = pkt[IP].dst
    ttl = pkt[IP].ttl
    proto = pkt[IP].proto  # 6=TCP, 17=UDP, 1=ICMP
    length = pkt[IP].len
```

### ARP Packet:
```python
if ARP in pkt:
    op = pkt[ARP].op          # 1=request, 2=reply
    src_mac = pkt[ARP].hwsrc
    src_ip = pkt[ARP].psrc
    dst_mac = pkt[ARP].hwdst
    dst_ip = pkt[ARP].pdst
```

---

## 🎯 Success Criteria

By end of project, your IDS should:

✅ Detect port scans with <1 second latency
✅ Detect SYN floods in real-time
✅ Identify ARP spoofing attempts
✅ Generate timestamped alerts
✅ Produce meaningful graphs
✅ Have <10% false positive rate on normal traffic
✅ Work reliably in Docker environment

---

**Next Step:** Test the sniffer, then start building `detection_engine.py`
