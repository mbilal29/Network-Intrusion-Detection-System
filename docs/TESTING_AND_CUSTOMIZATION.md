# 🎓 Professor Testing & Customization Guide

## 📊 Generating Full Reports

### Quick Demo vs Full Report

**Interactive Demo (`demo_terminal_attacks.py`):**
```bash
python3 demo_terminal_attacks.py
```
- ✅ Shows real-time attack detection
- ✅ Perfect for live demonstrations
- ❌ Does NOT generate HTML report
- ❌ Does NOT create visualizations

**Quick Demo (`run_all_demos.py`):**
```bash
python3 run_all_demos.py
```
- ✅ Runs all 4 attacks in sequence
- ✅ Shows detection results
- ❌ Does NOT generate HTML report
- ❌ Does NOT create visualizations

**For Full Report with Charts:**
```bash
# Option 1: Synthetic Testing (10 seconds)
python3 test_dynamic_ids.py

# Option 2: Docker Comprehensive (60 seconds) - MOST REALISTIC
python3 workflow_docker_comprehensive.py
```
- ✅ Generates complete HTML report
- ✅ Creates 6 visualization charts
- ✅ Includes all metrics and statistics
- ✅ Opens report in browser automatically

---

## 🔧 Customizing Detection Thresholds

All detection thresholds are **global constants at the top of `enhanced_ids.py`** (lines 16-28):

### Current Default Thresholds
```python
# ============================================================================
# DETECTION THRESHOLDS - EASY TO MODIFY FOR TESTING
# ============================================================================
# Signature-Based Detection Thresholds
PORT_SCAN_THRESHOLD = 10          # Alert after scanning X unique ports
SYN_FLOOD_THRESHOLD = 50          # Alert after X SYN packets without responses
SYN_FLOOD_RATIO = 0.1             # Alert if SYN/ACK ratio below X (10% responses)
ICMP_FLOOD_THRESHOLD = 50         # Alert after X ICMP packets in time window
ICMP_FLOOD_WINDOW = 5             # Time window in seconds for ICMP flood detection
DNS_TUNNEL_MIN_LENGTH = 30        # Alert if DNS subdomain longer than X characters
DNS_TUNNEL_HEX_THRESHOLD = 0.6    # Alert if subdomain has >X% hexadecimal characters

# Anomaly-Based Detection Thresholds
ANOMALY_Z_THRESHOLD = 3.0         # Alert if z-score exceeds X standard deviations
PORT_ENTROPY_MULTIPLIER = 1.3     # Alert if entropy > baseline * X
ANOMALY_WINDOW_DURATION = 10      # Time window in seconds for anomaly detection
```

**Why at the top?** 
- ✅ Easy to find (first 30 lines of code)
- ✅ No need to search through 500+ lines
- ✅ Clear documentation with comments
- ✅ Professor can modify without understanding entire codebase

---

## 🧪 Testing Custom Thresholds

### Example 1: Make SYN Flood Detection MORE Strict

**Goal**: Only detect SYN floods with 100+ packets (instead of 50)

**Steps:**
1. Open `enhanced_ids.py`
2. Find **line 18** (near top of file):
   ```python
   SYN_FLOOD_THRESHOLD = 50
   ```
3. Change to:
   ```python
   SYN_FLOOD_THRESHOLD = 100
   ```
4. Save the file
5. Run full test:
   ```bash
   python3 workflow_docker_comprehensive.py
   ```
6. Open the generated report to see changes reflected

**Expected Result:**
- Before: SYN flood detected with 50+ packets
- After: SYN flood NOT detected until 100+ packets
- Report will show fewer SYN_FLOOD alerts

---

### Example 2: Make Port Scan Detection LESS Strict

**Goal**: Only alert after scanning 50 ports (instead of 10)

**Steps:**
1. Open `enhanced_ids.py`
2. Find **line 17** (near top):
   ```python
   PORT_SCAN_THRESHOLD = 10
   ```
3. Change to:
   ```python
   PORT_SCAN_THRESHOLD = 50
   ```
4. Save the file
5. Run test:
   ```bash
   python3 test_dynamic_ids.py
   ```
6. Check report - fewer PORT_SCAN alerts

---

### Example 3: Disable SYN Flood Detection Entirely

**Goal**: Never detect SYN floods (set threshold impossibly high)

**Steps:**
1. Open `enhanced_ids.py`
2. Change **line 18**:
   ```python
   SYN_FLOOD_THRESHOLD = 999999
   ```
3. Save and run:
   ```bash
   python3 workflow_docker_comprehensive.py
   ```

**Expected Result:**
- Report shows 0 SYN_FLOOD alerts
- All other detections still work normally

---

### Example 4: Make DNS Tunneling Detection MORE Sensitive

**Goal**: Detect shorter DNS queries (20 chars instead of 30)

**Steps:**
1. Open `enhanced_ids.py`
2. Find **line 22**:
   ```python
   DNS_TUNNEL_MIN_LENGTH = 30
   ```
3. Change to:
   ```python
   DNS_TUNNEL_MIN_LENGTH = 20
   ```
4. Run Docker workflow:
   ```bash
   python3 workflow_docker_comprehensive.py
   ```

**Expected Result:**
- More DNS_TUNNEL alerts detected
- Report shows higher alert count

---

