import cv2
import numpy as np
from sklearn.cluster import KMeans
import webcolors

# Function to get the name of the closest color
def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

# Function to determine the dominant color
def get_dominant_color(image_path, k=3):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    
    dominant_color = kmeans.cluster_centers_.astype(int)[0]
    color_name = closest_color(dominant_color)
    
    return color_name

# Example usage
if __name__ == "__main__":
    image_path = "D:/Users/91978/Downloads/Screenshot 2023-02-08 221640.jpg"  # Replace with the path to your image
    dominant_color = get_dominant_color(image_path)
    
    print(f"The dominant color in the image is: {dominant_color}")
