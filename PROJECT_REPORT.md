# Network Intrusion Detection System - Project Report

**CSCD58 Computer Security Course Project**  
**Authors:** Muhammad Bilal & Zuhair Khan  
**Institution:** University of Toronto  
**Date:** December 10, 2025

---

## 1. Project Description and Goals

### 1.1 Overview
This project implements a production-grade Network Intrusion Detection System (NIDS) capable of detecting multiple categories of network attacks through a dual detection architecture. The system combines signature-based pattern matching with statistical anomaly detection to achieve comprehensive threat identification.

### 1.2 Primary Goals
1. **Detect Known Attacks**: Implement signature-based detection for common network attacks
2. **Detect Novel Threats**: Use statistical anomaly detection to identify unusual behavior patterns
3. **Zero False Positives**: Maintain high accuracy with no false alarms on legitimate traffic
4. **Real-World Testing**: Deploy in isolated Docker environment with actual penetration testing tools
5. **Professional Reporting**: Generate comprehensive HTML reports with visualizations and metrics

### 1.3 Complete Feature Set

#### A. Signature-Based Detection (5 Attack Types)
- **Port Scan Detection**: Threshold-based tracking of unique ports accessed per source IP (threshold: 10 ports)
- **SYN Flood Detection**: Rate monitoring with SYN/ACK ratio analysis (threshold: 50 packets, ratio < 0.1)
- **ICMP Flood Detection**: Sliding window algorithm tracking packet rates over 5-second intervals (threshold: 50 packets)
- **DNS Tunneling Detection**: Pattern analysis of DNS query lengths and hexadecimal content (min length: 30 chars, hex ratio > 60%)
- **ARP Spoofing Detection**: MAC address tracking with change detection for known IP mappings

#### B. Anomaly-Based Detection (3 Statistical Methods)
- **Shannon Entropy Analysis**: Calculates randomness in destination port distributions; detects high-entropy scans
- **Z-Score Traffic Volume Detection**: Statistical modeling using mean ± 3σ thresholds for traffic spike identification
- **Inter-Arrival Time Analysis**: Detects burst patterns by analyzing packet timing deviations from baseline

#### C. Infrastructure & Testing
- **Docker Environment**: 3-container isolated network (IDS: 10.0.0.10, Attacker: 10.0.0.20, Victim: 10.0.0.30)
- **Real Attack Tools**: nmap, hping3, arpspoof, dig integrated in attacker container
- **Baseline Training**: Statistical profiling on 1,052 normal traffic packets with persistent model storage
- **PCAP Support**: Can analyze live traffic or pre-recorded PCAP files for reproducible testing

#### D. Reporting & Visualization
- **6 Visualization Charts**: Alert distribution, timeline, detection comparison, baseline statistics, entropy analysis, performance metrics
- **HTML Dashboard**: Professional corporate-style report with embedded base64-encoded charts
- **Real-Time Logging**: Console output with severity levels + persistent `alerts.log` file
- **JSON Metrics**: Structured performance data in `evaluation_results.json`

#### E. Testing & Demo Capabilities
- **Interactive Demos**: Menu-driven attack demonstrations (`demo_terminal_attacks.py`)
- **Automated Testing**: Full test suites with randomized attacks (`test_dynamic_ids.py`)
- **Docker Workflows**: Comprehensive attack sequences using real tools (`workflow_docker_comprehensive.py`)
- **Threshold Tuning**: Sensitivity testing script for detection parameter optimization

---

## 2. Team Contributions

### Muhammad Bilal - Infrastructure & Integration (50%)

#### Docker Environment Architecture (High Complexity)
- Designed 3-container network topology with proper isolation and routing
- Created Dockerfiles for IDS, attacker, and victim containers with appropriate capabilities (CAP_NET_RAW, CAP_NET_ADMIN)
- Configured docker-compose.yml with static IP addressing (10.0.0.0/24 network)
- Resolved package repository issues and optimized container build process

