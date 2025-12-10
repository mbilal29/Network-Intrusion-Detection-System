# Network Intrusion Detection System (NIDS)

**CSCD58 Course Project** | University of Toronto  
**Authors:** Bilal & Zuhair  
**Date:** December 2025

---

## 🎯 Quick Start

### 🎪 Interactive Demos (No Report)
```bash
cd ids/
python3 demo_terminal_attacks.py    # Menu-driven, choose attacks
python3 run_all_demos.py            # All attacks in 30 seconds
```
*Perfect for live demonstrations - shows real-time detection*

### 📊 Full Reports (With Visualizations)
```bash
# Fast synthetic testing (10 seconds)
cd ids/
python3 test_dynamic_ids.py

# Realistic Docker environment (60 seconds) - RECOMMENDED
python3 workflow_docker_comprehensive.py
```
*Generates complete HTML report with 6 charts + metrics*

### 📂 View Results
```bash
open ids/outputs/reports/ids_report.html         # HTML report with charts
cat ids/outputs/logs/alerts.log                  # Detection alerts
cat ids/outputs/logs/evaluation_results.json     # Performance metrics
```

---

## ✨ Features

### Dual Detection Architecture
- ✅ **Signature-Based Detection**
  - Port Scan Detection (threshold-based)
  - SYN Flood Detection (rate + ratio-based)
  - ICMP Flood Detection (sliding window)
  - DNS Tunneling Detection (length + hex pattern)
  - ARP Spoofing Detection (MAC tracking)

- ✅ **Anomaly-Based Detection**
  - Shannon Entropy Analysis (port distribution)
  - Z-Score Traffic Volume Detection (3σ thresholds)
  - Inter-Arrival Time Analysis (burst detection)
  - Statistical Baseline Profiling

### Professional Reporting
- ✅ **6 Visualization Charts** - Alert types, timeline, severity, top IPs
- ✅ **Detailed Metrics** - Detection rates, performance stats
- ✅ **HTML Dashboard** - Professional corporate design

### Docker Integration
- ✅ **Real Attack Tools** - nmap, hping3, arpspoof, dig
- ✅ **Network Isolation** - 3 isolated containers (attacker/victim/IDS)
- ✅ **Real Traffic Capture** - tcpdump-based PCAP generation

---

## 📊 Results

### Detection Performance
| Attack Type | Detection Rate | Alerts Generated |
|-------------|----------------|------------------|
| Port Scans | 100% | 35+ per test |
| SYN Floods | 100% | 1 per test |
| ICMP Floods | 100% | 1 per test |
| DNS Tunneling | 100% | 15 per test |
| Port Entropy Anomaly | 100% | 11 per test |
| Normal Traffic | 0% false positives | 0 |

### Key Metrics (Docker Workflow)
- **Total Alerts:** 60-70 per comprehensive test
- **Signature-Based:** 52 alerts
- **Anomaly-Based:** 11 alerts
- **False Positive Rate:** 0.00%
- **Test Duration:** ~60 seconds

---

## 🔧 Customization

All detection thresholds are configurable in `enhanced_ids.py`:

```python
self.PORT_SCAN_THRESHOLD = 10          # Alert after 10 unique ports
self.SYN_FLOOD_THRESHOLD = 50          # Alert after 50 SYN packets
self.ICMP_FLOOD_THRESHOLD = 50         # Alert after 50 ICMP in 5s
self.DNS_TUNNEL_MIN_LENGTH = 30        # Alert if subdomain > 30 chars
self.ANOMALY_Z_THRESHOLD = 3.0         # Alert if z-score > 3.0
```

**To test threshold changes:**
1. Modify values in `enhanced_ids.py`
2. Run `python3 workflow_docker_comprehensive.py`
3. Changes reflected in generated report

See `docs/TESTING_AND_CUSTOMIZATION.md` for detailed examples.

---

## 🏗️ Architecture

