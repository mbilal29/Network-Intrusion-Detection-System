# IDS Testing Workflows Guide

This project has **3 distinct testing workflows**, each serving a different purpose.

---

## 📁 File Organization

### Workflow Files (Main Entry Points)

1. **`workflow_fast_synthetic.py`** - Fast Python testing with synthetic attacks
2. **`workflow_docker_basic.py`** - Basic Docker with real nmap + synthetic PCAPs  
3. **`workflow_docker_comprehensive.py`** - Full Docker with real attacks + anomaly detection

### Supporting Files

- **`test_dynamic_ids.py`** - Generates synthetic attacks for fast workflow
- **`capture_docker_comprehensive.py`** - Captures real Docker traffic (comprehensive attacks)
- **`create_dynamic_visualizations.py`** - Generates 6 visualization charts
- **`generate_report.py`** - Creates HTML report with embedded charts
- **`enhanced_ids.py`** - Core IDS engine (dual detection)
- **`baseline_model.pkl`** - Pre-trained anomaly detection baseline

---

## 🚀 Workflow Descriptions

### Workflow 1: Fast Synthetic Testing
**File:** `workflow_fast_synthetic.py`  
**Time:** 10-20 seconds  
**Best for:** Quick testing, development, debugging

```bash
python3 workflow_fast_synthetic.py
```

**What it does:**
- Generates randomized synthetic attacks using Scapy
- Tests IDS with dual detection (signature + anomaly)
- Creates 6 visualization charts
- Generates HTML report
- Auto-opens report in browser

**Randomization:**
- Port scans: 10-100 ports (low/medium/high intensity)
- SYN floods: 50-300 packets (short/medium/long)
- ARP spoofs: 3-10 spoofed packets
- Every run produces different results

**Use when:**
- You want quick feedback
- Testing IDS logic changes
- Don't need Docker overhead

---

### Workflow 2: Docker Basic (Real Tools)
**File:** `workflow_docker_basic.py`  
**Time:** 30-45 seconds  
**Best for:** Demonstrations showing real attack tools

```bash
# Start Docker first
docker-compose up -d

# Run workflow
python3 workflow_docker_basic.py
```

**What it does:**
- Executes **real** nmap inside Docker attacker container
- Generates corresponding Scapy PCAPs for analysis
- Hybrid approach: real tools + analyzable traffic
- Creates visualizations and HTML report
- Auto-opens report in browser

**Docker Network:**
```
Attacker (10.0.0.20) → IDS (10.0.0.10) → Victim (10.0.0.30)
```

**Use when:**
- Demonstrating to prof/TA that real tools execute
- Want Docker isolation
- Don't need maximum realism

---

### Workflow 3: Docker Comprehensive (Real Capture + Anomaly)
**File:** `workflow_docker_comprehensive.py`  
**Time:** 40-60 seconds  
**Best for:** Full testing with signature + anomaly attacks

```bash
# Start Docker first
docker-compose up -d

# Run workflow
python3 workflow_docker_comprehensive.py
```

**What it does:**
1. **Captures ACTUAL traffic** with tcpdump in victim container
2. **Executes comprehensive attacks:**
   - **Phase 1 (Signature):** nmap port scan, SYN scan, ARP activity
   - **Phase 2 (Anomaly):** High entropy, distributed ports, volume spikes
   - **Phase 3 (Timing):** Burst-pause-burst patterns
3. **Copies real PCAP** from container to host
4. **Analyzes with IDS** (both signature + anomaly detection)
5. **Generates full report** with visualizations

**Attack Sophistication:**
- Traditional attacks (nmap, arping)
- High port entropy attacks (random ports = high entropy)
- Traffic volume spikes (200 packets in burst)
- Timing anomalies (irregular burst patterns)
- All captured as REAL traffic from Docker network

**Use when:**
- Final testing before submission
- Want to showcase BOTH signature AND anomaly detection
- Need actual Docker traffic capture
- Testing IDS against sophisticated attacks

---

## 📊 Output Files (All Workflows)

Every workflow generates:

```
ids/outputs/
├── visualizations/
│   ├── alert_distribution.png
│   ├── severity_distribution.png
│   ├── detection_summary.png
│   ├── attack_timeline.png
│   ├── baseline_statistics.png
│   └── performance_metrics.png
├── reports/
│   └── ids_report.html
└── logs/
    ├── alerts.log
    └── evaluation_results.json
```

---

## 🎯 Quick Comparison

| Feature | Fast Synthetic | Docker Basic | Docker Comprehensive |
|---------|---------------|--------------|---------------------|
| **Speed** | ⚡ 10-20s | 🐢 30-45s | 🐌 40-60s |
| **Setup** | None | Docker | Docker |
| **Attacks** | Scapy synthetic | Real nmap + synthetic | Real capture: nmap, Scapy, arping |
| **Traffic** | Simulated | Hybrid | 100% real captured |
| **Anomaly Tests** | ✅ Yes | ❌ No | ✅ Yes (advanced) |
| **Signature Tests** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | Development | Demos | Final testing |

---

## 💡 Recommendations

### For Quick Testing:
```bash
python3 workflow_fast_synthetic.py
```

### For Demonstrations:
```bash
docker-compose up -d
python3 workflow_docker_basic.py
```

### For Comprehensive Evaluation:
```bash
docker-compose up -d
python3 workflow_docker_comprehensive.py
```

### For Prof/TA Demo:
Show **Workflow 3** - proves your IDS detects both signature-based AND anomaly-based attacks using REAL captured Docker traffic!

---

## 🔧 Troubleshooting

**Problem:** Docker containers not running  
**Solution:** `docker-compose up -d`

**Problem:** "No module named 'scapy'"  
**Solution:** `pip3 install scapy matplotlib numpy`

**Problem:** Report doesn't open  
**Solution:** Check `outputs/reports/ids_report.html` manually

---

## 📝 For Your Report/Documentation

When explaining your testing methodology:

1. **Fast Synthetic** - Used during development for rapid iteration
2. **Docker Basic** - Demonstrates real attack tools in isolated environment
3. **Docker Comprehensive** - Full validation with real captured traffic and advanced anomaly detection

This shows you've tested thoroughly at multiple levels of realism!