#### Attack Suite Implementation (High Complexity)
- Developed `capture_docker_comprehensive.py` orchestrating 8 different attack types
- Integrated real penetration testing tools (nmap, hping3, arpspoof, dig)
- Implemented sophisticated Scapy-based attack scripts for anomaly generation
- Created timing sequences for realistic attack scenarios (200-port scans, 180 ICMP floods, 25 DNS tunnels)

#### Workflow Automation (Medium Complexity)
- Built `workflow_docker_comprehensive.py` for end-to-end testing pipeline
- Implemented tcpdump capture synchronization across containers
- Created PCAP extraction and analysis automation
- Developed cleanup and preparation routines for reproducible testing

#### Documentation & Organization (Medium Complexity)
- Authored comprehensive README.md with quick-start guides
- Created Docker setup documentation and troubleshooting guides
- Organized project structure with clear separation of concerns
- Maintained version control and collaborative development workflow

---

### Zuhair Khan - Detection Algorithms & Analysis (50%)

#### Core IDS Engine (High Complexity)
- Implemented dual detection architecture in `enhanced_ids.py` (529 lines)
- Developed signature-based detection algorithms for 5 attack types with stateful tracking
- Created anomaly detection engine with statistical baseline modeling
- Designed configurable threshold system for easy tuning and testing

#### Statistical Analysis Framework (High Complexity)
- Implemented Shannon entropy calculations for port distribution analysis
- Developed Z-score anomaly detection with mean/standard deviation modeling
- Created inter-arrival time analysis for burst detection
- Built baseline training system with model persistence (pickle serialization)

#### Reporting & Visualization System (Medium Complexity)
- Developed `generate_report.py` creating professional HTML dashboards (746 lines)
- Implemented `create_dynamic_visualizations.py` generating 6 chart types using matplotlib
- Created base64 image embedding for standalone HTML reports
- Designed metrics collection and JSON serialization system

#### Testing & Validation (Medium Complexity)
- Built `test_dynamic_ids.py` for randomized attack generation and validation
- Created `demo_terminal_attacks.py` for interactive demonstrations
- Developed `test_threshold_sensitivity.py` for detection parameter optimization
- Implemented evaluation metrics calculation (detection rates, throughput, false positives)

#### Demo Scripts & Presentation Tools (Medium Complexity)
- Created `run_all_demos.py` for automated 4-attack demonstrations
- Built `demo_presentation.sh` for live presentation scenarios
- Developed synthetic traffic generators for each attack type
- Implemented verbose/quiet modes for different use cases

---

## 3. Running & Testing Instructions

### 3.1 Prerequisites
```bash
# Python 3.8+ with dependencies
pip3 install scapy matplotlib numpy pandas

# Docker Desktop (for Docker workflows)
docker --version
docker-compose --version
```

### 3.2 Quick Start Options

#### Option A: Interactive Demo (No Docker - 30 seconds)
```bash
cd ids/
python3 demo_terminal_attacks.py
# Choose attacks from menu (1-4) or run all (5)
```

#### Option B: Automated Demo (No Docker - 30 seconds)
```bash
cd ids/
python3 run_all_demos.py
# Executes all 4 attacks automatically with detection
```

#### Option C: Fast Synthetic Testing (No Docker - 10 seconds)
```bash
cd ids/
python3 test_dynamic_ids.py
# Generates randomized attacks, detects, creates HTML report
```

#### Option D: Comprehensive Docker Testing (Recommended - 60 seconds)
```bash
# Step 1: Create Docker network (one-time setup)
docker network create --subnet=10.0.0.0/24 ids-net

# Step 2: Start containers
docker compose up -d

# Step 3: Verify containers running
docker compose ps

# Step 4: Run comprehensive workflow
cd ids/
python3 workflow_docker_comprehensive.py

# This will:
# - Execute 8 attack types using real tools
# - Capture traffic with tcpdump
# - Analyze with IDS (dual detection)
# - Generate 6 visualizations
# - Create HTML report
# - Auto-open report in browser
```

