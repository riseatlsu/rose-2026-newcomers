library(readxl)

# Image size: 270 x 140 pixels
final_dataset <- read_excel("GitHub/rose-2026-newcomers/final_dataset.xlsx")

# DOCUMENT ANALYSIS
docs <- final_dataset[, c(
  "has_readme",
  "has_contributing",
  "has_code_of_conduct",
  "has_pr_template",
  "has_issue_template",
  "has_newcomer_labels"
)]

doc_counts <- colSums(docs, na.rm = TRUE)

barplot(
  doc_counts,
  col = "lightgray",
  border = "black",
  las = 2,            # rotate labels
  ylab = "# of Projects",
  lwd = 2
)