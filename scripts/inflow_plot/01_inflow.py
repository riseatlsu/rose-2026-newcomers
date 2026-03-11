#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ =  "Elijah Phifer"
__contact__ = "elijah.phifer@lsu.edu"

import os
import csv
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from collections import Counter

class NewcomersInflow():
    def __init__(self, dataset_folder, csv_folder, min_age_months, filtered_repos_csv):
        self.csv_folder = csv_folder
        self.dataset_folder = dataset_folder
        self.min_age_months = min_age_months
        self.filtered_repos_csv = filtered_repos_csv
        
        if not filtered_repos_csv or not os.path.exists(filtered_repos_csv):
            print(f"ERROR: Filtered repos CSV not found: {filtered_repos_csv}")
            return
        
        # Load projects from filtered CSV and check their ages
        projects = self.load_and_filter_projects()
        self.repo_metadata = self._load_repo_metadata()
        
        if not projects:
            print("No projects with valid commits found after filtering!")
            return
        
        # Fixed 28-week window ending on the reference date March 3, 2026 (x-axis: -27 to 0)
        self.end_date = datetime(2026, 3, 3).date()
        self.start_date = self.end_date - timedelta(weeks=27)
        print(f"\nCounting newcomers from: {self.start_date} to {self.end_date} (28-week window)\n")
        
        # Track latest commit across all repos
        self.latest_commit_date = None
        
        weekly_series = self.get_weekly_series(projects)
        
        print(f"\nExporting weekly inflow from {self.start_date} to {self.end_date}...")
        
        # Export weekly inflow
        self.export_newcomers_inflow(weekly_series)
        
        # Export monthly inflow
        # self.export_monthly_inflow(weekly_series, weekly_min, weekly_max)
    
    def load_and_filter_projects(self):
        """
        Load repositories from the filtered CSV.
        All repos in filtered_repo_dataset.csv are assumed mature.
        Returns list of project info dicts with folder paths and first commit dates.
        """
        # Determine the data folder path
        if self.dataset_folder.endswith('ros_robotics_data'):
            ros_data_folder = self.dataset_folder
        else:
            ros_data_folder = os.path.join(self.dataset_folder, 'ros_robotics_data')
        
        print(f"Reading filtered repositories from: {self.filtered_repos_csv}")
        print(f"Looking for commit data in: {os.path.abspath(ros_data_folder)}\n")
        
        if not os.path.exists(ros_data_folder):
            print(f"ERROR: Data directory does not exist: {os.path.abspath(ros_data_folder)}")
            return []
        
        projects = []
        repos_in_csv = 0
        repos_with_commits = 0
        
        try:
            with open(self.filtered_repos_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    repos_in_csv += 1
                    
                    # Get owner and repo name
                    owner = row.get('Owner', '').strip()
                    repo_name = row.get('Name', '').strip()
                    
                    if not owner or not repo_name:
                        continue
                    
                    full_name = f"{owner}/{repo_name}"

                    # Alert if repository is younger than the minimum age threshold
                    try:
                        repo_age = int(row.get('Repository age (months)', '') or -1)
                        if 0 <= repo_age < self.min_age_months:
                            print(f"  ⚠️  YOUNG REPO: {full_name} is only {repo_age} month(s) old "
                                  f"(minimum is {self.min_age_months} months)")
                    except (ValueError, TypeError):
                        pass

                    # Build path to commits.json
                    folder_name = f"{owner}__{repo_name}"
                    project_path = os.path.join(ros_data_folder, folder_name)
                    commits_file = os.path.join(project_path, 'commits.json')
                    
                    # Check if commits.json exists
                    if not os.path.isfile(commits_file):
                        print(f"  Warning: {full_name} - no commits.json found, excluding")
                        continue
                    
                    # Get first commit date
                    first_commit_date = self.get_first_commit_date(commits_file)
                    
                    if not first_commit_date:
                        print(f"  Warning: {full_name} - no valid commits found, excluding")
                        continue
                    
                    repos_with_commits += 1
                    projects.append({
                        'full_name': full_name,
                        'folder_path': project_path,
                        'first_commit_date': first_commit_date
                    })
        
        except Exception as e:
            print(f"ERROR reading filtered CSV: {e}")
            return []
        
        print(f"\nFiltering Summary:")
        print(f"  Repositories in filtered CSV: {repos_in_csv}")
        print(f"  Repositories with commit data: {repos_with_commits}")
        print(f"  Repositories included: {len(projects)}")
        
        return projects

    def _load_repo_metadata(self):
        """
        Load owner_type and distribution_type for each repo from filtered_repo_dataset.csv.
        Returns a dict mapping 'owner/name' -> {'owner_type': ..., 'distribution_type': ...}.
        """
        metadata = {}
        if not self.filtered_repos_csv or not os.path.exists(self.filtered_repos_csv):
            return metadata
        
        try:
            with open(self.filtered_repos_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    owner = row.get('Owner', '').strip()
                    name = row.get('Name', '').strip()
                    if not owner or not name:
                        continue
                    project_key = f"{owner}/{name}"
                    
                    owner_type = row.get('owner_type', 'unknown').strip()
                    if owner_type not in ['User', 'Organization']:
                        owner_type = 'unknown'
                    
                    distros = row.get('distros_present', '').strip()
                    if distros and '|' in distros:
                        distribution_type = 'multi-distro'
                    elif distros:
                        distribution_type = f"{distros}-only"
                    else:
                        distribution_type = 'unknown'
                    
                    metadata[project_key] = {
                        'owner_type': owner_type,
                        'distribution_type': distribution_type
                    }
        except Exception as e:
            print(f"Warning: Could not load repo metadata: {e}")
        
        return metadata

    def get_first_commit_date(self, commits_file_path):
        """
        Find the first (earliest) commit date in a repository.
        Returns None if no commits found.
        """
        try:
            with open(commits_file_path, 'r', encoding='utf-8') as f:
                commits_data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read {commits_file_path}: {e}")
            return None
        
        # Extract commits from the data field if present
        if isinstance(commits_data, dict) and 'data' in commits_data:
            commits_list = commits_data['data']
        elif isinstance(commits_data, list):
            commits_list = commits_data
        else:
            return None
        
        earliest_date = None
        
        for commit in commits_list:
            # Handle multiple formats:
            # 1. New simplified format: {date: "...", author: "..."}
            # 2. Old nested format: {commit: {author: {date: "..."}}}
            # 3. Alternative format: {author_date: "..."}
            commit_date_str = None
            
            if 'date' in commit:
                commit_date_str = commit['date']
            elif 'author_date' in commit:
                commit_date_str = commit['author_date']
            elif 'commit' in commit and 'author' in commit['commit']:
                commit_date_str = commit['commit']['author'].get('date')
            
            if commit_date_str:
                try:
                    commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ').date()
                    
                    if earliest_date is None or commit_date < earliest_date:
                        earliest_date = commit_date
                except Exception:
                    continue
        
        return earliest_date

    def get_weekly_series(self, projects):
        weekly_series = {}

        for project in projects:
            project_weekly_series = self.get_project_weekly_series(project['folder_path'])
            weekly_series[project['full_name']] = project_weekly_series

        return weekly_series

    def get_project_weekly_series(self, folder):
        commits_file_path = os.path.join(folder, 'commits.json')
        
        if not os.path.isfile(commits_file_path):
            return Counter()
        
        try:
            with open(commits_file_path, 'r', encoding='utf-8') as f:
                commits_data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read {commits_file_path}: {e}")
            return Counter()
        
        # Extract commits from the data field if present
        if isinstance(commits_data, dict) and 'data' in commits_data:
            commits_list = commits_data['data']
        elif isinstance(commits_data, list):
            commits_list = commits_data
        else:
            print(f"Warning: Unexpected format in {commits_file_path}")
            return Counter()
        
        newcomers_list = []
        entry_list = []

        for commit in commits_list:
            # Handle multiple formats:
            # 1. New simplified format: {author: "...", date: "..."}
            # 2. Old nested format: {commit: {author: {name: "...", date: "..."}}}
            # 3. Alternative format: {author_name: "...", author_date: "..."}
            newcomer = None
            commit_date = None
            
            if 'author' in commit and 'date' in commit:
                newcomer = commit['author']
                commit_date = commit['date']
            elif 'author_name' in commit and 'author_date' in commit:
                newcomer = commit['author_name']
                commit_date = commit['author_date']
            elif 'commit' in commit and 'author' in commit['commit']:
                newcomer = commit['commit']['author'].get('name')
                commit_date = commit['commit']['author'].get('date')

            if commit_date is not None and newcomer is not None:
                try:
                    commit_date = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').date()
                    
                    # Track the latest commit date
                    if self.latest_commit_date is None or commit_date > self.latest_commit_date:
                        self.latest_commit_date = commit_date
                    
                    # Only count commits from the start date onward
                    if commit_date >= self.start_date:
                        if newcomer not in newcomers_list:
                            newcomers_list.append(newcomer)
                            entry_list.append(commit_date)
                except Exception as e:
                    continue

        ordered_entry_list = Counter(entry_list)

        return ordered_entry_list

    def get_number_of_weeks(self, weekly_series):
        weekly_max = None
        weekly_min = None

        for series in weekly_series.values():
            if series:
                for date in series.keys():
                    if weekly_min is None or date < weekly_min:
                        weekly_min = date
                    if weekly_max is None or date > weekly_max:
                        weekly_max = date

        return weekly_min, weekly_max

    def export_newcomers_inflow(self, weekly_series):
        # Use the fixed 6-month window
        weekly_min = self.start_date
        weekly_max = self.end_date
        
        fieldnames = []
        step = timedelta(days=1)
        current_date = weekly_min

        while current_date <= weekly_max:
            week = (current_date.isocalendar()[1], current_date.year)
            if not week in fieldnames:
                fieldnames.append(week)
            current_date += step
        
        print(f"Exporting inflow data for {len(fieldnames)} weeks (from week {fieldnames[0]} to week {fieldnames[-1]})...")
        
        with open(self.csv_folder + '/inflow.csv', 'w', newline='', encoding='utf-8') as inflow_file:
            writer = csv.DictWriter(inflow_file, fieldnames=['project'] + fieldnames + ['owner_type', 'distribution_type'])
            writer.writeheader()
        
        for project in weekly_series:
            inflow = {}
            inflow['project'] = project

            for week in fieldnames:
                number_of_newcomers = 0
                # Look through all entry dates to find matches for this week
                for entry_date, count in weekly_series[project].items():
                    entry_week = (entry_date.isocalendar()[1], entry_date.year)
                    if entry_week == week:
                        number_of_newcomers += count
                inflow[week] = number_of_newcomers

            meta = self.repo_metadata.get(project, {})
            inflow['owner_type'] = meta.get('owner_type', 'unknown')
            inflow['distribution_type'] = meta.get('distribution_type', 'unknown')

            with open(self.csv_folder + '/inflow.csv', 'a', newline='', encoding='utf-8') as inflow_file:
                writer = csv.DictWriter(inflow_file, fieldnames=['project'] + fieldnames + ['owner_type', 'distribution_type'])
                writer.writerow(inflow)
        
        print(f"Inflow data saved to: {self.csv_folder}/inflow.csv")
    
    
if __name__ == '__main__':
    # Use paths relative to script location, not current working directory
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Point to scripts/data folder which contains commits.json files (../data from scripts/clustering/)
    dataset_folder = os.path.join(script_dir, 'data')
    # Output to tables subfolder within clustering folder
    csv_folder = os.path.join(script_dir, 'tables')
    # Use the filtered repos dataset (509 repos after exclusion criteria)
    filtered_repos_csv = os.path.join(script_dir, '..', 'out', 'filtered_repo_dataset.csv')
    
    # Minimum repository age in months (repositories must have first commit at least this many months ago)
    min_age_months = 6
    
    # Create output folder if it doesn't exist
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
        print(f"Created output folder: {csv_folder}\n")

    print(f"Filtered repos CSV: {filtered_repos_csv}")
    print(f"Commit data folder: {dataset_folder}")
    print(f"Output folder: {csv_folder}")
    print(f"Minimum repository age: {min_age_months} months\n")
    
    inflow = NewcomersInflow(dataset_folder, csv_folder, min_age_months, filtered_repos_csv)