### 3.3 Viewing Results
```bash
# HTML report (opens in browser)
open ids/outputs/reports/ids_report.html

# Alert log (all detections)
cat ids/outputs/logs/alerts.log

# Performance metrics (JSON)
cat ids/outputs/logs/evaluation_results.json

# Visualizations (6 PNG files)
ls ids/outputs/visualizations/
```

### 3.4 Testing Specific Features

#### Test Port Scan Detection
```bash
cd ids/
python3 - <<'EOF'
from scapy.all import *
from enhanced_ids import EnhancedIDS

# Generate port scan
packets = [IP(src="192.168.1.50", dst="192.168.1.100")/TCP(dport=p, flags="S") 
           for p in range(1, 101)]

# Analyze with IDS
ids = EnhancedIDS(use_anomaly_detection=False)
for pkt in packets:
    ids.packet_handler(pkt)

print(f"Alerts: {len(ids.alerts)}")
EOF
```

#### Test Anomaly Detection
```bash
cd ids/
python3 test_threshold_sensitivity.py
# Tests various detection thresholds and shows results
```

#### Test Docker Attacks Individually
```bash
# Port scan only
docker exec attacker nmap -p 1-100 10.0.0.30

# SYN flood only
docker exec attacker hping3 -S -p 80 --flood --rand-source 10.0.0.30

# View IDS logs in real-time
docker compose logs -f ids
```

### 3.5 Cleanup
```bash
# Stop and remove containers
docker compose down --volumes --remove-orphans

# Remove generated files
rm -rf ids/outputs/
rm -f ids/baseline_model.pkl
rm -f pcaps/*.pcap
```

---

## 4. Implementation Details

### 4.1 Core Detection Engine Architecture

#### Packet Processing Pipeline
```
Packet → Protocol Parsing → Signature Detection → Anomaly Detection → Alert Generation
         (Scapy)            (Pattern Matching)   (Statistical)     (Logging)
```

#### Key Data Structures
```python
# Signature-based tracking
port_scan_tracker: dict[src_ip → set(ports)]
syn_tracker: dict[src_ip → count]
icmp_tracker: dict[src_ip → [timestamps]]
arp_table: dict[ip → mac]

# Anomaly-based tracking
window_packets: list[packet_data]
dst_ports_window: list[ports]
baseline: dict[metric → {mean, std}]
```

#### Detection Algorithms

**Port Scan Detection**
```python
if len(unique_ports_per_source) > THRESHOLD:
    alert("PORT_SCAN", severity="HIGH")
```

**SYN Flood Detection**
```python
if syn_count > THRESHOLD and syn_ack_ratio < RATIO_THRESHOLD:
    alert("SYN_FLOOD", severity="CRITICAL")
```

**Entropy-Based Anomaly**
```python
entropy = -Σ(p_i * log2(p_i))  # Shannon entropy
if entropy > baseline_entropy * MULTIPLIER:
    alert("ENTROPY_ANOMALY", severity="MEDIUM")
```

**Z-Score Anomaly**
```python
z = |value - mean| / std
if z > 3.0:  # 3-sigma threshold
    alert("VOLUME_ANOMALY", severity="MEDIUM")
```

### 4.2 Docker Network Architecture

```
ids-net Bridge (10.0.0.0/24)
├── IDS Container
│   ├── IP: 10.0.0.10
│   ├── Capabilities: NET_RAW, NET_ADMIN
│   ├── Runs: tcpdump, enhanced_ids.py
│   └── Sniffs: all traffic on bridge
├── Attacker Container  
│   ├── IP: 10.0.0.20
│   ├── Tools: nmap, hping3, arpspoof, scapy
│   └── Generates: malicious traffic
└── Victim Container
    ├── IP: 10.0.0.30
    ├── Runs: tcpdump for capture
    └── Receives: attack traffic
```

### 4.3 Baseline Training Process

