# Network Intrusion Detection System - Demo Script
## 5-10 Minute Video Recording Guide

**Authors:** Bilal & Zuhair  
**Course:** CSCD58 - Computer Security  
**Date:** December 2025

---

## 📋 Demo Overview

**Total Time:** 8-10 minutes  
**Format:** Screen recording with narration  
**Goal:** Demonstrate dual-detection IDS with real attacks and professional reporting

---

## 🎬 OPENING: Demo Overview (30 seconds)

### Screen: Show terminal with project folder open

**Script:**
> "Hello! I'm [Name] and today I'll be demonstrating our Network Intrusion Detection System built for CSCD58. In the next 10 minutes, I'll show you:"

### Screen: Show bullet points on screen or README

**Script (point to each as you mention):**
> "First, the architecture and core detection engine that implements both signature-based and anomaly-based detection.
>
> Second, three different testing modes: an interactive menu for live demos, automated testing with synthetic traffic, and comprehensive Docker-based testing with real attack tools like nmap and hping3.
>
> Third, we'll compare the dynamically generated reports from different test types to show how the system adapts to different attack patterns.
>
> And finally, I'll demonstrate live threshold customization - changing detection sensitivity and immediately seeing the results in a regenerated report.
>
> Let's get started!"

---

## 🎬 PART 1: Introduction & Project Overview (1 minute)

### Screen: Show README.md in editor

**Script:**
> "Our Network Intrusion Detection System is a production-ready IDS that combines signature-based and anomaly-based detection to identify various network attacks with 100% accuracy and zero false positives."

### Screen: Scroll through project structure

**Script:**
> "The system is built with Python and Docker. The core detection engine is in enhanced_ids.py, and we have comprehensive Docker integration for realistic testing."

### Screen: Show architecture diagram in README

**Script:**
> "The architecture flows packets through our dual detector - signature rules catch known attacks like port scans and SYN floods, while anomaly detection uses statistical methods to identify unusual behavior that deviates from baseline traffic patterns."

---

## 🎬 PART 2: Core Detection Engine (2 minutes)

### Screen: Open `enhanced_ids.py` in editor

**Script:**
> "Let me show you the heart of our system - the Enhanced IDS class. This implements both detection methods simultaneously, protecting against five different attack types."

### Screen: Scroll to line 209 (configuration thresholds)

**Script:**
> "All detection thresholds are configurable. We detect five attack categories: PORT_SCAN after 10 unique ports, SYN_FLOOD after 50 packets with low ACK ratio, ICMP_FLOOD using a 5-second sliding window, DNS_TUNNEL when subdomains exceed 30 characters with hex patterns, and ARP_SPOOF when we detect MAC address changes."

```python
# SHOW THESE LINES (209-215):
self.PORT_SCAN_THRESHOLD = 10
self.SYN_FLOOD_THRESHOLD = 50
self.ICMP_FLOOD_THRESHOLD = 50
self.DNS_TUNNEL_MIN_LENGTH = 30
self.ANOMALY_Z_THRESHOLD = 3.0
```

### Screen: Scroll to signature detection methods (lines 300-400)

**Script:**
> "For signature-based detection, we track connection states per IP address. Here's our port scan detector - it counts unique destination ports per source IP and triggers when the threshold is exceeded. The SYN flood detector tracks the ratio of SYN packets to ACKs, identifying incomplete handshakes."

**Show briefly:**
- `detect_port_scan()` method
- `detect_syn_flood()` method
- `detect_dns_tunnel()` method

### Screen: Scroll to anomaly detection methods (lines 450-550)

**Script:**
> "For anomaly-based detection, we implemented Shannon entropy analysis - this is directly from our CSCD58 coursework. Shannon entropy measures the randomness of port distributions. A port scan hitting random ports creates high entropy compared to normal traffic patterns. We also use Z-score calculations with 3-sigma thresholds to detect traffic volume anomalies and inter-arrival timing analysis for burst detection."

**Show and explain:**
- `calculate_entropy()` method - point out the Shannon entropy formula
- `detect_traffic_volume_anomaly()` method - mention Z-score from class
- Baseline training concept

**Script:**
> "The entropy calculation here - negative sum of p times log p - is exactly the Shannon entropy we learned in class. When port distribution becomes too random, entropy spikes and we catch it."

---

