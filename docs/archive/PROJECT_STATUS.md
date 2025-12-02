# ⚠️ ARCHIVED DOCUMENT - Development History Only

**This document is kept for project history and is NOT part of the core submission.**  
**For evaluation, refer to: `FINAL_REPORT.md`, `SUBMISSION_CHECKLIST.md`**

---

# Project Status & Division of Work

## ✅ What's Already Done (Bilal)

### Infrastructure Complete
- ✅ Docker network created (`ids-net`)
- ✅ Three containers configured:
  - IDS (Python 3.10 + Scapy + PyShark)
  - Attacker (Kali Linux + nmap + hping3)
  - Victim (Ubuntu)
- ✅ docker-compose.yml configured
- ✅ All Dockerfiles working
- ✅ README with setup instructions
- ✅ Basic folder structure

### What Works Right Now
- Containers can communicate (ping)
- Network is isolated and safe
- All attack tools installed on Kali
- Python environment ready for IDS code

---

## 🚧 What's Left to Build (7 days)

### Day 1-2: Core Sniffer & Data Collection (ZUHAIR - YOU)
**Status: STARTED**

**Your Tasks:**
1. ✅ Create working `sniffer.py` (DONE - just created)
2. ⬜ Test sniffer with real traffic
3. ⬜ Extract packet fields into structured data
4. ⬜ Create flow tracking (group packets by src/dst)
5. ⬜ Build logging framework (`alerts.log`, `traffic.csv`)

**Deliverables:**
- Working packet capture system
- Data structures for tracking:
  - Per-host statistics
  - TCP connection states
  - ARP mappings
  - Flow-level features

---

### Day 2-3: Signature-Based Detection (BOTH - Split)

**BILAL Could Do:**
- Port scan detection
  - Track SYN packets to many ports
  - Detect rapid connection attempts
  - Half-open TCP detection

**ZUHAIR (YOU) Could Do:**
- SYN flood detection
  - Count SYN rate per source
  - SYN/ACK ratio monitoring
  - Time-window based thresholds
- ARP spoofing detection
  - MAC-IP mapping conflicts
  - Unsolicited ARP replies
  - Rapid ARP changes

---

### Day 4-5: Anomaly-Based Detection (ZUHAIR - YOU)

**Your Focus:**
1. ⬜ Extract flow-level features:
   - Packets/sec, bytes/sec
   - Unique ports per host
   - Entropy calculations (port distribution)
   - Inter-arrival times
2. ⬜ Implement statistical detection:
   - Z-score thresholds
   - Moving averages
   - Baseline vs. current behavior
3. ⬜ Create anomaly scoring system

---

### Day 6: Evaluation & Testing (BOTH)

**Tasks:**
- ⬜ Run controlled attack scenarios
- ⬜ Measure detection performance:
  - True positives
  - False positives
  - Detection latency
- ⬜ Test under different traffic loads
- ⬜ Document results

---

### Day 7: Visualization & Final Report (BOTH)

**BILAL Could Do:**
- Create graphs with matplotlib:
  - Traffic volume over time
  - Attack timelines
  - Detection accuracy charts
- Screenshots for report

**ZUHAIR (YOU) Could Do:**
- Write final report sections:
  - Methodology
  - Detection algorithms explanation
  - Results & analysis
- Prepare demo video script

---

## 🎯 Your Immediate Next Steps (TODAY)

### 1. Test the Environment (15 minutes)

```bash
# Create Docker network (if not exists)
docker network create --subnet=10.0.0.0/24 ids-net

# Build and start everything
docker-compose up --build
```

Open 3 terminals:
```bash
# Terminal 1 - IDS
docker exec -it ids bash
cd /app
python3 sniffer.py

# Terminal 2 - Attacker
docker exec -it attacker bash
ping 10.0.0.30

# Terminal 3 - Victim
docker exec -it victim bash
```

### 2. Verify Sniffer Works (5 minutes)

From attacker, run:
```bash
ping 10.0.0.30
```

You should see ICMP packets in the IDS terminal ✅

### 3. Test First Attack (10 minutes)

From attacker:
```bash
nmap -sS 10.0.0.30
```

Watch the IDS terminal fill with TCP SYN packets ✅

---

## 📋 Recommended Division of Labor

### Zuhair (YOU) - Focus Areas:
1. **Core IDS Engine**
   - Packet processing pipeline
   - Flow tracking and statistics
   - Logging system
2. **Anomaly Detection**
   - Statistical models
   - Entropy calculations
   - Behavioral analysis
3. **SYN Flood + ARP Spoof Detection**
4. **Report Writing** (methodology, algorithms)

### Bilal - Focus Areas:
1. **Port Scan Detection**
   - Signature rules
   - Pattern matching
2. **Attack Scripts**
   - Create controlled test scenarios
   - Automate attack generation
3. **Visualization**
   - Graphs with matplotlib
   - Demo video preparation
4. **Environment Maintenance**
   - Docker troubleshooting
   - Documentation updates

---

## 📁 File Structure You'll Create

```
Network-Intrusion-Detection-System/
├── ids/
│   ├── __init__.py
│   ├── sniffer.py          ✅ DONE
│   ├── detection_engine.py ⬜ YOU - NEXT
│   ├── flow_tracker.py     ⬜ YOU
│   ├── anomaly_detector.py ⬜ YOU
│   ├── logger.py           ⬜ YOU
│   └── utils.py            ⬜ SHARED
├── attacks/
│   ├── port_scan.sh        ⬜ BILAL
│   ├── syn_flood.sh        ⬜ BILAL
│   └── arp_spoof.py        ⬜ BILAL
├── evaluation/
│   ├── analysis.py         ⬜ BILAL
│   ├── graphs.py           ⬜ BILAL
│   └── results.md          ⬜ BOTH
├── logs/
│   ├── alerts.log
│   └── traffic.csv
└── docs/
    ├── ARCHITECTURE.md     ⬜ YOU
    └── FINAL_REPORT.md     ⬜ BOTH
```

---

## 🚀 Communication with Bilal

### Share This Document
Send Bilal this file so he knows:
- What you're working on
- What he should focus on
- How to avoid duplicate work

### GitHub Workflow
```bash
# Create feature branches
git checkout -b feature/anomaly-detection   # For you
git checkout -b feature/port-scan           # For Bilal

# Regular commits
git add .
git commit -m "Add flow tracking logic"
git push origin feature/anomaly-detection

# Merge when ready
```

---

## 📞 Questions to Ask Bilal

1. "Should I focus on anomaly detection while you do port scan signatures?"
2. "Can you handle the attack scripts while I build the detection engine?"
3. "Who wants to do the visualization/graphing?"
4. "Let's sync up after Day 3 to integrate our code"

---

## ⚡ Quick Wins for Today

If environment works, you can immediately:
1. ✅ Commit the working sniffer.py
2. ⬜ Create `detection_engine.py` skeleton
3. ⬜ Start building flow tracker
4. ⬜ Test SYN flood detection logic

**Goal:** By end of today, you should have:
- ✅ Working sniffer that shows all traffic
- ✅ Basic structure for detection engine
- ✅ Clear plan with Bilal on who does what

---

## 🎓 Learning Resources

While coding, refer to:
- **Scapy docs**: https://scapy.readthedocs.io/
- **Packet fields**: IP.src, IP.dst, TCP.sport, TCP.dport, TCP.flags
- **TCP flags**: S (SYN), A (ACK), F (FIN), R (RST), P (PSH)
- **ARP operations**: op=1 (request), op=2 (reply)

---

**Created by: Zuhair**
**Next update: After Day 2**
