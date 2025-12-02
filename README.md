# Network Intrusion Detection System (NIDS)

**CSCD58 Course Project** | University of Toronto  
**Authors:** Bilal & Zuhair  
**Date:** December 2025

---

## 🎯 Quick Start

### Generate Comprehensive Report
```bash
cd ids/
python3 generate_report.py
open ids_report.html  # View professional HTML report
```

### Run Enhanced IDS with Dual Detection
```bash
cd ids/
python3 test_enhanced_ids.py ../pcaps/entropy_scan.pcap
```

### View Results
```bash
cat ids/alerts.log                      # Real-time detection alerts
cat ids/evaluation_results.json         # Performance metrics (JSON)
open ids/ids_report.html                # Professional report with charts
```

## ✨ Features

### Dual Detection Architecture
- ✅ **Signature-Based Detection**
  - Port Scan Detection - 100% detection rate
  - ARP Spoofing Detection - 100% detection rate
  - SYN Flood Detection - Rate-based algorithm

- ✅ **Anomaly-Based Detection**
  - Shannon Entropy Analysis (port distribution)
  - Z-Score Traffic Volume Detection (3σ thresholds)
  - Inter-Arrival Time Analysis (burst detection)
  - Statistical Baseline Profiling (1,052 training packets)

- ✅ **Zero False Positives** on normal traffic
- ⚡ **High Performance** - 21,090 packets/second average throughput

## 📊 Test Results Summary

### Overall Performance
| Metric | Value |
|--------|-------|
| Total Packets Analyzed | 3,548 |
| Signature Alerts | 53 |
| Anomaly Alerts | 8 |
| False Positive Rate | 0.00% |
| Avg Throughput | 21,090 pkt/s |

### Detection Rates
| Attack Type | Packets | Detection Rate | Alerts |
|-------------|---------|----------------|--------|
| Port Scan (Signature) | 50 | 100% | 4 |
| ARP Spoofing | 2 | 100% | 1 |
| High Entropy Scan (Anomaly) | 499 | 100% | 8 HIGH_PORT_ENTROPY |
| Normal Traffic | 50 | 0% (no false positives) | 0 |

## 🏗️ Architecture

```
┌──────────┐    ┌────────────────┐    ┌──────────┐
│ Sniffer  │ -> │   Detector     │ -> │  Logger  │
│          │    │ [Signature +   │    │          │
│          │    │  Anomaly]      │    │          │
└──────────┘    └────────────────┘    └──────────┘
                      ↑
                      │
                ┌─────┴─────┐
                │  Baseline │
                │  Training │
                └───────────┘
```

## 📁 Project Structure

### Core Files for Evaluation

```
├── README.md                           # This file
├── FINAL_REPORT.md                     # Comprehensive technical documentation
├── DEMO_SCRIPT.md                      # Presentation guide with talking points
├── SUBMISSION_CHECKLIST.md             # Pre-submission verification
├── ANOMALY_DETECTION_SUMMARY.md        # Enhancement documentation
├── READY_FOR_SUBMISSION.md             # Submission readiness checklist
│
├── ids/                                # IDS Implementation
│   ├── enhanced_ids.py                 # Dual detection IDS (signature + anomaly)
│   ├── simple_ids.py                   # Original signature-based IDS
│   ├── sniffer.py                      # Packet capture demo
│   │
│   ├── generate_baseline.py            # Normal traffic generator (1,052 pkts)
│   ├── generate_anomaly_attacks.py     # Advanced attack generator
│   ├── generate_traffic.py             # Original attack generator
│   │
│   ├── test_enhanced_ids.py            # Dual detection test suite
│   ├── test_anomaly_detection.py       # Focused anomaly tests
│   ├── test_pcap.py                    # Basic PCAP testing
│   │
│   ├── evaluate_enhanced_ids.py        # Comprehensive evaluator
│   ├── evaluate_results.py             # Original evaluator
│   │
│   ├── create_visualizations.py        # Matplotlib chart generator
│   ├── generate_report.py              # HTML report generator (SOC tool)
│   │
│   ├── baseline_model.pkl              # Trained anomaly detector
│   ├── evaluation_results.json         # Performance metrics
│   ├── ids_report.html                 # Professional HTML report
│   └── *.png                           # 6 visualization charts
│
├── pcaps/                              # Test Traffic
│   ├── baseline_normal.pcap            # Training data (1,052 packets)
│   ├── portscan.pcap                   # Port scan attack
│   ├── synflood.pcap                   # SYN flood attack
│   ├── arpspoof.pcap                   # ARP spoofing attack
│   ├── normal.pcap                     # Normal traffic
│   ├── mixed_attack.pcap               # Combined attacks
│   ├── entropy_scan.pcap               # High-entropy port scan
│   ├── volume_spike.pcap               # Traffic volume anomaly
│   ├── burst_attack.pcap               # Timing burst anomaly
│   ├── bandwidth_attack.pcap           # Bandwidth anomaly
│   └── asymmetric_flow.pcap            # Flow asymmetry anomaly
│
├── docker/                             # Docker Deployment
│   ├── Dockerfile.ids                  # IDS container
│   ├── Dockerfile.attacker             # Attack generator (Kali)
│   └── Dockerfile.victim               # Target system (Ubuntu)
│
├── docker-compose.yml                  # Container orchestration
└── docs/archive/                       # Archived development docs
    ├── PROJECT_COMPLETE.md
    ├── PROJECT_STATUS.md
    ├── CURRENT_STATUS.md
    ├── FAST_TRACK.md
    ├── QUICKSTART.md
    └── ARCHITECTURE.md
```

