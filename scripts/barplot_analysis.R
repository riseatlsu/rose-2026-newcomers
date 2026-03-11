# Load datasets
final_dataset <- read.csv("out/filtered_repo_dataset.csv", check.names = FALSE)
commits_spreadsheet <- read.csv("out/all_commits_spreadsheet.csv", check.names = FALSE)

# Create output folder if needed
if (!dir.exists("figs")) dir.create("figs", recursive = TRUE)

# Colors assigned by category name
category_colors <- c(
  "Code"            = "#4E79A7",
  "Configuration"   = "#59A14F",
  "Documentation"   = "#F28E2B",
  "Other"           = "#E15759",
  "Assets"          = "#76B7B2",
  "Readme"          = "#4E79A7",
  "Beginner Labels" = "#59A14F",
  "Contributing"    = "#F28E2B",
  "Pull Template"   = "#E15759",
  "Code of Conduct" = "#76B7B2",
  "Issue Template"  = "#B07AA1"
)

# ============================================================
# BARPLOT 1: Commits per type
# ============================================================

draw_barplot_commits <- function() {
  commit_counts <- table(commits_spreadsheet$commit_type)
  commit_counts <- commit_counts[!is.na(names(commit_counts))]
  name_map <- c("assets" = "Assets", "other" = "Other", "docs" = "Documentation",
                "config" = "Configuration", "code" = "Code")
  names(commit_counts) <- name_map[names(commit_counts)]
  commit_counts <- sort(commit_counts, decreasing = TRUE)  # largest first → largest at bottom
  commit_pct <- commit_counts / sum(commit_counts) * 100
  colors <- category_colors[names(commit_counts)]

  par(mar = c(4, 8.5, 1, 1), mgp = c(1.75, 0.5, 0), lwd = 2)
  bar_positions <- barplot(commit_pct, horiz = TRUE, plot = FALSE)
  plot(NA, NA, xlim = c(0, 100), ylim = range(bar_positions) + c(-0.7, 0.7),
       xlab = "Percentage of Commits", ylab = "", axes = FALSE, xaxs = "i", yaxs = "i",
       cex.lab = 0.9)
  abline(v = seq(0, 100, 25), col = "lightgray", lwd = 1)
  barplot(commit_pct, horiz = TRUE, col = colors, border = "black", lwd = 2,
          las = 1, axes = FALSE, add = TRUE, xlim = c(0, 100), cex.names = 0.9)
  text(x = commit_pct + 1, y = bar_positions, labels = as.integer(commit_counts),
       adj = 0, cex = 0.8, col = "black")
  axis(side = 1, at = seq(0, 100, 25), labels = paste0(seq(0, 100, 25), "%"), lwd = 2, cex.axis = 0.9)
  box(lwd = 2)
}

postscript("figs/barplot_commits.eps", width = 4.5, height = 2.3, paper = "special", horizontal = FALSE)
draw_barplot_commits()
dev.off()

png("figs/barplot_commits.png", width = 810, height = 415, res = 150)
draw_barplot_commits()
dev.off()


# ============================================================
# BARPLOT 2: Repository documentation/community practices
# ============================================================

draw_barplot_docs <- function() {
  docs <- final_dataset[, c("has_readme", "has_contributing", "has_code_of_conduct",
                             "has_pr_template", "has_issue_template", "has_newcomer_labels")]
  docs[] <- lapply(docs, function(x) as.logical(x))
  doc_counts <- colSums(docs, na.rm = TRUE)
  doc_percent <- (doc_counts / nrow(final_dataset)) * 100
  names(doc_counts) <- c("Readme", "Contributing", "Code of Conduct",
                          "Pull Template", "Issue Template", "Beginner Labels")
  names(doc_percent) <- names(doc_counts)
  ord <- order(doc_percent, decreasing = TRUE)  # largest first → largest at bottom
  doc_percent <- doc_percent[ord]
  doc_counts  <- doc_counts[ord]
  colors <- category_colors[names(doc_percent)]

  par(mar = c(4, 8.5, 1, 1), mgp = c(1.75, 0.5, 0), lwd = 2)
  bar_positions <- barplot(doc_percent, horiz = TRUE, plot = FALSE)
  plot(NA, NA, xlim = c(0, 100), ylim = range(bar_positions) + c(-0.7, 0.7),
       xlab = "Percentage of Projects", ylab = "", axes = FALSE, xaxs = "i", yaxs = "i",
       cex.lab = 0.9)
  abline(v = seq(0, 100, 25), col = "lightgray", lwd = 1)
  barplot(doc_percent, horiz = TRUE, col = colors, border = "black", lwd = 2,
          las = 1, axes = FALSE, add = TRUE, xlim = c(0, 100), cex.names = 0.9)
  text(x = doc_percent + 1, y = bar_positions, labels = as.integer(doc_counts),
       adj = 0, cex = 0.8, col = "black")
  axis(side = 1, at = seq(0, 100, 25), labels = paste0(seq(0, 100, 25), "%"), lwd = 2, cex.axis = 0.9)
  box(lwd = 2)
}

postscript("figs/barplot_docs.eps", width = 4.5, height = 2.3, paper = "special", horizontal = FALSE)
draw_barplot_docs()
dev.off()

png("figs/barplot_docs.png", width = 810, height = 415, res = 150)
draw_barplot_docs()
dev.off()


# ============================================================
# INFLOW PLOT 1: Newcomers by ROS distribution
# ============================================================

