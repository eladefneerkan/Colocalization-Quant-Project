import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/lucialiu/Downloads/10_29_2025_fxr1_157W_PK/test output/C1-PK2_WT_results.csv')
filtered_df = df[df['Area'] > 0.14]
filtered_df.to_csv('C1-PK2_WT_results_filtered.csv', index=False)

summary = {' ': ['Raw data', 'Filtered Noise data'],
           'Raw Count': [len(df), len(filtered_df)],
           'Median Size': [df['Area'].median(), filtered_df['Area'].median()],
           'Average Size': [f'{df['Area'].mean():.3f}', f'{filtered_df['Area'].mean():.3f}'],
           'Min Size': [df['Area'].min(), filtered_df['Area'].min()],
           'Max Size': [df['Area'].max(), filtered_df['Area'].max()]}

summary_df = pd.DataFrame(summary)
print(summary_df.head())
summary_df.to_csv('C1-PK2_WT_summary.csv', index=False)

def plot_histogram(title, bin_width, dataframe):
    sns.histplot(dataframe['Area'], binwidth = bin_width, binrange=(0, dataframe['Area'].max()), shrink=1)
    plt.xlabel('Area')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()

plot_histogram('Raw Distribution of Particle Areas', 0.1, df)
plot_histogram('Filtered Distribution of Particle Areas', 1, filtered_df)
