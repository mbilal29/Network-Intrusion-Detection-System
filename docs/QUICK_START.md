# 🎯 Quick Start Guide - IDS Testing & Demo

## What You Have

Your Network Intrusion Detection System has **3 different testing workflows** for different purposes:

---

## 🚀 Quick Commands

### 1. Quick Demos (30 seconds)
```bash
cd ids/
python3 run_all_demos.py
```
**What it does**: Runs all 4 attack demos in sequence, shows detections
**Best for**: Quick validation, showcasing capabilities

### 2. Synthetic Testing (10 seconds)
```bash
cd ids/
python3 test_dynamic_ids.py
```
**What it does**: Generates random attacks, creates full report with charts
**Best for**: Fast testing, report generation

### 3. Interactive Terminal Demo (as long as you want)
```bash
cd ids/
python3 demo_terminal_attacks.py
```
**What it does**: Menu-driven interface, run attacks one at a time
**Best for**: Live demonstrations, teaching

### 4. Docker Real Environment (~60 seconds)
```bash
cd ids/
python3 workflow_docker_comprehensive.py
```
**What it does**: Full production-like test with real Docker containers
**Best for**: Final validation, realistic testing

---

## 📊 What Gets Detected

All workflows detect these attacks:

### Signature-Based Detection
- ✅ **PORT_SCAN** - Detects nmap-style port scans
- ✅ **SYN_FLOOD** - Detects TCP SYN flooding
- ✅ **ICMP_FLOOD** - Detects ping floods
- ✅ **DNS_TUNNEL** - Detects DNS tunneling via long subdomains + hex encoding
- ✅ **ARP_SPOOF** - Detects ARP cache poisoning (Docker only)

### Anomaly-Based Detection
- ✅ **HIGH_PORT_ENTROPY** - Statistical analysis of port randomness
- ✅ **TRAFFIC_VOLUME_ANOMALY** - Detects unusual traffic spikes
- ✅ **TIMING_ANOMALY** - Detects irregular packet timing patterns

---

## 📈 Expected Results

### Quick Demo (`run_all_demos.py`)
- **Port Scan**: ~10 alerts
- **SYN Flood**: 1 alert
- **ICMP Flood**: 1 alert
- **DNS Tunnel**: 15 alerts
- **Total**: ~27 alerts
- **Time**: 30 seconds

### Synthetic Test (`test_dynamic_ids.py`)
- **Total**: 30-50 alerts (randomized)
- **Generates**: Full HTML report with 6 charts
- **Time**: 10 seconds

### Docker Comprehensive (`workflow_docker_comprehensive.py`)
- **Total**: 60-70 alerts
- **Signature**: 52 alerts (PORT_SCAN, SYN_FLOOD, ICMP_FLOOD, DNS_TUNNEL)
- **Anomaly**: 11 alerts (HIGH_PORT_ENTROPY)
- **Generates**: Full HTML report with all detections
- **Time**: 60 seconds

---

## 🎪 Demo Recommendation

For a **live presentation or demo**, do this:

```bash
# Terminal 1: Run quick demo
cd ids/
python3 run_all_demos.py

# Then run Docker comprehensive
python3 workflow_docker_comprehensive.py
```

This shows:
1. **Quick validation** - All detections work (30 sec)
2. **Real environment** - Production-ready testing (60 sec)
3. **Professional report** - Opens in browser automatically

Total demo time: **90 seconds** for full end-to-end demonstration! 🚀

---

## 📂 File Locations

After running any workflow, find these files:

```
ids/
├── outputs/
│   ├── logs/
│   │   ├── alerts.log                     # All detected alerts
│   │   └── evaluation_results.json        # Metrics summary
│   ├── visualizations/                    # 6 charts (PNG)
│   │   ├── alerts_by_type.png
│   │   ├── alerts_timeline.png
│   │   ├── alert_severity_pie.png
│   │   ├── top_source_ips.png
│   │   ├── attack_types_distribution.png
│   │   └── detection_methods_pie.png
│   └── reports/
│       └── ids_report.html                # Full HTML report
└── pcaps/                                 # Generated traffic
    ├── docker_comprehensive_capture.pcap  # Docker workflow
    ├── demo_port_scan.pcap                # Demo PCAPs
    ├── demo_syn_flood.pcap
    ├── demo_icmp_flood.pcap
    └── demo_dns_tunnel.pcap
```

---

## 🛠️ Troubleshooting

### Docker not working?
```bash
cd ..
docker-compose down
docker-compose build
docker-compose up -d
cd ids/
python3 workflow_docker_comprehensive.py
```

### Report not opening?
```bash
open ids/outputs/reports/ids_report.html
```

### Want to see verbose output?
The IDS has a `verbose` flag that can be toggled:
- `verbose = True` - Shows all packet traces (default for full workflows)
- `verbose = False` - Only shows alerts (used in demos)

---

## 🎓 Key Differences

| Feature | Quick Demo | Synthetic | Interactive | Docker |
|---------|-----------|-----------|-------------|--------|
| **Time** | 30 sec | 10 sec | Variable | 60 sec |
| **Alerts** | ~27 | 30-50 | Varies | 60-70 |
| **Report** | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| **Realistic** | Low | Low | Low | **High** |
| **Randomized** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | Quick check | Fast testing | Teaching | Production validation |

---

## 📝 Summary

You now have **4 different ways** to test and demonstrate your IDS:

1. **run_all_demos.py** - Quick validation (30 sec)
2. **test_dynamic_ids.py** - Full synthetic test with report (10 sec)
3. **demo_terminal_attacks.py** - Interactive menu-driven demos
4. **workflow_docker_comprehensive.py** - Realistic Docker environment (60 sec)

### Recommended Flow for Demo/Presentation:
```bash
# 1. Quick validation
python3 run_all_demos.py

# 2. Full realistic test
python3 workflow_docker_comprehensive.py
# Report opens automatically in browser
```

**Total time: 90 seconds** ⚡

Everything is ready to go! 🛡️✨
