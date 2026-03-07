#!/usr/bin/env python3
"""
Generate ROS package statistics table by distribution.
"""

import csv
import os
from collections import defaultdict

def main():
    # Load all packages
    all_packages_by_distro = defaultdict(int)
    total_all_packages = 0
    
    with open("out/mapping_packages_to_github.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            distro = row.get('ros_distro', '').strip()
            all_packages_by_distro[distro] += 1
            total_all_packages += 1
    
    # Load packages on GitHub
    github_packages_by_distro = defaultdict(int)
    total_github_packages = 0
    
    with open("out/diagnostics/resolved_ok.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            distro = row.get('ros_distro', '').strip()
            github_packages_by_distro[distro] += 1
            total_github_packages += 1
    
    # Load unique repos per distribution
    repos_by_distro = defaultdict(int)
    total_repos = 0
    
    if os.path.exists("out/repos/github_repos_unique_by_distro.csv"):
        with open("out/repos/github_repos_unique_by_distro.csv", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                distro = row.get('ros_distro', '').strip()
                if distro:
                    repos_by_distro[distro] += 1
                    total_repos += 1
    
    # Load filtered repos by distribution
    filtered_repos_by_distro = defaultdict(int)
    total_filtered_repos = 0
    
    filtered_repo_names = set()
    if os.path.exists("out/filtered_repo_dataset.csv"):
        with open("out/filtered_repo_dataset.csv", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_name = row.get('full_name', '').strip()
                if full_name:
                    filtered_repo_names.add(full_name)
                    total_filtered_repos += 1
    
    # Count filtered repos per distribution
    if os.path.exists("out/repos/github_repos_unique_by_distro.csv"):
        with open("out/repos/github_repos_unique_by_distro.csv", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                distro = row.get('ros_distro', '').strip()
                full_name = row.get('full_name', '').strip()
                if distro and full_name in filtered_repo_names:
                    filtered_repos_by_distro[distro] += 1
    
    # Build table
    all_distros = sorted(set(all_packages_by_distro.keys()))
    rows_data = []
    
    for distro in all_distros:
        total = all_packages_by_distro[distro]
        github = github_packages_by_distro[distro]
        repos = repos_by_distro[distro]
        filtered_repos = filtered_repos_by_distro[distro]
        pct = (github / total * 100) if total > 0 else 0
        
        rows_data.append({
            'distribution': distro,
            'total_packages': total,
            'packages_on_github': github,
            'not_on_github': total - github,
            'github_percentage': f"{pct:.1f}%",
            'unique_repositories': repos,
            'repos_after_exclusion': filtered_repos,
        })
    
    # Total row
    total_not_github = total_all_packages - total_github_packages
    total_pct = (total_github_packages / total_all_packages * 100) if total_all_packages > 0 else 0
    
    rows_data.append({
        'distribution': 'TOTAL',
        'total_packages': total_all_packages,
        'packages_on_github': total_github_packages,
        'not_on_github': total_not_github,
        'github_percentage': f"{total_pct:.1f}%",
        'unique_repositories': total_repos,
        'repos_after_exclusion': total_filtered_repos,
    })
    
    # Print table
    print(f"\n{'Distribution':<15} {'Total Pkg':<12} {'On GitHub':<12} {'Not GitHub':<12} {'GitHub %':<10} {'Unique Repos':<14} {'After Exclusion':<16}")
    print("-" * 95)
    for row in rows_data:
        print(f"{row['distribution']:<15} {row['total_packages']:<12} {row['packages_on_github']:<12} {row['not_on_github']:<12} {row['github_percentage']:<10} {row['unique_repositories']:<14} {row['repos_after_exclusion']:<16}")
    
    # Write CSV
    os.makedirs("out", exist_ok=True)
    
    with open("out/ros_package_statistics.csv", 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['distribution', 'total_packages', 'packages_on_github', 'not_on_github', 'github_percentage', 'unique_repositories', 'repos_after_exclusion']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_data)
    
    print(f"\n✅ Saved to: out/ros_package_statistics.csv")

if __name__ == "__main__":
    main()