```python
# 1. Load normal traffic PCAP
packets = rdpcap("normal_traffic.pcap")

# 2. Extract features
packet_rates, byte_rates, ports, inter_arrival_times = extract_features(packets)

# 3. Calculate statistics
baseline = {
    'packet_rate': {'mean': μ, 'std': σ},
    'port_entropy': H(ports),
    'inter_arrival': {'mean': μ_iat, 'std': σ_iat}
}

# 4. Save model
pickle.dump(baseline, open('baseline_model.pkl', 'wb'))
```

### 4.4 Report Generation Pipeline

```
Alerts Log → Parse Alerts → Count by Type → Generate Charts → Embed in HTML → Open Browser
             ↓
Metrics JSON → Calculate Stats → Format Tables → 
```

Charts generated using matplotlib:
- Pie charts for distribution
- Bar charts for comparisons  
- Line charts for timelines
- Heatmaps for correlation analysis

---

## 5. Analysis & Discussion

### 5.1 Detection Performance Results

#### Comprehensive Test Results (Docker Workflow)
| Metric | Value |
|--------|-------|
| Total Packets Processed | 500-700 |
| Total Alerts Generated | 60-70 |
| Signature-Based Alerts | 52 |
| Anomaly-Based Alerts | 11 |
| Detection Rate | 100% |
| False Positive Rate | 0% |
| Processing Throughput | 3,000-21,000 pkt/s |
| Test Duration | ~60 seconds |

#### Attack-Specific Detection Rates
| Attack Type | Packets | Alerts | Detection Rate |
|-------------|---------|--------|----------------|
| Port Scan (200 ports) | 200+ | 35+ | 100% |
| SYN Flood | 100+ | 1-2 | 100% |
| ICMP Flood | 180 | 1 | 100% |
| DNS Tunneling | 25 | 15 | 100% |
| ARP Spoofing | 8 | 8 | 100% |
| High Entropy Scan | 150 | 11 | 100% |
| Normal Traffic | 50 | 0 | 0% FP |

### 5.2 Algorithm Effectiveness

#### Signature-Based Detection
**Strengths:**
- Fast, deterministic identification of known attacks
- Low computational overhead (simple threshold checks)
- Zero false positives on well-tuned thresholds
- Easy to understand and explain detection logic

**Limitations:**
- Cannot detect novel attacks not in signature database
- Susceptible to evasion through minor protocol variations
- Requires manual threshold tuning per network environment

#### Anomaly-Based Detection
**Strengths:**
- Detects zero-day attacks and novel attack patterns
- Adapts to network baseline through statistical learning
- Identifies subtle deviations (e.g., high-entropy scans)
- No need for prior attack knowledge

**Limitations:**
- Requires training period on clean traffic
- Higher computational cost (entropy, z-score calculations)
- Potential for false positives if baseline is polluted
- Less interpretable than signature-based alerts

### 5.3 Docker vs. Synthetic Testing Comparison

| Aspect | Docker Workflow | Synthetic (Scapy) |
|--------|----------------|-------------------|
| Realism | High (real tools) | Medium (simulated) |
| Reproducibility | Medium (timing varies) | High (deterministic) |
| Setup Time | ~10 min (first run) | ~30 sec |
| Test Duration | ~60 sec | ~10 sec |
| Tool Coverage | nmap, hping3, arpspoof | Scapy-generated |
| Network Isolation | Full (containers) | None (host) |
| Debugging | Harder (multi-container) | Easier (single process) |
| Best Use Case | Demos, final validation | Development, tuning |

**Recommendation:** Use synthetic testing during development for rapid iteration, then validate with Docker workflow before deployment.

### 5.4 Threshold Tuning Analysis

Testing revealed optimal thresholds balance sensitivity vs. false positives:

| Threshold | Too Low | Optimal | Too High |
|-----------|---------|---------|----------|
| Port Scan | FP on legit apps | 10 ports | Miss slow scans |
| SYN Flood | FP on web servers | 50 pkts | Miss small attacks |
| ICMP Flood | FP on ping tests | 50/5s | Miss distributed floods |
| Z-Score | FP on traffic spikes | 3.0σ | Miss subtle anomalies |

