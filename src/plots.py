import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_occupation_categories(df: pd.DataFrame, save_path: str | None = None):

    # Sort by occupation_ratio to plot bars from highest to lowest
    df = df.sort_values(by=["occupation_ratio","avg_occupation_ratio"] , ascending=True)

    # Plotting
    fig, ax = plt.subplots(figsize=(15, 10))
    bar_width = 0.6
    spacing = 0.3  # Add space between bar groups
    index = index = np.arange(len(df)) * (bar_width * 2 + spacing) #np.arange(len(df))

    # Bars for user percentage and global average
    bars1 = ax.barh(index- bar_width/2, df["occupation_ratio"], bar_width, label="Tes pourcentages d'utilisation", color="#E07A5F")
    bars2 = ax.barh(index + bar_width/2 , df["avg_occupation_ratio"], bar_width, label="Pourcentage moyen de ton OI", color="#3D405B")

    # Labels and Titles
    ax.set_yticks(index)
    ax.set_yticklabels(df["occupation_type"], fontsize=10)
    ax.set_xlabel("Percentage")
    ax.set_title("Comparaison des taux d'occupation")

    # Adding percentage labels
    for bars in [bars1, bars2]:
        for bar in bars:
            bar_width = bar.get_width()
            if bar_width > 0:
                y_position = bar.get_y() + bar.get_height() / 2
                ax.text(bar_width + 0.005, y_position, f'{bar_width*100:.2f}%', va='center', ha='left', fontsize=10)

    ax.legend()
    plt.gca().invert_yaxis()  # Invert Y-axis to match the original orientation

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_donut(manual_fill_in_ratio:float, save_path: str | None = None):
    # Define values and labels
    values = [100*manual_fill_in_ratio, 100*(1-manual_fill_in_ratio)]  # Example values (adjust as needed)

    labels = ["Taux de remplissage manuel", "Non-rempli"]
    colors = ["#0A2F63", "#E23D28"]  # Dark blue & red

    non_zero_indices = [i for i, val in enumerate(values) if val > 0]
    non_zero_values = [values[i] for i in non_zero_indices]
    non_zero_colors = [colors[i] for i in non_zero_indices]

    # Create the donut chart
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        non_zero_values,
        labels=None,  # Hide default labels
        autopct='%.2f%%',
        colors=non_zero_colors,
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        pctdistance=0.85  # Position of percentage labels
    )

    # Draw a white circle in the center to create the donut effect
    center_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(center_circle)

    # Customize text properties
    for text in autotexts:
        text.set_color("white")
        text.set_fontsize(14)
        text.set_weight("bold")

    # Add legend
    plt.legend(labels, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=10)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

