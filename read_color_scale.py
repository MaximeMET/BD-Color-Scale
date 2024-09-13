# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:46:09 2024

@author: maxim
"""

from PIL import Image, ImageFilter

def apply_gaussian_blur(image, radius):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    return blurred_image

def save_and_compute_averages(image, output_file, scan_x_if_equal=False):
    # Open the image and get its original dimensions
    original_width, original_height = image.size
    
    # Resize the picture so that the number of rows of output data is 256
    if original_width > original_height or (original_width == original_height and scan_x_if_equal):  # Width is greater than height or scan_x_if_equal=True
        # Compress the width to 256 and keep the height the same
        new_width = 256
        new_height = original_height
        image = image.resize((new_width, new_height))
        # print(f"图片宽大于高，调整后的图片大小: {new_width}x{new_height}")
    else:  # The height is greater than the width
        # Compress the height to 256 and keep the width the same
        new_height = 256
        new_width = original_width
        image = image.resize((new_width, new_height))
        # print(f"图片高大于宽，调整后的图片大小: {new_width}x{new_height}")
    
    data_dict = {}

    # Determine the scanning direction according to the aspect ratio of the original image
    if original_width > original_height or (original_width == original_height and scan_x_if_equal):  # Scan along x-direction
        for y in range(new_height):  # From top to bottom
            for x in range(new_width):  # Along x-direction
                pixel = image.getpixel((x, y))
                r, g, b, a = (pixel if len(pixel) == 4 else (*pixel, 255))
                
                # Initialize if x does not already appear in the dict
                if x not in data_dict:
                    data_dict[x] = ([r], [g], [b], [a])
                else:
                    # Append a value to the list
                    data_dict[x][0].append(r)
                    data_dict[x][1].append(g)
                    data_dict[x][2].append(b)
                    data_dict[x][3].append(a)
                    
    else:  # Scan along 7-direction
        for y in range(new_height - 1, -1, -1):  # From bottom to top
            for x in range(new_width):  # Along x-direction
                pixel = image.getpixel((x, y))
                r, g, b, a = (pixel if len(pixel) == 4 else (*pixel, 255)) 
                
                # Initialize if y does not already appear in the dict
                if y not in data_dict:
                    data_dict[y] = ([r], [g], [b], [a])
                else:
                    # Append a value to the list
                    data_dict[y][0].append(r)
                    data_dict[y][1].append(g)
                    data_dict[y][2].append(b)
                    data_dict[y][3].append(a)

    # Save the average result to the output file
    with open(output_file, 'w') as result_file:
        for key, values in data_dict.items():
            avg_r = sum(values[0]) / len(values[0])
            avg_g = sum(values[1]) / len(values[1])
            avg_b = sum(values[2]) / len(values[2])
            result_file.write(f"{avg_r:.2f} {avg_g:.2f} {avg_b:.2f}\n")

# sample
image_path = "sample1.png"
output_file = "averages_result.txt"
image = Image.open(image_path)

gaussian_switch = True
radius = 5
if gaussian_switch:
    image = apply_gaussian_blur(image, radius)

scan_x_if_equal = True  # Use a switch to choose whether to average by the x-direction

save_and_compute_averages(image, output_file, scan_x_if_equal)