### Archived / Development Documentation

The `docs/archive/` folder contains mid-project status updates and development notes kept for project history. **These are NOT part of the core submission** - refer to the root-level documentation files for evaluation.

## 🚀 Usage Examples

### Generate Test Traffic
```bash
cd ids/
python3 generate_traffic.py
```

### Run Full Evaluation
```bash
cd ids/
python3 evaluate_results.py
```

### Live Capture (requires sudo)
```bash
cd ids/
sudo python3 simple_ids.py
```

## 🛠️ Requirements

- Python 3.9+
- Scapy 2.6.1
- Docker (optional, for containerized deployment)

### Install Dependencies
```bash
pip3 install scapy
```

## 🔍 Detection Algorithms

### Port Scan Detection
- Tracks unique destination ports per source IP
- Threshold: 11+ ports in 5 seconds
- 100% detection on test cases

### ARP Spoofing Detection
- Maintains ARP cache (IP → MAC)
- Detects MAC address changes
- Alerts on cache poisoning attempts

### SYN Flood Detection
- Monitors SYN packet rate
- Analyzes SYN/ACK ratio
- Threshold: 50+ SYNs with <10% ACK

## 📈 Performance Metrics

- **Throughput:** 21,672 packets/second
- **Latency:** < 1ms per packet
- **False Positives:** 0 on normal traffic
- **Detection Rate:** 100% for implemented attacks

## 📚 Documentation

- **[FINAL_REPORT.md](FINAL_REPORT.md)** - Complete project report with detailed analysis
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical details
- **[FAST_TRACK.md](FAST_TRACK.md)** - Quick completion guide

## 🏆 Key Achievements

✅ Functional IDS with 3 detection algorithms  
✅ Zero false positives on baseline traffic  
✅ Professional PCAP-based testing methodology  
✅ High-performance packet processing (21k+ pps)  
✅ Comprehensive documentation & evaluation  

## ⚠️ Known Limitations

- SYN flood detection requires live capture (PCAP files have static timestamps)
- Port scan detection may miss slow scans (>5 sec between ports)
- Docker build blocked by external repository issues (infrastructure problem, not code)

## 📝 License

Academic project for CSCD58 - University of Toronto

---

**For detailed technical information and analysis, see [FINAL_REPORT.md](FINAL_REPORT.md)**



This project runs on a Docker-based virtual network consisting of three isolated containers:

- **IDS**
- **Attacker**
- **Victim**

All containers communicate on a custom Docker subnet (`ids-net`) to safely simulate and analyze malicious traffic.

## 🛠️ 1. Prerequisites

Install:

- **Docker Desktop** (macOS/Windows/Linux)

## 🌐 2. Create the Docker Network

This network acts like a LAN switch, allowing the IDS to monitor attacker → victim traffic.

```bash
docker network create --subnet=10.0.0.0/24 ids-net
```

## 🧱 3. Build and Launch the Environment

Run from the project root:

```bash
docker-compose up --build
```

This will:

- ✔ Build all 3 Docker images
- ✔ Start attacker, victim, and IDS containers
- ✔ Connect them to the `ids-net` network
- ✔ Assign static IPs:
  - **IDS** → `10.0.0.10`
  - **Attacker** → `10.0.0.20`
  - **Victim** → `10.0.0.30`

If everything builds correctly, you will see:

```
✔ network-intrusion-detection-system-attacker Built
✔ network-intrusion-detection-system-ids Built
✔ network-intrusion-detection-system-victim Built
✔ Container attacker Created
✔ Container ids Created
✔ Container victim Created
```

## 🖥️ 4. Opening Shells Inside Each Container

Open 3 separate terminals for easy testing.

**Attacker**
```bash
docker exec -it attacker bash
```

**Victim**
```bash
docker exec -it victim bash
```

**IDS Node**
```bash
docker exec -it ids bash
```

