# Replication Package
Welcome to the replication package of the paper entitled "Are We Welcome Here? A Preliminary Study of Newcomer Onboarding in the ROS Ecosystem"

# Repository Structure
- [**scripts**](scripts): Complete data processing pipeline
  - **00-11**: Core data collection pipeline (download ROS index, build mappings, extract features, apply exclusion criteria)
  - **12-14**: Inflow and documentation visualization scripts
  - [**clustering**](scripts/clustering): Time series clustering analysis and package classification
  - [**descriptive_stats**](scripts/descriptive_stats): Descriptive statistics and visualization generation
  - **Utility scripts**: `generate_all_commits_spreadsheet.py`, `generate_ros_packages_statistics.py`
- [**data**](scripts/data): Per-repository data collected from GitHub (metadata, commits, contributors, issues, community files)
- [**tables**](scripts/tables): Summarized results and statistics (inflow metrics, repository overlap, cluster assignments)
- [**figs**](figs): Generated visualizations (inflow patterns, documentation metrics)
- **config.py**: Centralized configuration (paths, colors, visualization styles)
- **run_pipeline.py**: Main entry point to execute the complete pipeline

# Running the Replication Pipeline
To replicate our data collection and analysis:

```bash
pip install -r requirements.txt
echo "GITHUB_TOKEN=your_github_token_here" > .env
python run_pipeline.py
```
The pipeline analyzes ROS packages across three distributions (ROS 2 Humble, Jazzy, and Kilted) and generates the final repository dataset at `out/filtered_repo_dataset.csv`. Individual scripts can also be run independently if you want to execute specific steps of the pipeline.

# Contact
If you have any questions or are interested in contributing to this project, please don't hesitate to contact us:

* Juliana Freitas (jfreit4@lsu.edu)
* Elijah Phifer (ephife3@lsu.edu)
* Author Name (email@institution.edu)
* Felipe Fronchetti (ffronchetti@lsu.edu)

