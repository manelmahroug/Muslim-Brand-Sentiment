import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

#helper function to save plots in the images folder
def save_plot(title):
    image_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(image_dir, exist_ok=True)
    filename = title.replace(" ", "_").replace("(", "").replace(")", "").replace("?", "")
    return os.path.join(image_dir, f"{filename}.png")

def plot_percentages(df, column_name, x_label, title):
    plt.rcParams['figure.dpi'] = 300
    counts_df = df[column_name].value_counts(normalize=True).reset_index()
    counts_df.columns = ['Category', 'Percentage']
    counts_df['Percentage'] *= 100
    max_index = counts_df['Percentage'].idxmax()
    colors = ['#A9F5AE' if i == max_index else 'grey' for i in range(len(counts_df))]
    plt.figure(figsize=(8.5, 5.5))
    sns.barplot(x='Category', y='Percentage', data=counts_df, palette=colors)
    plt.title(title, fontsize=10)
    plt.xlabel(x_label, fontsize=8)
    plt.ylabel('Percentage', fontsize=8)
    plt.xticks(rotation=45, ha='right', fontsize=7)
    plt.yticks(rotation=45, ha='right', fontsize=7)
    plt.tight_layout()
    print("Saving plot to:", save_plot(title))

    plt.savefig(save_plot(title), dpi= 300)
   

    

def plot_stacked_bar_chart(df, title, xlabel, ylabel, cat_col, sent_col, order=None, legend_title='View'):
    plt.rcParams['figure.dpi'] = 300
    colors = {'Good': '#8ccc87', 'Bad': '#ba3e2b', 'Neutral':'#d1cfcf'}

    grouped = df.groupby([cat_col, sent_col]).size().unstack(fill_value=0)
    grouped_percentage = grouped.div(grouped.sum(axis=1), axis=0) * 100

    if order:
        grouped_percentage = grouped_percentage.loc[order]

    ax = grouped_percentage.plot(kind='bar', stacked=True, figsize=(12, 8), 
                                 color=[colors[col] for col in grouped_percentage.columns])

    for i, (colname, coldata) in enumerate(grouped_percentage.items()):
        for index, value in enumerate(coldata):
            if value > 0:
                ax.text(index, 
                        grouped_percentage.iloc[:index+1, :i+1].sum(axis=1)[index] - (value / 2), 
                        f"{value:.1f}%", 
                        ha='center', va='center', 
                        color='white' if colors[colname] == 'grey' else 'black', 
                        fontsize=8)

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_plot(title), dpi=300)
    plt.show()

def plot_comfort(df, category_col, comfort_level, title, xlabel, ylabel):
    plt.rcParams['figure.dpi'] = 300
    grouped = df.groupby([category_col, comfort_level]).size().reset_index(name='count')
    totals = grouped.groupby(category_col)['count'].transform('sum')
    grouped['percentage'] = (grouped['count'] / totals) * 100
    pivot_table = grouped.pivot(index=category_col, columns=comfort_level, values='percentage').fillna(0)

    comfort_colors = {
        'Very comfortable': '#17b50e',
        'Comfortable': '#9be897',
        'Neutral': '#e3e1e1',
        'Uncomfortable': '#cf4229',
        'Very uncomfortable': '#2ebf26'
    }

    ax = pivot_table.plot(kind='bar', stacked=True, figsize=(10, 6), 
                          color=[comfort_colors.get(level) for level in pivot_table.columns])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Comfort Level', bbox_to_anchor=(1.05, 1), loc='upper left')

    for i, variable in enumerate(pivot_table.index):
        cumulative_percentage = 0
        for level in pivot_table.columns:
            percentage = pivot_table.loc[variable, level]
            if percentage > 0:
                ax.text(i, cumulative_percentage + (percentage / 2),  
                        f"{percentage:.1f}%", 
                        ha='center', va='center', 
                        color='white' if level == 'Very comfortable' else 'black', fontsize=9)
                cumulative_percentage += percentage

    plt.tight_layout()
    plt.savefig(save_plot(title), dpi=300)
    plt.show()

