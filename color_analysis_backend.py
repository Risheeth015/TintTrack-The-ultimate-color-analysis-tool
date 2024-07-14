import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import colorsys

# Function to get the colors from the image
def get_image_colors(image_path, num_colors=5):
    # Load and convert image to RGB
    image = Image.open(image_path).convert('RGB')
    image.thumbnail((200, 200))  # Resize for faster processing

    # Convert image to numpy array
    pixels = np.array(image).reshape((-1, 3))

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_

    # Count the frequency of each color
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    color_frequencies = sorted(zip(colors, counts), key=lambda x: x[1], reverse=True)

    return color_frequencies

# Function to plot primary and secondary dominant colors
def plot_dominant_colors(primary_color, secondary_color):
    fig, axes = plt.subplots(1, 2, figsize=(6, 3))

    # Plot primary color
    axes[0].imshow([[primary_color / 255]])
    axes[0].set_title("Primary Dominant Color")
    axes[0].axis('off')

    # Plot secondary color
    axes[1].imshow([[secondary_color / 255]])
    axes[1].set_title("Secondary Dominant Color")
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()

# Function to plot color palette
def plot_color_palette(color_frequencies):
    colors = [color for color, count in color_frequencies]
    counts = [count for color, count in color_frequencies]

    fig, ax = plt.subplots(1, figsize=(12, 2), subplot_kw=dict(xticks=[], yticks=[], frame_on=False))
    total_count = sum(counts)
    proportions = [count / total_count for count in counts]

    start = 0
    for color, proportion in zip(colors, proportions):
        end = start + proportion
        ax.add_patch(plt.Rectangle((start, 0), end - start, 1, facecolor=np.array(color)/255))
        start = end

    plt.title("Color Palette")
    plt.show()

# Function to plot color pie chart
def plot_color_pie_chart(color_frequencies):
    colors = [color for color, count in color_frequencies]
    counts = [count for color, count in color_frequencies]
    total_count = sum(counts)
    proportions = [count / total_count for count in counts]
    hex_colors = ['#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2])) for color in colors]

    # Create labels with percentage
    labels = [f'{color}: {proportion:.2%}' for color, proportion in zip(hex_colors, proportions)]

    plt.figure(figsize=(8, 8))
    plt.pie(proportions, labels=labels, colors=hex_colors, startangle=90, counterclock=False, autopct='%1.1f%%')
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
    plt.title("Color Distribution Using Pie Chart")
    plt.show()

# Function to plot color bar chart
def plot_color_bar_chart(color_frequencies):
    colors = [color for color, count in color_frequencies]
    counts = [count for color, count in color_frequencies]
    total_count = sum(counts)
    proportions = [count / total_count for count in counts]
    hex_colors = ['#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2])) for color in colors]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(len(colors)), proportions, color=hex_colors)
    plt.xlabel('Colors')
    plt.ylabel('Proportion')
    plt.title('Color Distribution Using Bar Chart')
    plt.xticks(range(len(colors)), hex_colors, rotation=90)

    for bar, proportion in zip(bars, proportions):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f'{proportion:.2f}', ha='center', va='bottom')

    plt.show()

# Function to get dominant colors
def get_dominant_colors(image_path, num_colors=5):
    # Load image
    image = Image.open(image_path).convert('RGB')
    image.thumbnail((200, 200))

    # Convert image to numpy array
    pixels = np.array(image).reshape((-1, 3))

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_

    return colors

# Helper functions to convert RGB to HSV and vice versa
def rgb_to_hsv(color):
    return colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)

def hsv_to_rgb(color):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(color[0], color[1], color[2]))

# Function to get similar colors
def get_similar_colors(primary_color, num_colors=5, hue_range=30, saturation_range=30):
    similar_colors = []
    hsv_primary = rgb_to_hsv(primary_color)

    for _ in range(num_colors):
        hue = (hsv_primary[0] + np.random.uniform(-hue_range, hue_range) / 360.0) % 1.0
        saturation = max(0, min(1, hsv_primary[1] + np.random.uniform(-saturation_range, saturation_range) / 100.0))
        value = hsv_primary[2]
        rgb_color = hsv_to_rgb((hue, saturation, value))
        similar_colors.append(rgb_color)

    return similar_colors

# Function to plot similar colors
def plot_similar_colors(image_path, num_dominant_colors=5, num_similar_colors=5):
    dominant_colors = get_dominant_colors(image_path, num_dominant_colors)

    plt.figure(figsize=(10, len(dominant_colors) * 2))  # Adjust figure size based on number of dominant colors

    for i, primary_color in enumerate(dominant_colors, start=1):
        plt.subplot(len(dominant_colors), num_similar_colors + 1, i*(num_similar_colors + 1) - num_similar_colors)
        plt.imshow([np.array([primary_color])/255], extent=[0, 1, 0, 1], aspect='auto')
        plt.axis('off')
        plt.title(f'Dominant Color {i}')

        similar_colors = get_similar_colors(primary_color, num_colors=num_similar_colors)
        for j, color in enumerate(similar_colors, start=1):
            plt.subplot(len(dominant_colors), num_similar_colors + 1, i*(num_similar_colors + 1) - num_similar_colors + j)
            plt.imshow([np.array([color])/255], extent=[0, 1, 0, 1], aspect='auto')
            plt.axis('off')
            plt.title(f'Similar {j}')

    plt.tight_layout()
    plt.show()

# Example usage
image_path = '/content/sample_data/bg.jpg'  # Replace with the path to your image
color_frequencies = get_image_colors(image_path)

# Extract primary and secondary colors
primary_color = color_frequencies[0][0]
secondary_color = color_frequencies[1][0]

# Display primary and secondary dominant colors
plot_dominant_colors(primary_color, secondary_color)

# Plot color palette
plot_color_palette(color_frequencies)

# Plot color pie chart
plot_color_pie_chart(color_frequencies)

# Plot color bar chart
plot_color_bar_chart(color_frequencies)

# Plot similar colors
plot_similar_colors(image_path)