## 📈 Verifying Changes in Report

After modifying thresholds, the changes are reflected in:

### 1. Terminal Output
```bash
🚨 DETECTION RESULTS:
   Total Alerts: 52  # Number will change based on thresholds
```

### 2. HTML Report Sections

**Alert Summary Table:**
```
Total Alerts: [changes based on thresholds]
Signature-Based: [changes]
Anomaly-Based: [changes]
```

**Alerts by Type Chart:**
- PORT_SCAN count changes
- SYN_FLOOD count changes
- ICMP_FLOOD count changes
- etc.

**Detailed Alerts Log:**
- Shows actual alerts generated
- Missing alerts mean threshold not reached

### 3. Evaluation Metrics JSON
Located at: `ids/outputs/logs/evaluation_results.json`
```json
{
  "total_alerts": 52,
  "signature_based": 41,
  "anomaly_based": 11,
  "alert_counts": {
    "PORT_SCAN": 35,
    "SYN_FLOOD": 1,    # ← This changes with threshold
    "ICMP_FLOOD": 1,
    "DNS_TUNNEL": 15
  }
}
```

---

## 🎯 Complete Testing Workflow for Professor

### Scenario: Test SYN Flood Threshold Modification

**Step 1: Baseline Test (Current Thresholds)**
```bash
cd ids/
python3 workflow_docker_comprehensive.py
# Note the number of SYN_FLOOD alerts (should be 1)
```

**Step 2: Modify Threshold**
```bash
# Open enhanced_ids.py
# Change line 210:
self.SYN_FLOOD_THRESHOLD = 100  # Was 50
```

**Step 3: Retest with New Threshold**
```bash
python3 workflow_docker_comprehensive.py
# Note the number of SYN_FLOOD alerts (should be 0 now)
```

**Step 4: Compare Reports**
- **Before**: `ids/outputs/reports/ids_report.html` shows 1 SYN_FLOOD alert
- **After**: New report shows 0 SYN_FLOOD alerts
- **Why**: Attack only sends ~50 SYNs, threshold now requires 100

---

## 📝 Quick Reference: All Configurable Thresholds

**Location**: `enhanced_ids.py` - **Lines 16-28** (top of file)

| Threshold | Line # | Default | Purpose |
|-----------|--------|---------|---------|
| `PORT_SCAN_THRESHOLD` | 17 | 10 | Unique ports before alert |
| `SYN_FLOOD_THRESHOLD` | 18 | 50 | SYN packets before alert |
| `SYN_FLOOD_RATIO` | 19 | 0.1 | SYN/ACK response ratio (10%) |
| `ICMP_FLOOD_THRESHOLD` | 20 | 50 | ICMP packets in time window |
| `ICMP_FLOOD_WINDOW` | 21 | 5 | Time window for ICMP (seconds) |
| `DNS_TUNNEL_MIN_LENGTH` | 22 | 30 | Subdomain length to check |
| `DNS_TUNNEL_HEX_THRESHOLD` | 23 | 0.6 | Hex character ratio (60%) |
| `ANOMALY_Z_THRESHOLD` | 26 | 3.0 | Standard deviations for anomaly |
| `PORT_ENTROPY_MULTIPLIER` | 27 | 1.3 | Entropy threshold multiplier |
| `ANOMALY_WINDOW_DURATION` | 28 | 10 | Anomaly detection window (seconds) |

---

## 🔬 Advanced: Testing Multiple Configurations

### Automated Testing Script Idea
```bash
#!/bin/bash
# Test different thresholds

echo "Test 1: Default thresholds"
python3 workflow_docker_comprehensive.py
mv ids/outputs/reports/ids_report.html reports/test1_default.html

# Modify threshold in script (sed or manual)
echo "Test 2: Strict SYN threshold (100)"
# Change threshold to 100
python3 workflow_docker_comprehensive.py
mv ids/outputs/reports/ids_report.html reports/test2_strict_syn.html

# Compare the two reports side-by-side
```

---

## 💡 Demo Script for Presentation

**What to say during demo:**

> "For quick interactive demos, we can run `python3 demo_terminal_attacks.py` which shows real-time detection of individual attacks.
>
> However, for a **complete report with visualizations and metrics**, we run:
>
> ```bash
> python3 workflow_docker_comprehensive.py
> ```
>
> This generates a professional HTML report with 6 charts showing alert distributions, timelines, and detailed analysis.
>
> All detection thresholds are easily configurable in `enhanced_ids.py`. For example, if you want to test stricter SYN flood detection, simply change `self.SYN_FLOOD_THRESHOLD` from 50 to 100, and rerun the workflow. The changes will be reflected in the generated report immediately."

---

## ✅ Summary

**For Demos (No Report):**
- `demo_terminal_attacks.py` - Interactive
- `run_all_demos.py` - Automated sequence

**For Full Reports:**
- `test_dynamic_ids.py` - Fast synthetic (10s)
- `workflow_docker_comprehensive.py` - Realistic Docker (60s) ⭐ **RECOMMENDED**

**To Modify Detection:**
1. Edit `enhanced_ids.py` lines 209-215
2. Change threshold values
3. Save file
4. Rerun workflow
5. Check new report

**Changes appear in:**
- Terminal output
- HTML report charts
- Alert count tables
- JSON metrics file
- Detailed alert logs
