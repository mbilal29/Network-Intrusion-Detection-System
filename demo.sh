#!/bin/bash

# Network Intrusion Detection System - Demo Script
# CSCD58 Course Project Demo

echo "======================================================================"
echo "🚀 NETWORK INTRUSION DETECTION SYSTEM - DEMO"
echo "======================================================================"
echo ""
echo "Project by: Bilal (Docker Setup) & Zuhair (IDS Implementation)"
echo "Course: CSCD58 - Computer Networks"
echo "Date: December 2, 2025"
echo ""
echo "======================================================================"

# Move to ids directory
cd ids

echo ""
echo "📋 DEMO AGENDA:"
echo "  1. Show project structure"
echo "  2. Display IDS code highlights"
echo "  3. Run IDS on port scan attack"
echo "  4. Run IDS on ARP spoofing attack"
echo "  5. Show performance evaluation results"
echo ""
read -p "Press ENTER to start demo..."

# 1. Project Structure
echo ""
echo "======================================================================"
echo "📁 STEP 1: PROJECT STRUCTURE"
echo "======================================================================"
cd ..
tree -L 2 -I '__pycache__' 2>/dev/null || ls -lR | grep "^d" || find . -maxdepth 2 -type d
echo ""
read -p "Press ENTER to continue..."

# 2. Code Highlights
echo ""
echo "======================================================================"
echo "💻 STEP 2: IDS CODE HIGHLIGHTS"
echo "======================================================================"
echo ""
echo "PORT SCAN DETECTION:"
echo "─────────────────────"
cat ids/simple_ids.py | grep -A 10 "def detect_port_scan" | head -15
echo ""
echo "ARP SPOOF DETECTION:"
echo "─────────────────────"
cat ids/simple_ids.py | grep -A 8 "def detect_arp_spoof" | head -12
echo ""
read -p "Press ENTER to continue..."

# 3. Port Scan Demo
echo ""
echo "======================================================================"
echo "🎯 STEP 3: DETECTING PORT SCAN ATTACK"
echo "======================================================================"
echo ""
echo "Running IDS on portscan.pcap (50 packets scanning ports 1-50)..."
echo ""
cd ids
python3 test_pcap.py ../pcaps/portscan.pcap 2>&1 | tail -30
echo ""
read -p "Press ENTER to continue..."

# 4. ARP Spoof Demo
echo ""
echo "======================================================================"
echo "🎯 STEP 4: DETECTING ARP SPOOFING ATTACK"
echo "======================================================================"
echo ""
echo "Running IDS on arpspoof.pcap (MAC address change)..."
echo ""
python3 test_pcap.py ../pcaps/arpspoof.pcap
echo ""
read -p "Press ENTER to continue..."

# 5. Evaluation Results
echo ""
echo "======================================================================"
echo "📊 STEP 5: PERFORMANCE EVALUATION RESULTS"
echo "======================================================================"
echo ""
cat evaluation_output.txt | grep -A 20 "OVERALL EVALUATION SUMMARY"
echo ""
echo "======================================================================"
echo "📄 FULL REPORT: See FINAL_REPORT.md"
echo "📊 DETAILED METRICS: See evaluation_results.json"
echo "🚨 ALERT LOG: See ids/alerts.log"
echo "======================================================================"
echo ""
echo "✅ DEMO COMPLETE!"
echo ""
echo "KEY ACHIEVEMENTS:"
echo "  ✓ Port Scan Detection: 100% success rate"
echo "  ✓ ARP Spoofing Detection: 100% success rate"
echo "  ✓ Zero False Positives on normal traffic"
echo "  ✓ Processing Speed: 21,672 packets/second"
echo ""
echo "======================================================================"
