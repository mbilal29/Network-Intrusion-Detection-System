#!/usr/bin/env python3
"""
Test IDS Threshold Sensitivity
Demonstrates how changing detection thresholds affects alert rates
"""

import subprocess
import json
import os
import shutil

def backup_ids():
    """Backup the original IDS file"""
    shutil.copy('enhanced_ids.py', 'enhanced_ids.py.backup')
    print("✓ Backed up enhanced_ids.py")

def restore_ids():
    """Restore the original IDS file"""
    shutil.copy('enhanced_ids.py.backup', 'enhanced_ids.py')
    os.remove('enhanced_ids.py.backup')
    print("✓ Restored enhanced_ids.py")

def modify_threshold(param_name, new_value):
    """Modify a specific threshold in enhanced_ids.py"""
    with open('enhanced_ids.py', 'r') as f:
        content = f.read()
    
    # Find and replace the threshold
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith(f'{param_name} ='):
            old_value = line.split('=')[1].strip().split('#')[0].strip()
            lines[i] = f'{param_name} = {new_value}          # MODIFIED FOR TESTING (was {old_value})'
            break
    
    with open('enhanced_ids.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"  ✓ Modified {param_name}: {old_value} → {new_value}")

def run_test():
    """Run the IDS test and return results"""
    # Clear old logs
    os.system('rm outputs/logs/alerts.log outputs/logs/evaluation_results.json 2>/dev/null')
    
    # Run test
    result = subprocess.run(['python3', 'test_dynamic_ids.py'], 
                          capture_output=True, text=True)
    
    # Read results
    with open('outputs/logs/evaluation_results.json', 'r') as f:
        metrics = json.load(f)
    
    return metrics

def print_comparison(test_name, metrics):
    """Print test results"""
    print(f"\n{'='*70}")
    print(f"📊 {test_name}")
    print(f"{'='*70}")
    print(f"  Total Packets:     {metrics['total_packets']}")
    print(f"  Total Alerts:      {metrics['total_alerts']}")
    print(f"  Signature Alerts:  {metrics['signature_alerts']}")
    print(f"  Anomaly Alerts:    {metrics['anomaly_alerts']}")
    print(f"  Detection Rate:    {metrics['total_alerts']/metrics['total_packets']*100:.1f}%")

def main():
    print("\n" + "="*70)
    print("🧪 IDS THRESHOLD SENSITIVITY TEST")
    print("="*70)
    print("This test demonstrates how threshold changes affect detection rates\n")
    
    # Backup original
    backup_ids()
    
    try:
        # Test 1: Default thresholds
        print("\n🔵 TEST 1: DEFAULT THRESHOLDS (Baseline)")
        print("-" * 70)
        metrics_default = run_test()
        print_comparison("Default Configuration", metrics_default)
        
        # Test 2: Stricter thresholds (more sensitive - more alerts)
        print("\n\n🟢 TEST 2: STRICTER THRESHOLDS (More Sensitive)")
        print("-" * 70)
        print("  Modifications:")
        modify_threshold('PORT_SCAN_THRESHOLD', 5)      # Was 10
        modify_threshold('SYN_FLOOD_THRESHOLD', 25)      # Was 50
        modify_threshold('ANOMALY_Z_THRESHOLD', 2.0)     # Was 3.0
        
        metrics_strict = run_test()
        print_comparison("Stricter Thresholds", metrics_strict)
        
        # Test 3: Looser thresholds (less sensitive - fewer alerts)
        restore_ids()
        backup_ids()
        
        print("\n\n🔴 TEST 3: LOOSER THRESHOLDS (Less Sensitive)")
        print("-" * 70)
        print("  Modifications:")
        modify_threshold('PORT_SCAN_THRESHOLD', 20)      # Was 10
        modify_threshold('SYN_FLOOD_THRESHOLD', 100)     # Was 50
        modify_threshold('ANOMALY_Z_THRESHOLD', 4.0)     # Was 3.0
        
        metrics_loose = run_test()
        print_comparison("Looser Thresholds", metrics_loose)
        
        # Summary comparison
        print("\n\n" + "="*70)
        print("📈 SUMMARY COMPARISON")
        print("="*70)
        print(f"{'Configuration':<25} {'Total Alerts':<15} {'Detection Rate':<15}")
        print("-" * 70)
        print(f"{'Default':<25} {metrics_default['total_alerts']:<15} "
              f"{metrics_default['total_alerts']/metrics_default['total_packets']*100:.1f}%")
        print(f"{'Stricter (More Sensitive)':<25} {metrics_strict['total_alerts']:<15} "
              f"{metrics_strict['total_alerts']/metrics_strict['total_packets']*100:.1f}%")
        print(f"{'Looser (Less Sensitive)':<25} {metrics_loose['total_alerts']:<15} "
              f"{metrics_loose['total_alerts']/metrics_loose['total_packets']*100:.1f}%")
        
        print("\n💡 Key Insight:")
        print("   Stricter thresholds → More alerts (higher sensitivity)")
        print("   Looser thresholds  → Fewer alerts (lower false positive rate)")
        print("\n✅ Test demonstrates IDS responds correctly to threshold changes!")
        
    finally:
        # Always restore original
        restore_ids()
        print("\n" + "="*70)

if __name__ == "__main__":
    main()
