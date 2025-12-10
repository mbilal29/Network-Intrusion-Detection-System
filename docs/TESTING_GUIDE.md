# IDS Testing Guide

## 🎯 Two Testing Workflows

### Workflow 1: Python-Based (Fast)
**Best for:** Quick testing, development, debugging  
**Time:** 10-20 seconds

```bash
cd ids/
python3 run_complete_test.py
```

**What it does:**
1. Generates randomized attacks with Scapy
2. Tests IDS with dual detection
3. Creates 6 visualization charts
4. Generates HTML report
5. Opens report in browser

**Randomization:**
- Port scans: Low/medium/high intensity (10-100 ports)
- SYN floods: Short/medium/long duration (50-300 packets)
- ARP spoofs: 3-10 spoofed packets
- Every run produces different results!

---

### Workflow 2: Docker-Based (Realistic)
**Best for:** Demonstrations, realistic network simulation  
**Time:** 30-45 seconds

```bash
# Start Docker containers
docker-compose up -d

# Run complete workflow
cd ids/
python3 run_docker_workflow.py
```

**What it does:**
1. Verifies Docker containers are running
2. Executes **REAL** attack tools inside Docker:
   - `nmap` for port scanning
   - `hping3` for SYN flooding
   - `arping` for ARP activity
3. Generates corresponding PCAPs with Scapy
4. Analyzes with IDS
5. Creates visualizations and HTML report
6. Opens report in browser

**Docker Network:**
```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Attacker   │──────▶│     IDS      │──────▶│    Victim    │
│  10.0.0.20   │       │  10.0.0.10   │       │  10.0.0.30   │
│ (nmap,hping3)│       │  (Python)    │       │  (target)    │
└──────────────┘       └──────────────┘       └──────────────┘
```

---

## 📊 Output Files

Both workflows generate organized outputs:

```
ids/outputs/
├── visualizations/
│   ├── alert_distribution.png        # Alert types pie chart
│   ├── severity_distribution.png     # Severity levels
│   ├── detection_summary.png         # Detection stats
│   ├── attack_timeline.png           # Temporal analysis
│   ├── baseline_statistics.png       # Normal traffic baseline
│   └── performance_metrics.png       # Throughput graphs
├── reports/
│   └── ids_report.html               # Comprehensive HTML report
└── logs/
    ├── alerts.log                     # All detected alerts
    └── evaluation_results.json        # Performance metrics
```

---

## 🔧 Troubleshooting

### Python Workflow

**Problem:** "No module named 'scapy'"  
**Solution:**
```bash
pip3 install scapy matplotlib numpy
```

**Problem:** No visualizations generated  
**Solution:** Check that `outputs/logs/alerts.log` exists and has content

---

### Docker Workflow

**Problem:** "Missing containers: ids, attacker, victim"  
**Solution:**
```bash
docker-compose up -d
```

**Problem:** "Cannot connect to Docker daemon"  
**Solution:** Start Docker Desktop application

**Problem:** Docker containers not found  
**Solution:** Verify containers are running:
```bash
docker ps
# Should show: ids, attacker, victim
```

---

## 📈 Expected Results

### Typical Test Run
- **Total Packets:** 400-600
- **Total Alerts:** 25-35
- **Port Scan Alerts:** 8-12
- **SYN Flood Alerts:** 1-2
- **ARP Spoof Alerts:** 15-20
- **False Positives:** 0

### Alert Examples
```
[2025-12-04 19:57:50] [HIGH] PORT_SCAN: 10.0.0.20 scanned 11 ports
[2025-12-04 19:57:50] [CRITICAL] SYN_FLOOD: 10.0.0.20 sent 51 SYNs (ratio: 0.08)
[2025-12-04 19:57:50] [HIGH] ARP_SPOOF: IP 10.0.0.30 MAC changed: aa:bb:cc → 11:22:33
[2025-12-04 19:57:50] [MEDIUM] HIGH_PORT_ENTROPY: Port entropy: 5.90 (baseline: 3.93)
```

---

## 🎯 Comparison

| Feature | Python Workflow | Docker Workflow |
|---------|----------------|-----------------|
| **Speed** | ⚡ Fast (10-20s) | 🐢 Slower (30-45s) |
| **Setup** | ✅ None | 🐳 Docker required |
| **Attacks** | Scapy-generated | Real tools (nmap, hping3) |
| **Network** | Simulated | Isolated containers |
| **Realism** | Medium | High |
| **Best For** | Development | Demonstrations |

---

## 💡 Tips

1. **For quick testing:** Use Python workflow
2. **For demonstrations:** Use Docker workflow to showcase real attack tools
3. **Check reports:** All reports auto-open in browser
4. **View metrics:** Check `outputs/logs/evaluation_results.json` for detailed stats
5. **Clean outputs:** Delete `outputs/` folder to start fresh
