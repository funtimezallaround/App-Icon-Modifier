import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# DETECT APP ICONS FROM A SCREENSHOT

# path to the input image
src_img:str = 'input/edges.png'

# load the image
img = cv2.imread(src_img)

small_mask = cv2.imread('masks/iconmask_small.png', cv2.IMREAD_UNCHANGED)
big_mask = cv2.imread('masks/iconmask_big.png', cv2.IMREAD_UNCHANGED)

small_mask = cv2.resize(small_mask, (86, 86))
big_mask = cv2.resize(big_mask, (157, 157))

# find edges
# img_blurred = cv2.GaussianBlur(img, (5, 5), 0)
# img_edges = cv2.Canny(img_blurred, 100, 200)


# Match template
image = img
template = small_mask

result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Get best match location
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

print("Best match confidence:", max_val)

# Draw rectangle if match is strong enough
threshold = 0.5  # Adjust this value (closer to 1.0 = stricter match)
if max_val >= threshold:
    h, w = template.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(image_color, top_left, bottom_right, (0, 255, 0), 2)

    cv2.imwrite("/mnt/data/match_result.png", image_color)
    print("Match found and result saved to match_result.png")
else:
    print("No strong match found")
cv2.imwrite('output/edges.png', img)