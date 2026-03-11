#!/usr/bin/env python3
"""
Generate newcomer inflow summary tables:
  - out/newcomer_inflow_summary.csv   (totals by distribution and owner type)
  - out/top20_packages_newcomers.csv  (top 20 packages by newcomer count)
"""

import csv
from collections import defaultdict, Counter

INFLOW_CSV = "scripts/tables/inflow.csv"
N_WEEKS = 28
META_COLS = {'project', 'owner_type', 'distribution_type'}

# Manual classification of top 20 package owners
CLASSIFICATION = {
    'ros-planning/navigation2':         'ROS org',
    'autowarefoundation/autoware_core': 'Non-profit',
    'foxglove/foxglove-sdk':            'Company',
    'ros-controls/ros2_controllers':    'ROS org',
    'borglab/gtsam':                    'Research lab',
    'IntelRealSense/librealsense':      'Company',
    'facontidavide/PlotJuggler':        'Individual',
    'ros2/rclcpp':                      'ROS org',
    'luxonis/depthai-core':             'Company',
    'ros2/rclpy':                       'ROS org',
    'ros-controls/ros2_control':        'ROS org',
    'ros-planning/moveit2':             'ROS org',
    'ros2/rviz':                        'ROS org',
    'ros2/rmw_zenoh':                   'ROS org',
    'stack-of-tasks/pinocchio':         'Research lab',
    'aerostack2/aerostack2':            'Research lab',
    'ros2/rosbag2':                     'ROS org',
    'eProsima/Fast-DDS':                'Company',
    'BehaviorTree/BehaviorTree.CPP':    'Individual',
    'ros2/ros2cli':                     'ROS org',
    'ros2/geometry2':                   'ROS org',
    'ompl/ompl':                        'Research lab',
}


def main():
    total = 0
    by_distro = defaultdict(int)
    by_owner = defaultdict(int)
    multi_org = 0
    repos_by_distro = defaultdict(int)
    repos_by_owner = defaultdict(int)
    repos_multi_org = 0
    repo_totals = defaultdict(int)

    with open(INFLOW_CSV) as f:
        reader = csv.DictReader(f)
        week_cols = [c for c in reader.fieldnames if c not in META_COLS]
        for row in reader:
            project = row['project']
            distro = row.get('distribution_type', 'unknown')
            owner = row.get('owner_type', 'unknown')
            row_total = sum(int(row[k]) for k in week_cols if row[k].strip().lstrip('-').isdigit())
            total += row_total
            by_distro[distro] += row_total
            by_owner[owner] += row_total
            repos_by_distro[distro] += 1
            repos_by_owner[owner] += 1
            repo_totals[project] = row_total
            if distro == 'multi-distro' and owner == 'Organization':
                multi_org += row_total
                repos_multi_org += 1

    # ── newcomer_inflow_summary.csv ──────────────────────────────────────────
    rows = [
        {'group': 'Overall', 'category': 'All',
         'n_repos': sum(repos_by_distro.values()),
         'total_newcomers': total,
         'avg_per_week': round(total / N_WEEKS, 1),
         'n_weeks': N_WEEKS},
    ]
    for k, v in sorted(by_distro.items(), key=lambda x: -x[1]):
        rows.append({'group': 'Distribution', 'category': k,
                     'n_repos': repos_by_distro[k],
                     'total_newcomers': v,
                     'avg_per_week': round(v / N_WEEKS, 1),
                     'n_weeks': N_WEEKS})
    for k, v in sorted(by_owner.items(), key=lambda x: -x[1]):
        rows.append({'group': 'Owner Type', 'category': k,
                     'n_repos': repos_by_owner[k],
                     'total_newcomers': v,
                     'avg_per_week': round(v / N_WEEKS, 1),
                     'n_weeks': N_WEEKS})
    rows.append({'group': 'Combined', 'category': 'multi-distro + Organization',
                 'n_repos': repos_multi_org,
                 'total_newcomers': multi_org,
                 'avg_per_week': round(multi_org / N_WEEKS, 1),
                 'n_weeks': N_WEEKS})

    with open('out/newcomer_inflow_summary.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['group', 'category', 'n_repos', 'total_newcomers', 'avg_per_week', 'n_weeks'])
        writer.writeheader()
        writer.writerows(rows)
    print("✅ Saved: out/newcomer_inflow_summary.csv")

    # ── top20_packages_newcomers.csv ─────────────────────────────────────────
    top20 = sorted(repo_totals.items(), key=lambda x: -x[1])[:20]
    top20_rows = []
    for rank, (proj, count) in enumerate(top20, 1):
        top20_rows.append({
            'rank': rank,
            'project': proj,
            'newcomers_28w': count,
            'category': CLASSIFICATION.get(proj, 'Unknown')
        })

    with open('out/top20_packages_newcomers.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'project', 'newcomers_28w', 'category'])
        writer.writeheader()
        writer.writerows(top20_rows)
    print("✅ Saved: out/top20_packages_newcomers.csv")

    cat_counts = Counter(r['category'] for r in top20_rows)
    print("\nTop 20 breakdown:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:<15} {count} ({count/20*100:.0f}%)")


if __name__ == "__main__":
    main()
