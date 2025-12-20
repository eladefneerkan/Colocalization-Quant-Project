# Name: Lucia Liu
# Last Edited: 12/19/25

library(dplyr)
library(ggplot2)

BINWIDTH_AREA <- 0.1
BY_AREA <- 0.5
BINWIDTH_BRIGHTNESS <- 2500
BY_BRIGHTNESS <- 2500

dark_blue <- "#12436D"
teal <- "#28A197"
orange <- "#F46A25"
lavender <- "#A285D1"
dark_red <- "#801650"
light_blue <- "#6BACE6"
medium_blue <- "#2073BC"

# Input your csv pathname below
df <- read.csv('______PATHNAME HERE______')

# Plotting Methods
plot_histogram <- function(dataset, x_var, x_name, fill_color, title, bin_width, x_tick_break) {
  ggplot(data = dataset, aes(x={{ x_var }})) +
    theme_bw() +
    geom_histogram(color = "white", fill = fill_color, binwidth = bin_width) +
    theme(plot.title = element_text(hjust = 0.5),
          text = element_text(size = 18),
          axis.text.x = element_text(size = 11, angle = 45, hjust = 1)) +
    labs(x = x_name,
         y = "Frequency",
         title = title) +
    scale_x_continuous(breaks = seq(0, max(dataset[[rlang::as_name(rlang::enquo(x_var))]], na.rm = TRUE), by = x_tick_break)) +
    geom_text(stat="bin", binwidth = bin_width, aes(label=after_stat(count)), vjust=-0.3, size=2.5)
}

plot_scatterplot <- function(dataset, dot_color, cell_type) {
  ggplot(data = dataset, aes(x=Area, y=Mean)) +
    theme_bw() +
    geom_point(color = dot_color) +
    theme(plot.title = element_text(hjust = 0.5),
          text = element_text(size = 18)) +
    labs(x = 'Area (µm^2)',
         y = "Mean Gray Value",
         title = paste('Relationship between Area and Intensity of', cell_type)) +
    scale_x_continuous(breaks = seq(0, max(dataset$Area), by = 1))
}

# Graph plots (run one at a time)
plot_histogram(df, Area, 'Area (µm^2)', light_blue, 'Distribution of ______ Particle Areas', BINWIDTH_AREA, BY_AREA)
plot_histogram(df, Mean, 'Mean Gray Value', teal, 'Distribution of ______ Intensity', BINWIDTH_BRIGHTNESS, BY_BRIGHTNESS)
plot_scatterplot(df, dark_blue, '_________')