def plot_exposure(df, category_col, exposure_level, title, xlabel, ylabel): 
    grouped = df.groupby([category_col, exposure_level]).size().reset_index(name='count')
    totals = grouped.groupby(category_col)['count'].transform('sum')
    grouped['percentage'] = (grouped['count'] / totals) * 100
    pivot_table = grouped.pivot(index=category_col, columns=exposure_level, values='percentage').fillna(0)

    exposure_colors = {
        'Often': '#17b50e',
        'Not Often': '#cf4229',
        "I don't know": '#9db0f2'
    }

    ax = pivot_table.plot(kind='bar', stacked=True, figsize=(10, 6), 
                          color=[exposure_colors.get(level, '#cccccc') for level in pivot_table.columns])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Exposure Level', bbox_to_anchor=(1.05, 1), loc='upper left')

    for i, category in enumerate(pivot_table.index):
        cumulative_percentage = 0
        for level in pivot_table.columns:
            percentage = pivot_table.loc[category, level]
            if percentage > 0:
                ax.text(i, cumulative_percentage + (percentage / 2), 
                        f"{percentage:.1f}%", 
                        ha='center', va='center', 
                        color='white' if level == 'Often' else 'black', fontsize=9)
                cumulative_percentage += percentage

    plt.tight_layout()
    plt.savefig(save_plot(title), dpi=300)
    plt.show()

def plot_income(df, title, xlabel, ylabel, cat_col, sent_col, legend_title='View', cat_order=None):
    colors = {'Good': '#8ccc87', 'Bad': '#ba3e2b', 'Neutral': '#d1cfcf'}

    if cat_order:
        df[cat_col] = pd.Categorical(df[cat_col], categories=cat_order, ordered=True)

    grouped = df.groupby([cat_col, sent_col]).size().unstack(fill_value=0)
    grouped_percentage = grouped.div(grouped.sum(axis=1), axis=0) * 100

    ax = grouped_percentage.plot(kind='bar', stacked=True, figsize=(12, 8), 
                                 color=[colors[col] for col in grouped_percentage.columns])

    for i, (colname, coldata) in enumerate(grouped_percentage.items()):
        for index, value in enumerate(coldata):
            if value > 0:
                ax.text(index, 
                        grouped_percentage.iloc[:index+1, :i+1].sum(axis=1)[index] - (value / 2), 
                        f"{value:.1f}%", 
                        ha='center', va='center', 
                        color='white' if colors[colname] == 'grey' else 'black', fontsize=8)

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_plot(title), dpi=300)
    plt.show()


def plot_stacked_bar_chart_interaction(df, title, xlabel, ylabel, cat_col, sent_col, legend_title='View'):
    """
    Plots a stacked bar chart with percentages based on the grouping of two columns, 
    one for categories (e.g., education or religion)
    and the other for sentiments.
    """
    
    colors = {
        'Good': '#8ccc87',
        'Bad': '#ba3e2b',
        'Neutral':'#d1cfcf'
    }
    interaction_order = ["None - 0", "1", "2 to 4", "5 to 10", "More than 10"]
    
    grouped = df.groupby([cat_col, sent_col]).size().unstack(fill_value=0)

    grouped = grouped.reindex(interaction_order)
    
    grouped_percentage = grouped.div(grouped.sum(axis=1), axis=0) * 100

    ax = grouped_percentage.plot(kind='bar', stacked=True, figsize=(12, 8), \
                                 color=[colors[col] for col in grouped_percentage.columns])
    # Add percentage annotations
    for i, (colname, coldata) in enumerate(grouped_percentage.items()):
        for index, value in enumerate(coldata):
            if value > 0:  # Only annotate non-zero segments
                ax.text(index, 
                        grouped_percentage.iloc[:index+1, :i+1].sum(axis=1)[index] - (value / 2), 
                        # Position the text in the center of the segment
                        f"{value:.1f}%", 
                        ha='center', 
                        va='center', 
                        color='white' if colors[colname] == 'grey' else 'black', 
                        fontsize=8)


    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45, ha='right')

    # Position the legend outside the plot
    plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.figure(figsize=(9, 5), dpi=800)
    plt.savefig(save_plot(title), dpi=300)
    plt.show()