**Key Insight:** Thresholds must be tuned to specific network environments. Our defaults work well for lab/test networks but may need adjustment for production deployment.

### 5.5 Performance Bottlenecks

Profiling identified key performance factors:

1. **Packet Capture:** Scapy sniffing is fast enough for lab traffic (<1000 pkt/s) but may struggle with 10Gbps networks
2. **Entropy Calculation:** O(n log n) complexity for large port sets; optimized with 10-second sliding windows
3. **Report Generation:** Base64 encoding of charts adds ~500ms; negligible compared to attack duration
4. **Docker Overhead:** Container networking adds ~5-10ms latency; acceptable for IDS use case

**Optimization Opportunities:**
- Use libpcap directly instead of Scapy for higher throughput
- Implement parallel packet processing with multiprocessing
- Cache baseline statistics to avoid repeated calculations
- Stream alerts to external SIEM instead of local files

### 5.6 Real-World Deployment Considerations

**Security Hardening:**
- Run IDS container as non-root user with minimal capabilities
- Implement alert rate limiting to prevent alert flooding
- Encrypt alert logs and use secure syslog transport
- Add authentication for HTML report access

**Scalability:**
- Distribute packet capture across multiple IDS instances
- Use message queue (Kafka/RabbitMQ) for alert aggregation
- Implement database backend for alert storage
- Add REST API for programmatic access

**Integration:**
- Export alerts in SIEM-compatible formats (CEF, Syslog)
- Add webhook notifications for critical alerts
- Integrate with firewall for automatic blocking
- Support PCAP export for forensic analysis

---

## 6. Conclusions & Lessons Learned

### 6.1 Project Achievements

This project successfully demonstrates a production-capable intrusion detection system with the following accomplishments:

1. **Comprehensive Detection:** Implemented 5 signature-based and 3 anomaly-based detection methods covering major attack categories
2. **Perfect Accuracy:** Achieved 100% detection rate with 0% false positives across all test scenarios
3. **Real-World Validation:** Tested with actual penetration testing tools (nmap, hping3) in isolated Docker environment
4. **Professional Reporting:** Created industry-standard HTML reports with embedded visualizations and detailed metrics
5. **Reproducible Testing:** Developed automated workflows enabling consistent evaluation and demonstration

### 6.2 Technical Lessons Learned

#### Network Security
- **Defense in Depth:** Single detection method insufficient; dual approach (signature + anomaly) provides comprehensive coverage
- **Baseline Importance:** Accurate normal traffic modeling crucial for anomaly detection effectiveness
- **Threshold Tuning:** No one-size-fits-all; thresholds must be adjusted per network environment
- **Attack Diversity:** Real attacks vary significantly; testing must include multiple tools and techniques

#### Software Engineering
- **Containerization Benefits:** Docker isolation enables safe attack testing without compromising host systems
- **Modular Design:** Separation of detection, reporting, and testing components enables independent development and testing
- **Configuration Management:** Exposing thresholds as constants enables easy tuning without code changes
- **Automated Testing:** Reproducible test workflows essential for validation and regression testing

#### Data Science & Statistics
- **Feature Selection:** Port entropy and inter-arrival times proved most effective anomaly indicators
- **Statistical Methods:** Z-score (3σ) provided good balance between sensitivity and false positives
- **Training Data Quality:** Clean baseline traffic critical; even small amounts of attack traffic pollute baseline
- **Visualization Value:** Charts communicate results more effectively than raw numbers for stakeholders

### 6.3 Challenges Overcome

1. **Docker Package Repositories:** Ubuntu/Kali mirrors had hash mismatches during development; resolved by switching to Python slim base images and minimal package installations

2. **Network Capture Synchronization:** tcpdump timing in containers required careful orchestration; implemented delays and background process management

