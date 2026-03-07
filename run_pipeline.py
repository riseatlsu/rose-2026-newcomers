#!/usr/bin/env python3
"""
Master runner for the entire newcomers-ros pipeline.

Orchestrates:
1. Data collection via pipeline scripts (00-11)
2. Visualization generation

Run from project root: python run_pipeline.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Get paths
SCRIPT_DIR = Path(__file__).parent / "scripts"
PROJECT_ROOT = Path(__file__).parent
DESCRIPTIVE_STATS_DIR = PROJECT_ROOT / "scripts" / "descriptive_stats"

# Define pipeline stages
PIPELINE_SCRIPTS = [
    "00_download_ros_index_json.py",
    "01_build_mapping_from_rosdistro.py",
    "02_join_index_with_rosdistro.py",
    "03_validate_and_stats.py",
    "04_analyze_resolved_packages.py",
    "05_fill_missing_from_index_html.py",
    "06_diagnose_unresolved.py",
    "07_extract_unique_repos.py",
    "08_repo_overlap_table.py",
    "09_extract_repo_features_and_commits.py",
    "10_build_final_repo_dataset.py",
    "11_apply_exclusion_criteria.py",
]

# ============================================================================
# UTILITIES
# ============================================================================

def print_section(title, level=1):
    """Print a formatted section header."""
    if level == 1:
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    elif level == 2:
        print("\n" + "-" * 80)
        print(f"  {title}")
        print("-" * 80)

def print_step(step_num, total, script_name):
    """Print a step indicator."""
    print(f"\n[{step_num}/{total}] {script_name}")
    print("   " + "─" * 76)

def print_status(status, message):
    """Print a status message."""
    status_map = {
        'ok': '✅',
        'error': '❌',
        'skip': '⊝',
        'running': '▶',
        'info': 'ℹ',
    }
    symbol = status_map.get(status, '•')
    print(f"{symbol}  {message}")

def run_script(script_path, description=""):
    """Run a Python script and return success status."""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print_status('error', f"Exception: {e}")
        return False

# ============================================================================
# PIPELINE STAGES
# ============================================================================

def run_data_pipeline(skip=False):
    """Run the main data collection pipeline (scripts 00-11)."""
    print_section("STAGE 1: DATA PIPELINE (Scripts 00-11)", level=1)
    
    if skip:
        print_status('skip', "Skipping data pipeline (already completed)")
        return True
    
    print_status('info', f"Running {len(PIPELINE_SCRIPTS)} data processing scripts")
    print_status('info', f"Estimated time: 30-60 minutes (depends on GitHub API rate limits)")
    
    failed = []
    successful = []
    start_time = time.time()
    
    for idx, script in enumerate(PIPELINE_SCRIPTS, 1):
        script_path = SCRIPT_DIR / script
        
        if not script_path.exists():
            print_status('skip', f"Script not found: {script}")
            continue
        
        print_step(idx, len(PIPELINE_SCRIPTS), script)
        
        if run_script(script_path):
            print_status('ok', f"Completed successfully")
            successful.append(script)
        else:
            print_status('error', f"Failed with non-zero exit code")
            failed.append(script)
    
    elapsed = (time.time() - start_time) / 60
    
    print_section(f"Data Pipeline Summary ({elapsed:.1f} minutes)", level=2)
    print_status('info', f"Successful: {len(successful)}/{len(PIPELINE_SCRIPTS)}")
    
    if failed:
        print_status('error', "Failed scripts:")
        for script in failed:
            print(f"           - {script}")
        return False
    
    print_status('ok', "All data pipeline scripts completed successfully!")
    return True

def run_visualizations(skip=False):
    """Run all visualization generation scripts via run_all_plots.py."""
    print_section("STAGE 2: VISUALIZATION GENERATION", level=1)
    
    if skip:
        print_status('skip', "Skipping visualizations (already generated)")
        return True
    
    # Run the master visualization script
    script_file = DESCRIPTIVE_STATS_DIR / "run_all_plots.py"
    
    if not script_file.exists():
        print_status('error', f"Script not found: {script_file}")
        return False
    
    print_status('info', "Running all visualization scripts...")
    start_time = time.time()
    
    if run_script(script_file):
        elapsed = (time.time() - start_time) / 60
        print_section(f"Visualization Summary ({elapsed:.1f} minutes)", level=2)
        print_status('ok', "All visualizations generated successfully")
        return True
    else:
        print_section("Visualization Summary", level=2)
        print_status('error', "Visualization generation failed")
        return False

# ============================================================================
# MAIN
# ============================================================================

def print_welcome():
    """Print welcome message."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  NEWCOMERS-ROS PIPELINE - Complete Analysis & Visualization Generator".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Orchestrates: Data Collection → Visualization".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

def print_summary(data_ok, viz_ok, total_time):
    """Print final summary."""
    print_section("FINAL SUMMARY", level=1)
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time: {total_time / 60:.1f} minutes ({total_time / 3600:.1f} hours)")
    
    print("\n  Pipeline Results:")
    print_status('ok' if data_ok else 'error', "Stage 1: Data Pipeline")
    print_status('ok' if viz_ok else 'error', "Stage 2: Visualizations")
    
    if data_ok and viz_ok:
        print("\n" + "=" * 80)
        print_status('ok', "ALL STAGES COMPLETED SUCCESSFULLY! 🎉")
        print("=" * 80)
        print_status('info', "Output files are in:")
        print(f"           - {PROJECT_ROOT / 'out'}")
        print(f"           - {PROJECT_ROOT / 'scripts' / 'descriptive_stats' / 'plots'}")
    else:
        print("\n" + "=" * 80)
        print_status('error', "SOME STAGES FAILED - Check errors above")
        print("=" * 80)

def main():
    print_welcome()
    
    # Get command line options
    skip_data = '--skip-data' in sys.argv
    skip_viz = '--skip-viz' in sys.argv
    skip_all_data = '--skip-all-data' in sys.argv
    
    if skip_all_data:
        skip_data = skip_viz = True
    
    print_status('info', "Command line options:")
    if skip_data:
        print("           - Skipping data pipeline")
    if skip_viz:
        print("           - Skipping visualizations")
    if not (skip_data or skip_viz):
        print("           - Running all stages (full pipeline)")
    
    start_time = time.time()
    
    # Run stages
    data_ok = run_data_pipeline(skip=skip_data)
    viz_ok = run_visualizations(skip=skip_viz)
    
    total_time = time.time() - start_time
    
    # Print summary
    print_summary(data_ok, viz_ok, total_time)
    
    # Exit with appropriate code
    sys.exit(0 if (data_ok and viz_ok) else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print_status('error', "Pipeline interrupted by user")
        print("=" * 80)
        sys.exit(1)
