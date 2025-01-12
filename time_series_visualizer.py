import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    plt.figure(figsize=(12, 4))
    plt.plot(df.index, df['value'], label='Page Views', color='red', linewidth=1)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=10)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Page Views', fontsize=12)
    plt.tight_layout()
    fig = plt.gcf()

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    import numpy as np
    df2 = df.copy()
    df2['year'] = df2.index.year
    df2['month'] = df2.index.month
    monthly_avg = df2.groupby(['year', 'month'])['value'].mean().reset_index()
    pivot_table = monthly_avg.pivot(index='year', columns='month', values='value')
    years = pivot_table.index
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    colors = sns.color_palette("Paired", len(df2['month'].unique()))
    width = 0.7 / 12
    x = np.arange(len(years))
    plt.figure(figsize=(12, 8))
    for i, month in enumerate(months):
        plt.bar(x + i * width, pivot_table[i + 1], width=width, label=month, color=colors[i])

    plt.xlabel('Years', fontsize=14)
    plt.ylabel('Average Page Views', fontsize=14)
    plt.title('Average Page Views', fontsize=16)
    plt.legend(title='Months', fontsize=10, title_fontsize=12,loc='upper left')
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig('bar_plot.png')
    return fig

draw_bar_plot()
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, a = plt.subplots(1, 2, figsize=(25, 5))
    color_year = sns.color_palette("Paired", len(df_box['year'].unique()))
    color_month = sns.color_palette("Paired", len(df_box['month'].unique()))

    sns.boxplot(data=df_box, x="year", y="value", ax=a[0], palette=color_year, hue='year', legend=False)
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=a[1], hue='month', legend=False,
                palette=color_month)
    a[0].set_title("Year-wise Box Plot (Trend)")
    a[0].set_xlabel("Year")
    a[0].set_ylabel("Page Views")
    a[1].set_title("Month-wise Box Plot (Seasonality)")
    a[1].set_xlabel("Month")
    a[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig
