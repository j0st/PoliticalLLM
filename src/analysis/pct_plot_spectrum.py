import matplotlib.pyplot as plt

def extract_coordinates(raw_coordinates: str):
    """
    The PCT website gives us the coordinates in the following format: 'Economic Left/Right: -5.75\nSocial Libertarian/Authoritarian: -5.08'.
    This function splits the coordinates and extracts the actual values.
    """
    econ_coord, social_coord = raw_coordinates.split('\n')
    econ_value = float(econ_coord.split(': ')[1])
    social_value = float(social_coord.split(': ')[1])
    
    return econ_value, social_value


def plot_political_compass(filename: str, list_of_coordinates: list):
    """
    Plots the coordinates on a two-dimension spectrum. For multiple coordinates, this function calculates and plots the mean coordinates as well.
    """

    points = []

    for coordinate in list_of_coordinates:
        econ_value, social_value = extract_coordinates(coordinate)
        points.append((econ_value, social_value, "grey"))
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))

    # Set limits for x and y axes
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    # Draw axes lines
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)

    # Set grid
    plt.grid(color='gray', linestyle='-', linewidth=0.25)

    ax.fill_between([0, 10], [0, 0], [10, 10], color='#42AAFF', alpha=0.8, label='AR')     # Upper-right quadrant
    ax.fill_between([-10, 0], [0, 0], [10, 10], color='#FF7575', alpha=0.8, label='AL')   # Upper-left quadrant
    ax.fill_between([0, 10], [-10, -10], [0, 0], color='#C09AEC', alpha=0.8, label='LR')     # Lower-right quadrant
    ax.fill_between([-10, 0], [-10, -10], [0, 0], color='#9AED97', alpha=0.8, label='LL')     # Lower-left quadrant
    
    
    # Dictionary to store the count of dots at each coordinate
    coordinate_counts = {}
    
    # Plot the points
    for point in points:
        x, y, color = point
        coordinate = (x, y)
        if coordinate in coordinate_counts:
            coordinate_counts[coordinate] += 1
        else:
            coordinate_counts[coordinate] = 1

        # Adjust the alpha value based on the count of dots at the coordinate
        alpha = 0.3 / coordinate_counts[coordinate]  # Reduce alpha for additional dots

        ax.plot(x, y, color="black", marker='o', markersize=20, markerfacecolor=color, alpha=alpha)  # Adjust dot size and alpha
    
    
    # MEANS
    mean_point = (round(sum(x[0] for x in points) / len(points), 2), round(sum(x[1] for x in points) / len(points), 2))
    x, y = mean_point
    ax.plot(x, y, color="black", marker='^', markersize=20, markerfacecolor="grey")

    # Customize ticks
    ticks_range = range(-10, 11, 1)  # From -10 to 10, stepping by 2
    plt.xticks(ticks_range)
    plt.yticks(ticks_range)
    
    # Hide x and y ticks
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    
    # Remove outer black lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add legend
    ax.plot([], [], color="grey", marker='o', markersize=0, label=filename)  # Add Base legend without plotting points
    plt.legend(loc='upper right')
    
    # Save plot
    plt.savefig(f'results//experiments//pct//plot-{filename}.png', dpi=300)