## 🎬 PART 3: Interactive Menu Demo (1 minute)

### Screen: Terminal - run interactive demo

**Commands:**
```bash
cd ids/
python3 demo_terminal_attacks.py
```

**Script:**
> "Let's see the system in action. First, we have an interactive menu where you can select individual attacks to demonstrate. This is perfect for live presentations where you want to show specific attack types."

**Show the menu, then select option 5 (Run All Demos):**

**Script:**
> "I'll select option 5 to run all four attack types in sequence. Watch as it generates synthetic traffic using Scapy and analyzes it in real-time."

**Wait for output, narrate as it runs:**

> "Port scan executing... detected! SYN flood attack... caught! ICMP ping flood... identified! DNS tunneling with hex-encoded subdomains... detected! All four attacks successfully identified."

---

## 🎬 PART 4: Quick Automated Demo with Report (2 minutes)

### Screen: Terminal - run automated demo

**Commands:**
```bash
python3 run_all_demos.py
```

**Script:**
> "Now let's use our automated demo script which is faster and better for quick testing. This runs the same attacks but optimized for speed."

**Wait for completion (~30 seconds)**

**Script:**
> "Notice how quickly it processes - this demonstrates the efficiency of our detection engine. Now let's generate a report from this data."

### Screen: Terminal - generate report from demo data

**Commands:**
```bash
python3 test_dynamic_ids.py
```

**Script:**
> "This script generates synthetic attacks and creates a full HTML report with visualizations. This takes about 10 seconds."

**While running:**
> "It's generating attack traffic, analyzing with both signature and anomaly detection, creating six visualization charts, and building an HTML report."

### Screen: HTML report opens in browser (from test_dynamic_ids.py)

**Script:**
> "Here's our first report - generated from synthetic testing. You can see the attack distribution, timeline, detection metrics, and performance statistics. Notice this is fully dynamic - every metric, every chart, every number is calculated from actual test data, nothing is hardcoded."

**Scroll through quickly:**
- Point out detection rates
- Show one or two charts
- Highlight the statistics

**Script:**
> "This works great for rapid development and testing. But now let me show you something more impressive - testing with real attack tools in an isolated Docker environment."

---

## 🎬 PART 5: Comprehensive Docker Workflow (3 minutes)

### Screen: Terminal - show Docker setup

**Commands:**
```bash
cd ..
docker-compose ps
```

**Script:**
> "Now for the comprehensive demonstration using real network infrastructure. We have three Docker containers: an attacker with actual penetration testing tools like nmap and hping3, a victim system running tcpdump to capture traffic, and our IDS for analysis. This simulates a realistic network environment."

### Screen: Terminal - run comprehensive workflow

**Commands:**
```bash
cd ids/
python3 workflow_docker_comprehensive.py
```

**Script:**
> "This workflow executes three phases of attacks. Phase 1 uses real tools like nmap for port scanning, hping3 for SYN floods, and dig for DNS tunneling. Phase 2 generates high-entropy anomaly attacks. Phase 3 creates timing-based anomalies with burst patterns."

**While running, narrate the phases:**

**Phase 1 (Signature Attacks):**
> "Starting with signature-based attacks using actual penetration testing tools... port scan executing... SYN scan... ARP spoofing... ICMP flood... DNS tunneling with 25 suspicious queries."

**Phase 2 (Anomaly Attacks):**
> "Now Phase 2 - high-entropy attacks designed to test our anomaly detection. These send packets to random ports creating unusual distribution patterns."

**Phase 3 (Timing Attacks):**
> "Phase 3 tests our timing analysis with burst-pause-burst patterns that deviate from normal traffic rhythms."

**When capture completes:**
> "Excellent! The packet capture is complete - we have 509 packets captured from real network traffic. Now our IDS analyzes the captured PCAP file..."

**During analysis:**
> "You can see alerts being generated in real-time as packets are processed. Port scans detected... high entropy anomalies caught using Shannon entropy calculations... SYN flood identified... ICMP flood detected... DNS tunneling alerts for suspicious hex-encoded subdomains..."

### Screen: Terminal - show PCAP file details

**Commands:**
```bash
ls -lh ../pcaps/docker_comprehensive_capture.pcap
```

**Script:**
> "The capture produced a 35KB PCAP file. These PCAP files are in standard pcap format, compatible with any network analysis tool. Let me show you what the actual packets look like."

