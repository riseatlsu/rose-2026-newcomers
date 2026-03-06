# Replication Package
Welcome to the replication package of the paper entitled "Are We Welcome Here? A Preliminary Study of Newcomer Onboarding in the ROS Ecosystem"

# Repository Structure 
Our package is divided into folders and it is organized as follows:
- [**scripts**](scripts): This folder contains the complete data processing pipeline used to collect and analyze ROS repository data. It includes numbered scripts (00-14) that download ROS index data, build package-to-repo mappings, extract repository features, and generate the final datasets used in our analysis.
- [**data**](data): If you are looking for the data we have collected from GitHub repositories, this is the folder where it is located. This folder contains per-repository snapshots including metadata, commits, contributors, pull requests, issues, and community indicators (README, CONTRIBUTING, CODE_OF_CONDUCT files).
- [**tables**](tables): This folder contains all the summarized results and statistics from our analysis, including inflow metrics and repository overlap tables.
- [**figs**](figs): This folder contains all the figures and visualizations generated from our analysis, including plots of inflow patterns and documentation metrics.

# Running the Replication Pipeline
If you want to replicate our data collection and analysis, you can run the complete pipeline using:

```bash
pip install -r requirements.txt
echo "GITHUB_TOKEN=your_github_token_here" > .env
python scripts/run_all.py
```

The pipeline analyzes ROS packages across three distributions (ROS 2 Humble, Jazzy, and Kilted) and generates the final repository dataset at `out/final_repo_dataset.csv`. Individual scripts can also be run independently if you want to execute specific steps of the pipeline.

# Contact
If you have any questions or are interested in contributing to this project, please don't hesitate to contact us:

* Juliana Freitas (jfreit4@lsu.edu)
* Elijah Phifer (ephife3@lsu.edu)
* Author Name (email@institution.edu)