```
┌──────────────┐    ┌────────────────────┐    ┌──────────────┐
│   Packets    │ -> │  Dual Detector     │ -> │   Alerts     │
│  (Scapy)     │    │  ┌─────────────┐   │    │  (JSON/Log)  │
│              │    │  │ Signature   │   │    │              │
│              │    │  │ Detection   │   │    │              │
│              │    │  └─────────────┘   │    │              │
│              │    │  ┌─────────────┐   │    │              │
│              │    │  │ Anomaly     │   │    │              │
│              │    │  │ Detection   │   │    │              │
│              │    │  └─────────────┘   │    │              │
└──────────────┘    └────────────────────┘    └──────────────┘
                           ↑
                           │
                    ┌──────┴──────┐
                    │  Baseline   │
                    │  Training   │
                    └─────────────┘
```

---

## 📁 Project Structure

```
Network-Intrusion-Detection-System/
├── README.md                    # Project overview
├── TESTING_GUIDE.md            # How to test both workflows
├── FINAL_REPORT.md             # Technical documentation
├── docker-compose.yml          # Container orchestration
├── docker/                     # Dockerfiles
│   ├── Dockerfile.ids          # IDS container
│   ├── Dockerfile.attacker     # Attack generator
│   └── Dockerfile.victim       # Target system
├── pcaps/                      # Test traffic captures
└── ids/                        # Core IDS implementation
    ├── enhanced_ids.py         # Main IDS with dual detection
    ├── run_complete_test.py    # Fast Python workflow
    ├── run_docker_workflow.py  # Docker hybrid workflow
    ├── test_dynamic_ids.py     # Randomized attack generator
    ├── test_docker_hybrid.py   # Docker + Scapy hybrid
    ├── create_dynamic_visualizations.py  # Chart generation
    ├── generate_report.py      # HTML report builder
    └── outputs/                # Generated files
        ├── visualizations/     # PNG charts
        ├── reports/           # HTML reports
        └── logs/              # Alerts and metrics
```

---

## 🚀 Two Testing Workflows

### 1. Python Workflow (Fast)
**Best for:** Development, quick testing, debugging
```bash
cd ids/
python3 run_complete_test.py
```
- Generates randomized attacks with Scapy
- Tests IDS with dual detection
- Creates visualizations and HTML report
- **Time:** 10-20 seconds

### 2. Docker Workflow (Realistic)
**Best for:** Demonstrations, realistic network simulation
```bash
docker-compose up -d
cd ids/
python3 run_docker_workflow.py
```
- Executes **real** attack tools (nmap, hping3, arping)
- Runs in isolated Docker containers
- Generates PCAPs and analyzes with IDS
- Creates visualizations and HTML report
- **Time:** 30-45 seconds

---

## 📊 Output Files

All outputs are automatically organized:

```
ids/outputs/
├── visualizations/
│   ├── alert_distribution.png        # Alert types breakdown
│   ├── severity_distribution.png     # Severity levels
│   ├── detection_summary.png         # Detection statistics
│   ├── attack_timeline.png           # Temporal analysis
│   ├── baseline_statistics.png       # Normal traffic profile
│   └── performance_metrics.png       # Throughput graphs
├── reports/
│   └── ids_report.html               # Comprehensive report
└── logs/
    ├── alerts.log                     # All detected alerts
    └── evaluation_results.json        # Performance metrics
```

---

## 🔧 Requirements

### Python Dependencies
```bash
pip3 install scapy matplotlib numpy
```

### Docker (Optional)
- Docker Desktop installed and running
- Containers: `ids`, `attacker`, `victim`

---

## 📖 Documentation

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Step-by-step testing instructions
- **[FINAL_REPORT.md](FINAL_REPORT.md)** - Technical implementation details
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Docker configuration guide

---

## 🎓 Key Achievements

1. ✅ **Dual Detection System** - Signature + Anomaly detection
2. ✅ **100% Detection Rate** - All attacks detected with 0% false positives
3. ✅ **Fully Dynamic** - All metrics from actual tests, not hardcoded
4. ✅ **Docker Integration** - Real attack tools in isolated network
5. ✅ **Professional Reports** - HTML reports with embedded visualizations
6. ✅ **Organized Structure** - Clean separation of code and outputs

---

## 👥 Authors

**Bilal** & **Zuhair**  
CSCD58 - Computer Security | University of Toronto  
December 2025
