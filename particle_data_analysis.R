# Name: Lucia Liu
# Last Edited: 12/16/25

library(dplyr)
library(ggplot2)

BINWIDTH_AREA <- 0.1
BY_AREA <- 0.5
BINWIDTH_BRIGHTNESS <- 2500
BY_BRIGHTNESS <- 2500

# input your csv pathname below
df <- read.csv('/Users/lucialiu/Downloads/10_29_2025_fxr1_157W_PK/test output/C1-PK2_WT_results.csv')

# Plotting Methods
plot_histogram <- function(dataset, x_var, x_name, fill_color, title, bin_width, x_tick_break) {
  ggplot(data = dataset, aes(x={{ x_var }})) +
    theme_bw() +
    geom_histogram(color = "white", fill = fill_color, binwidth = bin_width) +
    theme(plot.title = element_text(hjust = 0.5),
          text = element_text(size = 16),
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
          text = element_text(size = 16)) +
    labs(x = 'Area',
         y = "Mean Brightness",
         title = paste('Relationship between Area and Mean Brightness of', cell_type)) +
    scale_x_continuous(breaks = seq(0, max(dataset$Area), by = 1))
}

# Graph plots (run one at a time)
plot_histogram(df, Area, 'Area', 'red', 'Raw Distribution of Channel 1 Stress Granule Area', BINWIDTH_AREA, BY_AREA)
plot_histogram(df, Mean, 'Mean Brightness', 'blue', 'Raw Distribution of Channel 1 Stress Granule Brightness', BINWIDTH_BRIGHTNESS, BY_BRIGHTNESS)
plot_scatterplot(df, 'blue4', 'PK2 WT Channel 1')

# filter out noise: < 0.14??