### Screen: Open Wireshark with the PCAP file

**Commands:**
```bash
open -a Wireshark ../pcaps/docker_comprehensive_capture.pcap
```

**Script:**
> "Opening this in Wireshark... Here you can see the raw packet capture. Notice the variety of traffic - TCP SYN packets from the port scans, ARP replies from the spoofing attack, ICMP echo requests from the flood, and DNS queries with those suspicious long subdomains for tunneling."

### Screen: In Wireshark - filter and show specific attacks

**Point out (don't need to type, just narrate):**

**Script:**
> "If I filter for TCP with the SYN flag set, you can see the port scan and SYN flood packets - all coming from 10.0.0.20, the attacker IP. Look at the destination ports - they're hitting sequential ports for the scan, exactly what our IDS detected."

**Show DNS queries:**
> "And here are the DNS queries - see these subdomains? 32 character hex strings like '3c0b7b88621d37d2be0bcde2623bbddf' - classic data exfiltration pattern. Our IDS caught all 25 of these."

**Show ICMP:**
> "The ICMP flood shows up here - 180 echo requests in rapid succession. Our sliding window detector caught this immediately."

**Script:**
> "This demonstrates that our system works with real, standard packet captures that security teams actually use. Any tool that reads PCAP format can analyze our captures."

---

## 🎬 PART 6: Docker Results & Report Analysis (3 minutes)

### Screen: Back to terminal - analysis complete

**Script:**
> "Perfect! The analysis is complete. Let's look at the results: 67 total alerts detected - 53 from signature-based detection covering five attack types, and 14 from anomaly-based detection using Shannon entropy and Z-score analysis. That's a 13.2% detection rate from 509 packets with zero false positives."

**Script (elaborate on attacks):**
> "To break that down by attack type: we caught port scanning - the classic reconnaissance attack, SYN floods designed to exhaust server resources, ICMP floods flooding the network with ping traffic, DNS tunneling for covert data exfiltration, ARP spoofing for man-in-the-middle attacks, and high-entropy anomalies that don't match any signature but show statistically unusual behavior."

### Screen: HTML report opens in browser (Docker workflow)

**Script:**
> "The workflow automatically generates a professional HTML report. Now watch - this is where you can really see the difference between synthetic testing and real Docker attacks."

### Screen: Split or switch between both reports

**Script:**
> "Let me show you both reports side by side. On the left is our synthetic test report - clean, predictable attack patterns. On the right is the Docker report with real attack tools. Notice the differences:"

**Point out key differences:**

1. **Packet Counts**
   > "The Docker test analyzed 509 real packets captured from the network, while synthetic testing is more controlled."

2. **Alert Distribution**
   > "Look at the attack distribution - the Docker environment shows the full attack spectrum: 27 port scan alerts, 25 DNS tunneling events, 14 high-entropy anomalies detected using Shannon entropy from our coursework, plus SYN floods, ICMP floods, and ARP spoofing. The synthetic test is more focused on basic signature attacks."

3. **Attack Timeline**
   > "The timeline is particularly interesting - synthetic attacks are evenly spaced, but real Docker attacks show the actual timing patterns from nmap and hping3 tools."

4. **Detection Metrics**
   > "Both show 100% detection rate with zero false positives, proving our system works consistently across different testing environments."

### Screen: Focus on Docker report - scroll through sections

**Point out each section:**

1. **Executive Summary**
   > "Comprehensive metrics - 67 alerts from 509 packets, both detection types active."

2. **Alert Distribution Chart**
   > "Port scans dominate with 27 alerts, DNS tunneling with 25 suspicious queries, high entropy anomalies with 14 - that's our Shannon entropy detection catching random port distributions that deviate from the baseline. We also caught SYN floods, ICMP floods, and ARP spoofing. This reflects real attack tool behavior across all five attack categories we implemented."

3. **Severity Distribution**
   > "Threat levels properly categorized - critical SYN floods, high-severity port scans, medium-level anomalies."

4. **Attack Timeline**
   > "You can see the three attack phases - signature attacks clustered in the first 10 seconds, anomaly attacks in the middle, timing attacks at the end."

5. **Performance Metrics**
   > "Processing 13 packets per second with sub-second analysis time. Production-ready performance."

### Screen: Show outputs folder structure

**Commands:**
```bash
cd ids
ls -la outputs/visualizations/
cat outputs/logs/alerts.log | head -20
```

**Script:**
> "Everything is automatically organized: six PNG charts for presentations, detailed alert logs with precise timestamps and severity levels, JSON metrics for integration with SIEM systems or other security tools. This is production-ready output."

---

## 🎬 PART 7: Live Threshold Customization (2.5 minutes)

### Screen: Open `enhanced_ids.py` in editor - line 209

**Script:**
> "Now let me demonstrate the system's configurability. All detection thresholds are easily adjustable. Let's make the port scan detection more sensitive and see the immediate impact."

### Screen: Show current thresholds (lines 209-215)

**Script:**
> "Currently, port scan detection triggers after 10 unique ports. Let's make it more aggressive - we'll change it to 5 ports. We'll also make SYN flood detection stricter, from 50 packets down to 30."

### Screen: Edit the file

**Show the changes:**
```python
# BEFORE:
self.PORT_SCAN_THRESHOLD = 10
self.SYN_FLOOD_THRESHOLD = 50

# AFTER:
self.PORT_SCAN_THRESHOLD = 5
self.SYN_FLOOD_THRESHOLD = 30
```

**Script:**
> "I'm changing PORT_SCAN_THRESHOLD from 10 to 5, and SYN_FLOOD_THRESHOLD from 50 to 30. Saving the file..."

### Screen: Terminal - save and rerun quick test

**Commands:**
```bash
# Save the file first (Cmd+S)
python3 test_dynamic_ids.py
```

**Script:**
> "Now let's regenerate the report with these new thresholds. The system will immediately apply the stricter detection rules. This takes about 10 seconds."

**While running:**
> "Notice - same attack patterns, but now we're expecting more alerts because our thresholds are lower. The system should detect port scans earlier and SYN floods with fewer packets."

### Screen: New HTML report opens

**Script:**
> "Perfect! Look at the results. With the stricter thresholds, we now have more port scan alerts - the system caught scanning activity after just 5 ports instead of waiting for 10. The SYN flood was also detected earlier in the attack sequence."

### Screen: Compare alert counts in report

**Script:**
> "Let me show you the difference. The alert distribution chart shows increased detection events because we lowered the sensitivity thresholds. The attack timeline shows alerts triggering earlier. This demonstrates how easily security teams can tune the IDS to match their network's security policy - stricter for high-security environments, more relaxed for development networks."

### Screen: Terminal - restore original thresholds

**Commands:**
```bash
# Open enhanced_ids.py again
```

**Script:**
> "Let me restore the original thresholds for production use. I'm changing them back to 10 and 50. This flexibility is crucial for production deployment where different networks have different threat models."

**Show restoring:**
```python
# RESTORED:
self.PORT_SCAN_THRESHOLD = 10
self.SYN_FLOOD_THRESHOLD = 50
```

**Save the file**

---

## 🎬 PART 8: Conclusion (30 seconds)

---

## 🎬 PART 8: Conclusion (30 seconds)

### Screen: Show README.md - Key Achievements section or project structure

**Script:**
> "To summarize: we've built a production-ready Network Intrusion Detection System with dual detection methods achieving 100% detection rate across all testing modes. The system handles everything from synthetic testing to real Docker-based attacks with actual penetration testing tools. Reports are fully dynamic and automatically generated, and detection thresholds can be tuned in seconds for different security requirements."

### Screen: Show outputs folder with all generated files

**Commands:**
```bash
ls -la outputs/
tree outputs/  # if tree is installed, otherwise use ls
```

**Script:**
> "All outputs are production-ready: HTML reports for management, JSON metrics for SIEM integration, detailed logs for forensics, and PCAP files compatible with standard tools like Wireshark. Thank you for watching!"

---

## 🎯 Key Points to Emphasize

✅ **Opening Hook** - Clear roadmap of what you'll demonstrate  
✅ **Five Attack Types** - PORT_SCAN, SYN_FLOOD, ICMP_FLOOD, DNS_TUNNEL, ARP_SPOOF  
✅ **Course Concepts** - Shannon entropy and Z-score from CSCD58  
✅ **Dual Detection** - Both signature AND anomaly-based working simultaneously  
✅ **Multiple Testing Modes** - Interactive, automated, and Docker-based  
✅ **PCAP Analysis** - Show raw packets in Wireshark for context  
✅ **Dynamic Reporting** - Compare synthetic vs real attack reports  
✅ **Real Tools** - Docker with nmap, hping3, not just synthetic traffic  
✅ **100% Detection** - All attacks caught across all testing modes  
✅ **Live Customization** - Change thresholds, regenerate report, show impact  
✅ **Professional Output** - HTML reports with embedded charts  
✅ **Production Ready** - Clean code, organized structure, zero false positives  

---

## 📊 Timing Breakdown

| Section | Time | Content |
|---------|------|---------|
| Opening Overview | 0.5 min | What we'll demonstrate |
| Introduction | 1 min | Project overview, architecture |
| Code Walkthrough | 2.5 min | Detection engine, Shannon entropy, 5 attacks |
| Interactive Menu Demo | 1 min | Menu-driven attack selection |
| Quick Demo + Report | 2 min | Automated demo, synthetic report |
| Docker Workflow | 3 min | Comprehensive real testing |
| Wireshark PCAP Analysis | 1.5 min | Show raw packets in Wireshark |
| Report Analysis | 3 min | Compare reports, attack breakdown |
| Threshold Customization | 2.5 min | Live editing, regeneration, comparison |
| Conclusion | 0.5 min | Summary and outputs |
| **TOTAL** | **17.5 min** | Complete demonstration |

**Note:** Can be shortened to 10 minutes by:
- Combining Opening + Introduction to 1 min
- Reducing code walkthrough to 1 min (show Shannon entropy code briefly)
- Skip interactive menu (go straight to automated demo)
- Reducing Docker workflow narration to 2 min (let it run)
- Skip Wireshark section (1.5 min saved)
- Reducing report comparison to 1.5 min (key differences only)
- Reducing threshold demo to 1.5 min (one threshold change, quick comparison)
- This gives you: 1 + 1 + 2 + 2 + 1.5 + 1.5 + 0.5 = **10 minutes**

---

## 🎥 Recording Tips

1. **Clean Terminal:** Run `clear` before each command
2. **Font Size:** Increase terminal font for readability (20-24pt)
3. **Speed:** Speak clearly, pause between sections
4. **Browser:** Close unnecessary tabs before showing HTML report
5. **Preparation:** Run workflow once before recording to ensure containers are ready
6. **Smooth Transitions:** Use Command+Tab (Mac) for clean screen transitions

---

## ✅ Pre-Demo Checklist

- [ ] Docker containers running (`docker-compose up -d`)
- [ ] Terminal font size increased (20-24pt)
- [ ] Wireshark installed and ready
- [ ] Browser tabs cleaned
- [ ] All previous outputs cleared (`rm -rf ids/outputs/*`)
- [ ] Test run completed successfully
- [ ] Screen recording software ready
- [ ] Microphone tested
- [ ] Script reviewed and practiced
- [ ] Have `enhanced_ids.py` ready in editor for quick threshold editing
- [ ] Keep two browser tabs ready for report comparison
- [ ] Have PCAP file path ready for Wireshark: `../pcaps/docker_comprehensive_capture.pcap`

---

## 🚀 Quick Test Run Commands

Before recording, verify everything works:

```bash
# Start Docker
docker-compose up -d
docker-compose ps

# Interactive demo test
cd ids/
python3 demo_terminal_attacks.py
# (Select option 6 to exit)

# Quick automated demo
python3 run_all_demos.py

# Generate synthetic report
python3 test_dynamic_ids.py
open outputs/reports/ids_report.html

# Full Docker workflow test
python3 workflow_docker_comprehensive.py

# Test Wireshark opens properly
open -a Wireshark ../pcaps/docker_comprehensive_capture.pcap

# Verify Docker outputs
ls outputs/visualizations/
cat outputs/logs/alerts.log | head
```

**Pro Tip:** Keep both HTML reports open in separate browser tabs so you can quickly switch between them during the comparison section!

**Wireshark Filters to Prepare:**
- `tcp.flags.syn == 1` - Show SYN packets (port scan/flood)
- `dns` - Show DNS queries (tunneling)
- `icmp.type == 8` - Show ICMP echo requests (flood)
- `arp` - Show ARP traffic (spoofing)

---

**Good luck with your demo! 🎬**
