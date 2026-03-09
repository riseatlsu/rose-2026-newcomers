library(readxl)

# Load datasets
final_dataset <- read_excel("GitHub/rose-2026-newcomers/final_dataset.xlsx")
# Load commits dataset (CSV)
all_commits_spreadsheet <- read.csv("GitHub/rose-2026-newcomers/all_commits.csv")

# Count commits per type
commit_counts <- table(all_commits_spreadsheet$commit_type)

# Remove NA if present
commit_counts <- commit_counts[!is.na(names(commit_counts))]

# Sort counts
commit_counts <- sort(commit_counts)

# Plot parameters
par(mar = c(4, 2, 1, 1), mgp = c(1.75, 0.5, 0), lwd = 2)

# Get bar positions
bar_positions <- barplot(
  commit_counts,
  horiz = TRUE,
  plot = FALSE
)

# Empty plot region
plot(
  NA,
  NA,
  xlim = c(0, max(commit_counts) * 1.1),
  ylim = range(bar_positions) + c(-0.7, 0.7),
  xlab = "Number of Commits",
  ylab = "",
  axes = FALSE,
  xaxs = "i",
  yaxs = "i"
)

# Grid
abline(v = pretty(c(0, max(commit_counts))), col = "lightgray", lwd = 1)

# Colors
commit_colors <- c(
  "#4E79A7",
  "#59A14F",
  "#F28E2B",
  "#E15759",
  "#76B7B2",
  "#B07AA1"
)

# Draw bars
barplot(
  commit_counts,
  horiz = TRUE,
  col = rep(commit_colors, length.out = length(commit_counts)),
  border = "black",
  lwd = 3,
  las = 1,
  axes = FALSE,
  add = TRUE
)

# Box and axis
box(lwd = 2)

axis(
  side = 1,
  at = pretty(c(0, max(commit_counts))),
  lwd = 2
)
# Select boolean columns
docs <- final_dataset[, c(
  "has_readme",
  "has_contributing",
  "has_code_of_conduct",
  "has_pr_template",
  "has_issue_template",
  "has_newcomer_labels"
)]

# Count repositories containing each document
doc_counts <- colSums(docs, na.rm = TRUE)

# Convert to percentage
doc_percent <- (doc_counts / nrow(final_dataset)) * 100

# Labels
names(doc_percent) <- c(
  "Readme",
  "Contributing",
  "Code of Conduct",
  "Pull Request Template",
  "Issue Template",
  "Labels for Newcomers"
)

# Optional: order bars
doc_percent <- sort(doc_percent)

# Plot margins + axis spacing
par(mar = c(4, 10, 1, 1), mgp = c(1.75, 0.5, 0), lwd = 2)

# Get bar positions without plotting yet
bar_positions <- barplot(
  doc_percent,
  horiz = TRUE,
  plot = FALSE
)

# Create an empty plotting region that matches the barplot layout
plot(
  NA,
  NA,
  xlim = c(0, 100),
  ylim = range(bar_positions) + c(-0.7, 0.7),
  xlab = "Percentage of Projects",
  ylab = "",
  axes = FALSE,
  xaxs = "i",
  yaxs = "i"
)

# Draw grid first
abline(v = seq(0, 100, 25), col = "lightgray", lwd = 1)

bar_colors <- c(
  "#4E79A7",  # blue
  "#59A14F",  # green
  "#F28E2B",  # orange
  "#E15759",  # red
  "#76B7B2",  # teal
  "#B07AA1"   # purple
)
# Draw bars on top of the grid
barplot(
  doc_percent,
  horiz = TRUE,
  col = bar_colors,
  border = "black",
  lwd = 3,
  xlim = c(0, 100),
  las = 1,
  axes = FALSE,
  add = TRUE
)

# Box and x-axis
box(lwd = 2)

axis(
  side = 1,
  at = seq(0, 100, 25),
  labels = paste0(seq(0, 100, 25), "%"),
  lwd = 2
)