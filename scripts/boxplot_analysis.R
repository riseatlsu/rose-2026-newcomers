# ============================================================
# Configuration
# ============================================================

# Input file
input_file <- "out/filtered_repo_dataset.csv"

# Output folder
output_dir <- "figs"

# Create output folder if it does not exist
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# EPS figure size
# 270 x 140 px equivalent -> 2.7 x 1.4 inches
fig_width <- 270 / 100
fig_height <- 140 / 100

# ============================================================
# Load dataset
# ============================================================

final_dataset <- read.csv(input_file)

# ============================================================
# Quick statistics (optional checks)
# ============================================================

summary(final_dataset$`Average number of newcomers per month`)

mean(
  final_dataset$`Average number of newcomers per month`[
    final_dataset$owner_type == "Organization"
  ],
  na.rm = TRUE
)

mean(
  final_dataset$`Average number of newcomers per month`[
    final_dataset$owner_type == "User"
  ],
  na.rm = TRUE
)

# ============================================================
# Plot functions
# ============================================================

plot_horizontal_boxplot <- function(data, file_name) {
  
  postscript(
    file = file.path(output_dir, file_name),
    horizontal = FALSE,
    onefile = FALSE,
    paper = "special",
    width = fig_width,
    height = fig_height
  )
  
  par(mar = c(2,2,1,1), cex.axis = 1.8, cex.lab = 1.8)
  
  boxplot(
    na.omit(data),
    horizontal = TRUE,
    col = "lightgray",
    lwd = 3,
    whisklwd = 3,
    staplelwd = 3,
    outline = FALSE,
    xlab = ""
  )
  
  box(lwd = 3)
  axis(side = 1, lwd = 3, labels = FALSE)
  
  dev.off()
}

plot_vertical_boxplot <- function(data, file_name) {
  
  postscript(
    file = file.path(output_dir, file_name),
    horizontal = FALSE,
    onefile = FALSE,
    paper = "special",
    width = fig_width,
    height = fig_height
  )
  
  par(mar = c(2,2,1,1), cex.axis = 1.8, cex.lab = 1.8)
  
  boxplot(
    na.omit(data),
    col = "lightgray",
    lwd = 3,
    whisklwd = 3,
    staplelwd = 3,
    outline = FALSE,
    ylab = ""
  )
  
  box(lwd = 3)
  axis(side = 2, lwd = 3, labels = FALSE)
  
  dev.off()
}

# ============================================================
# Export plots
# ============================================================

# Contributors
plot_horizontal_boxplot(
  final_dataset$contributors_count,
  "num_contributors.eps"
)

# Commits
plot_horizontal_boxplot(
  final_dataset$commits_count,
  "num_commits.eps"
)

# Repository age
plot_horizontal_boxplot(
  final_dataset$`Repository.age..months.`,
  "age_in_months.eps"
)

# Forks
plot_horizontal_boxplot(
  final_dataset$Number.of.forks,
  "num_forks.eps"
)

# Newcomers per month
plot_vertical_boxplot(
  final_dataset$Average.number.of.newcomers.per.month,
  "avg_newcomers_per_month.eps"
)