import matplotlib.pyplot as plt
import numpy as np

def plot_wahlomat_results(filename, values_group1, std_dev_group1, values_group2=None, std_dev_group2=None):
    # CATEGORIES
    categories = ["CDU / CSU", "AfD", "PIRATEN", "DIE LINKE", "SSW", "GRÜNE", "SPD", "FDP"]

    # # VALUES
    # values_group1 = [56.58, 44.74, 63.16, 57.89, 63.16, 65.79, 63.16, 56.58]
    # values_group2 = [60.53, 67.11, 46.05, 32.89, 46.05, 35.53, 40.79, 60.53]

    # # std
    # std_dev_group1 = [0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64]
    # std_dev_group2 = [1.24, 1.24, 1.49, 1.24, 1.52, 1.24, 0.83, 1.52]

    # Number of categories
    num_categories = len(categories)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Set the maximum value for the radial axis
    ax.set_ylim(0, 100)

    # Create a list of angles for the categories
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()

    # The plot is circular, so we "complete the loop" by appending the start value to the end
    values_group1 += values_group1[:1]
    if values_group2:
        values_group2 += values_group2[:1]
    angles += angles[:1]

    # Plot the values for the first group (grey color)
    ax.plot(angles, values_group1, color='grey', linewidth=1, linestyle='solid')
    ax.fill(angles, values_group1, color='grey', alpha=0.25)

    # Plot the values for the second group (blue color)
    if values_group2:
        ax.plot(angles, values_group2, color='blue', linewidth=1, linestyle='solid')
        ax.fill(angles, values_group2, color='blue', alpha=0.25)

    # Plot the error bars
    ax.errorbar(angles[:-1], values_group1[:-1], yerr=std_dev_group1, fmt='none', color='black', markersize=2, capsize=0)
    if values_group2:
        ax.errorbar(angles[:-1], values_group2[:-1], yerr=std_dev_group2, fmt='none', color='black', markersize=2, capsize=0)


    # Set the labels for each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    #plt.show()

    plt.savefig(f'results//experiments//wahlomat//plot-{filename}-wahlomat.png', dpi=300)