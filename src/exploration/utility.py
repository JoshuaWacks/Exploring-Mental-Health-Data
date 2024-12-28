import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def group_and_compare(data,inde,depe,min_percentage):

    plt.figure(figsize=(12,8))
    df = data.groupby(inde)[depe].describe().reset_index()

    min_count = min_percentage*len(data)
    df = df.loc[df['count'] > min_count]
    ax = sns.barplot(x = inde,y='mean',data=df)
    ax.bar_label(ax.containers[0], labels=df['count'])
    if inde == 'City':
        ax.set(xticklabels=[])
    

    plt.show()