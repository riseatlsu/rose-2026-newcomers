#!/usr/bin/env python3
"""
Global configuration for newcomers-ros project.
Centralized settings for paths, colors, and parameters.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = PROJECT_ROOT / "scripts" / "data" / "ros_robotics_data"
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "out"

# Input datasets
FILTERED_REPO_CSV = OUTPUT_DIR / "filtered_repo_dataset.csv"
COMMIT_TYPES_CSV = OUTPUT_DIR / "all_commits_spreadsheet.csv"

# Output paths for plots (in descriptive_stats folder)
PLOTS_DIR = PROJECT_ROOT / "scripts" / "descriptive_stats" / "plots"
COMMIT_TYPES_VIZ_DIR = PLOTS_DIR / "commit_types"
LABEL_VIZ_DIR = PLOTS_DIR / "label_analysis"

# Create directories if they don't exist
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
COMMIT_TYPES_VIZ_DIR.mkdir(parents=True, exist_ok=True)
LABEL_VIZ_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# VISUALIZATION STYLE CONFIGURATION
# ============================================================================

# Paper-style colors (consistent across visualizations)
COLORS = {
    'code': '#3498DB',      # Blue
    'docs': '#E67E22',      # Orange
    'config': '#27AE60',    # Green
    'assets': '#E74C3C',    # Red
    'other': '#95A5A6',     # Gray
    'with_label': '#3498DB', # Blue for "with" labels
    'without_label': '#E74C3C', # Red for "without" labels
}

# Figure sizes (width, height)
FIGSIZE = {
    'small': (6, 3.8),      # Single metric chart
    'medium': (10, 3.8),    # Stacked bars
    'large': (11, 3.8),     # Side-by-side charts
    'tall': (8, 6),         # Portrait layout
}

# Plot parameters
PLOT_PARAMS = {
    'dpi': 300,
    'format': 'png',
    'bbox_inches': 'tight',
    'facecolor': 'white',
    'fontsize_title': 9,
    'fontsize_label': 9,
    'fontsize_tick': 8,
    'grid_alpha': 0.3,
    'alpha_bar': 0.9,
    'linewidth_edge': 0.5,
    'bar_width': 0.6,
}

# ============================================================================
# DATA PROCESSING CONFIGURATION
# ============================================================================

# Top N repos to display in stacked bars
TOP_N_REPOS = 15

# Repository name mapping (directory names to full names)
REPO_NAME_MAPPING = {
    'ros-planning__moveit2': 'moveit/moveit2',
    'realsenseai__librealsense': 'realsenseai/librealsense',
    'ros-navigation__navigation2': 'ros-navigation/navigation2',
    'borglab__gtsam': 'borglab/gtsam',
    'ros2__rviz': 'ros2/rviz',
    'ros-visualization__rviz__python_qt_binding': 'ros-visualization/python_qt_binding',
    'ros2__geometry2': 'ros2/geometry2',
    'PX4__PX4-Autopilot': 'PX4/PX4-Autopilot',
    'ros2__demos': 'ros2/demos',
    'ros2__rclcpp': 'ros2/rclcpp',
    'StanfordASL__AutonomousBulldozer': 'StanfordASL/AutonomousBulldozer',
    'husarnet__husarnet': 'husarnet/husarnet',
    'ros-realtime__linux-ml': 'ros-realtime/linux-ml',
    'ros-teleop__teleop_twist_keyboard': 'ros-teleop/teleop_twist_keyboard',
    'ros-drivers__usb_cam': 'ros-drivers/usb_cam',
    'ros-drivers__stage': 'ros-drivers/stage',
    'ros-drivers__ros_astra_camera': 'ros-drivers/ros_astra_camera',
    'ros-drivers__pointcloud_to_laserscan': 'ros-drivers/pointcloud_to_laserscan',
    'ros-drivers__BLUESEA2': 'ros-drivers/BLUESEA2',
    't-thanh__mobile_robot_description': 't-thanh/mobile_robot_description',
    'ros2__sros2': 'ros2/sros2',
    'ros-perception__perception_pcl': 'ros-perception/perception_pcl',
}

# ============================================================================
# COMMIT TYPE CATEGORIES
# ============================================================================

COMMIT_TYPES = ['code', 'docs', 'config', 'assets', 'other']
COMMIT_TYPE_LABELS = {
    'code': 'Code',
    'docs': 'Docs',
    'config': 'Config',
    'assets': 'Assets',
    'other': 'Other',
}


if __name__ == "__main__":
    print("Configuration loaded successfully")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Data dir: {DATA_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Visualizations dir: {VISUALIZATIONS_DIR}")
