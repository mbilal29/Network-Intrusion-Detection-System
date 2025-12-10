# Network Intrusion Detection System (NIDS)

**CSCD58 Course Project** | University of Toronto  
**Authors:** Bilal & Zuhair  
**Date:** December 2025

---

## 🎯 Quick Start

### Fast Testing (Python-Only)
```bash
cd ids/
python3 run_complete_test.py
# Generates report automatically in 10-20 seconds
```

### Docker Integration (Realistic Attacks)
```bash
docker-compose up -d
cd ids/
python3 run_docker_workflow.py
# Executes real attacks (nmap, hping3, arping) + generates report
```

### View Results
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
  - SYN Flood Detection (rate-based algorithm)
  - ARP Spoofing Detection (MAC tracking)

- ✅ **Anomaly-Based Detection**
  - Shannon Entropy Analysis (port distribution)
  - Z-Score Traffic Volume Detection (3σ thresholds)
  - Inter-Arrival Time Analysis (burst detection)
  - Statistical Baseline Profiling

### Docker Integration
- ✅ **Real Attack Tools** - nmap, hping3, arping
- ✅ **Network Isolation** - 3 isolated containers
- ✅ **Hybrid Approach** - Docker attacks + Scapy analysis

---

## 📊 Results

### Detection Performance
| Attack Type | Detection Rate | Alerts Generated |
|-------------|----------------|------------------|
| Port Scans | 100% | 8-12 per test |
| SYN Floods | 100% | 1-2 per test |
| ARP Spoofing | 100% | 15-20 per test |
| Normal Traffic | 0% false positives | 0 |

### Key Metrics
- **Throughput:** ~3,000-3,500 pkt/s
- **Total Packets:** 400-600 per test run
- **Total Alerts:** 25-35 per test run
- **False Positive Rate:** 0.00%

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
