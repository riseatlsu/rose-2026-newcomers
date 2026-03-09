library(readxl)

# Image size: 270 x 140 pixels
final_dataset <- read_excel("GitHub/rose-2026-newcomers/final_dataset.xlsx")
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

# CONTRIBUTORS COUNT
par(mar = c(2, 2, 1, 1), cex.axis = 1.2, cex.lab = 1.2)

boxplot(
  na.omit(final_dataset$contributors_count),
  horizontal = TRUE,
  col = "lightgray",
  lwd = 3,        # Controls the box and median
  whisklwd = 3,   # Controls the whisker lines
  staplelwd = 3,  # Controls the "T" ends of the whiskers
  outline = FALSE,
  xlab = ""
)

# This adds the thick border around the plot area
box(lwd = 3)

# This redraws the x-axis line with the thicker width
axis(side = 1, lwd = 3, labels = FALSE)

# COMMITS COUNT
par(mar = c(2, 2, 1, 1), cex.axis = 1.2, cex.lab = 1.2)

boxplot(
  na.omit(final_dataset$commits_count),
  horizontal = TRUE,
  col = "lightgray",
  lwd = 3,        # Controls the box and median
  whisklwd = 3,   # Controls the whisker lines
  staplelwd = 3,  # Controls the "T" ends of the whiskers
  outline = FALSE,
  xlab = ""
)

# This adds the thick border around the plot area
box(lwd = 3)

# This redraws the x-axis line with the thicker width
axis(side = 1, lwd = 3, labels = FALSE)

# AGE
par(mar = c(2, 2, 1, 1), cex.axis = 1.2, cex.lab = 1.2)

boxplot(
  na.omit(final_dataset$`Repository age (months)`),
  horizontal = TRUE,
  col = "lightgray",
  lwd = 3,        # Controls the box and median
  whisklwd = 3,   # Controls the whisker lines
  staplelwd = 3,  # Controls the "T" ends of the whiskers
  outline = FALSE,
  xlab = ""
)

# This adds the thick border around the plot area
box(lwd = 3)

# This redraws the x-axis line with the thicker width
axis(side = 1, lwd = 3, labels = FALSE)


# FORKS COUNT
par(mar = c(2, 2, 1, 1), cex.axis = 1.2, cex.lab = 1.2)

boxplot(
  na.omit(final_dataset$`Number of forks`),
  horizontal = TRUE,
  col = "lightgray",
  lwd = 3,        # Controls the box and median
  whisklwd = 3,   # Controls the whisker lines
  staplelwd = 3,  # Controls the "T" ends of the whiskers
  outline = FALSE,
  xlab = ""
)

# This adds the thick border around the plot area
box(lwd = 3)

# This redraws the x-axis line with the thicker width
axis(side = 1, lwd = 3, labels = FALSE)

# NEWCOMERS COUNT (VERTICAL)

par(mar = c(2, 2, 1, 1), cex.axis = 1.2, cex.lab = 1.2)

boxplot(
  na.omit(final_dataset$`Average number of newcomers per month`),
  col = "lightgray",
  lwd = 3,        # Controls the box and median
  whisklwd = 3,   # Controls the whisker lines
  staplelwd = 3,  # Controls the "T" ends of the whiskers
  outline = FALSE,
  ylab = ""
)

# Thick border around the plot area
box(lwd = 3)

# Redraw the y-axis thicker
axis(side = 2, lwd = 3, labels = FALSE)