draw_inflow_distribution <- function() {
  inflow <- read.csv("scripts/tables/inflow.csv", check.names = FALSE)

  meta_cols <- c("project", "owner_type", "distribution_type")
  week_cols <- setdiff(names(inflow), meta_cols)
  n_weeks <- length(week_cols)
  x_vals <- seq(-(n_weeks - 1), 0)

  categories <- list(
    "Multi-Distribution" = "multi-distro",
    "Humble only"        = "humble-only",
    "Jazzy only"         = "jazzy-only",
    "Kilted only"        = "kilted-only"
  )
  colors <- c(
    "Multi-Distribution" = "#E74C3C",
    "Humble only"        = "#1F618D",
    "Jazzy only"         = "#A9B83E",
    "Kilted only"        = "#9B59B6"
  )
  ltypes <- c(
    "Multi-Distribution" = 1,
    "Humble only"        = 5,
    "Jazzy only"         = 2,
    "Kilted only"        = 6
  )

  agg <- lapply(categories, function(cat) {
    rows <- inflow[inflow$distribution_type == cat, week_cols]
    colSums(rows, na.rm = TRUE)
  })
  repo_counts <- sapply(categories, function(cat) sum(inflow$distribution_type == cat))
  tick_at <- seq(-27, 0, by = 3)

  par(mar = c(5.0, 5.0, 0.5, 0.5), mgp = c(3.5, 1.1, 0))
  plot(x_vals, agg[["Multi-Distribution"]], type = "n",
       xlim = c(-27, 0), ylim = c(0, 110),
       xlab = "Week", ylab = "# Newcomers", axes = FALSE,
       cex.lab = 1.6)
  abline(h = seq(0, 110, 25), col = "#d9d9d9", lty = 1, lwd = 0.5)
  abline(v = tick_at, col = "#d9d9d9", lty = 1, lwd = 0.5)

  for (cat_name in names(categories)) {
    lwd <- if (cat_name == "Multi-Distribution") 3.5 else 2.5
    lines(x_vals, agg[[cat_name]],
          col = colors[cat_name], lty = ltypes[cat_name], lwd = lwd)
  }

  axis(1, at = tick_at, labels = tick_at, cex.axis = 1.1, gap.axis = 0)
  axis(2, at = seq(0, 100, 25), las = 1, cex.axis = 1.4)
  box()

  legend("topleft",
         legend = paste0(names(categories), " (n=", repo_counts, ")"),
         col = colors, lty = ltypes, lwd = 2.0,
         bty = "n", cex = 1.1, seg.len = 1.5)
}

postscript("figs/newcomer_inflow_distribution.eps", width = 5.5, height = 4.0, paper = "special", horizontal = FALSE)
draw_inflow_distribution()
dev.off()

png("figs/newcomer_inflow_distribution.png", width = 990, height = 720, res = 150)
draw_inflow_distribution()
dev.off()


# ============================================================
# INFLOW PLOT 2: Newcomers by owner type
# ============================================================

draw_inflow_owner <- function() {
  inflow <- read.csv("scripts/tables/inflow.csv", check.names = FALSE)

  meta_cols <- c("project", "owner_type", "distribution_type")
  week_cols <- setdiff(names(inflow), meta_cols)
  n_weeks <- length(week_cols)
  x_vals <- seq(-(n_weeks - 1), 0)

  categories <- list(
    "Organization" = "Organization",
    "User"         = "User"
  )
  colors <- c(
    "Organization" = "#3498DB",
    "User"         = "#E67E22"
  )
  ltypes <- c(
    "Organization" = 1,
    "User"         = 2
  )

  agg <- lapply(categories, function(cat) {
    rows <- inflow[inflow$owner_type == cat, week_cols]
    colSums(rows, na.rm = TRUE)
  })
  repo_counts <- sapply(categories, function(cat) sum(inflow$owner_type == cat))
  tick_at <- seq(-27, 0, by = 3)

  par(mar = c(5.0, 5.0, 0.5, 0.5), mgp = c(3.5, 1.1, 0))
  plot(x_vals, agg[["Organization"]], type = "n",
       xlim = c(-27, 0), ylim = c(0, 120),
       xlab = "Week", ylab = "# Newcomers", axes = FALSE,
       cex.lab = 1.6)
  abline(h = seq(0, 120, 25), col = "#d9d9d9", lty = 1, lwd = 0.5)
  abline(v = tick_at, col = "#d9d9d9", lty = 1, lwd = 0.5)

  for (cat_name in names(categories)) {
    lwd <- if (cat_name == "Organization") 3.5 else 2.5
    lines(x_vals, agg[[cat_name]],
          col = colors[cat_name], lty = ltypes[cat_name], lwd = lwd)
  }

  axis(1, at = tick_at, labels = tick_at, cex.axis = 1.1, gap.axis = 0)
  axis(2, at = seq(0, 120, 25), las = 1, cex.axis = 1.4)
  box()

  legend("topleft",
         legend = paste0(names(categories), " (n=", repo_counts, ")"),
         col = colors, lty = ltypes, lwd = 2.0,
         bty = "n", cex = 1.1, seg.len = 1.5)
}

postscript("figs/newcomer_inflow_owner.eps", width = 5.5, height = 4.0, paper = "special", horizontal = FALSE)
draw_inflow_owner()
dev.off()

png("figs/newcomer_inflow_owner.png", width = 990, height = 720, res = 150)
draw_inflow_owner()
dev.off()