3. **PCAP Timestamp Handling:** Scapy Decimal timestamps caused serialization errors; resolved with explicit float conversion throughout codebase

4. **Report Size Optimization:** Initial HTML reports exceeded 10MB with full-size charts; implemented aggressive image compression and base64 embedding

5. **Cross-Container Communication:** Packet visibility between containers required proper network configuration and capabilities (CAP_NET_RAW)

### 6.4 Future Enhancements

**Short-Term (1-2 weeks):**
- Add HTTP/HTTPS protocol analysis for application-layer attacks
- Implement machine learning classifier (Random Forest) for anomaly scoring
- Create Grafana dashboard for real-time monitoring
- Add IPv6 support for dual-stack networks

**Medium-Term (1-2 months):**
- Deploy on cloud infrastructure (AWS VPC, Azure VNet)
- Implement distributed IDS across multiple network segments
- Add deep packet inspection (DPI) for payload analysis
- Create mobile app for alert notifications

**Long-Term (3+ months):**
- Integrate threat intelligence feeds (STIX/TAXII)
- Implement behavioral analysis with LSTM neural networks
- Add automated response capabilities (firewall rule updates)
- Achieve 10Gbps wire-speed processing with DPDK

### 6.5 Key Takeaways

**For Network Security Practitioners:**
- Dual detection architecture (signature + anomaly) provides comprehensive threat coverage
- Statistical baseline training requires clean traffic; continuous retraining recommended
- Threshold tuning is environment-specific; use sensitivity testing to optimize
- PCAP-based testing provides reproducible evaluation superior to live testing

**For Software Developers:**
- Docker containerization enables safe security testing without host compromise
- Automated testing workflows essential for complex multi-component systems
- Visualization and reporting as important as core functionality for user adoption
- Configuration flexibility (exposed thresholds) enables real-world deployment

**For Data Scientists:**
- Domain knowledge (networking) crucial for feature engineering
- Simple statistical methods (z-score, entropy) often outperform complex ML for interpretability
- Training data quality more important than algorithm sophistication
- Real-time constraints require algorithm optimization (O(1) vs O(n²))

### 6.6 Course Relevance

This project directly applies CSCD58 course concepts:

- **Network Security Fundamentals:** Protocol analysis (TCP/IP, ARP, DNS, ICMP)
- **Attack Taxonomy:** Port scanning, flooding, spoofing, tunneling
- **Detection Methods:** Signature-based vs. anomaly-based trade-offs
- **Defense Mechanisms:** Intrusion detection as preventive security control
- **Threat Modeling:** Understanding attacker techniques and detection strategies
- **Security Metrics:** False positive/negative rates, detection accuracy

The hands-on implementation reinforced theoretical knowledge and provided practical experience with real-world security tools and techniques.

---

## Appendix: Quick Reference

### Command Cheat Sheet
```bash
# Quick demo
cd ids/ && python3 run_all_demos.py

# Full Docker test
docker network create --subnet=10.0.0.0/24 ids-net
docker compose up -d
cd ids/ && python3 workflow_docker_comprehensive.py

# View results
open ids/outputs/reports/ids_report.html
cat ids/outputs/logs/alerts.log

# Cleanup
docker compose down --volumes --remove-orphans
rm -rf ids/outputs/
```

### File Organization
```
Key Files:
- ids/enhanced_ids.py          # Core IDS (529 lines)
- ids/workflow_docker_comprehensive.py  # Full test workflow
- ids/generate_report.py       # HTML report generator
- docker-compose.yml           # Container orchestration
- pcaps/                       # Traffic captures
- ids/outputs/                 # All generated files
```

### Performance Benchmarks
- **Throughput:** 3,000-21,000 packets/second
- **Detection Latency:** <100ms per packet
- **Memory Usage:** ~50MB baseline, ~200MB with visualizations
- **Disk Usage:** ~5MB reports, ~10MB PCAPs per test

---

**End of Report**
