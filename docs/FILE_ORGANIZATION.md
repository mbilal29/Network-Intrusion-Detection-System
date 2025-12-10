# IDS Folder Organization

## ✅ Essential Files (Keep)

### Core IDS
- `enhanced_ids.py` - Main IDS with dual detection (signature + anomaly)
- `baseline_model.pkl` - Trained baseline for anomaly detection

### Testing & Workflows
- `test_dynamic_ids.py` - Generates randomized attacks, tests IDS
- `test_docker_hybrid.py` - Docker-based realistic attack testing
- `run_complete_test.py` - Complete Python workflow (10-20s)
- `run_docker_workflow.py` - Complete Docker workflow (30-45s)

### Visualization & Reporting
- `create_dynamic_visualizations.py` - Generates 6 chart images
- `generate_report.py` - Creates HTML report with embedded charts

### Output Folders
- `outputs/visualizations/` - PNG charts
- `outputs/reports/` - HTML reports
- `outputs/logs/` - alerts.log, evaluation_results.json

## 🗑️ Legacy Files (Can Remove)

These files were used in earlier versions but are no longer part of the current workflows:

- `sniffer.py` - Old basic sniffer (replaced by enhanced_ids.py)
- `evaluate_enhanced_ids.py` - Old evaluation script (replaced by test_dynamic_ids.py)
- `test_enhanced_ids.py` - Old test harness (replaced by test_dynamic_ids.py)
- `generate_traffic.py` - Old traffic generator (replaced by randomized attacks)
- `generate_baseline.py` - Old baseline generator (baseline now pre-trained)
- `generate_anomaly_attacks.py` - Old attack generator (replaced by test_docker_hybrid.py)
- `generate_custom_attacks.py` - Old custom attack generator
- `run_full_analysis.py` - Old analysis script

## 📊 Workflow Summary

**Current System Uses:**

### Python Workflow (Fast)
```
run_complete_test.py
  ├── test_dynamic_ids.py (generates attacks, tests IDS)
  ├── create_dynamic_visualizations.py (creates charts)
  └── generate_report.py (creates HTML report)
```

### Docker Workflow (Realistic)
```
run_docker_workflow.py
  ├── test_docker_hybrid.py (real Docker attacks + PCAPs)
  ├── create_dynamic_visualizations.py (creates charts)
  └── generate_report.py (creates HTML report)
```

Both workflows depend on:
- `enhanced_ids.py` (core IDS)
- `baseline_model.pkl` (anomaly detection model)
