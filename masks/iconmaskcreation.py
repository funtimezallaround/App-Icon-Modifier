import cv2


# path to the input image
scr_img: str = 'masks\\OIP.JPG'

# load the image
img = cv2.imread(scr_img)

# convert to black and white (binary)
_, iconmask = cv2.threshold(cv2.cvtColor(
    img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)

# edges
icon_edges = cv2.Canny(iconmask, 100, 200)

# create a version with transparent background (remove black pixels, hello racism)
iconmask_nobg = cv2.cvtColor(icon_edges, cv2.COLOR_GRAY2BGRA)
iconmask_nobg[icon_edges == 0] = [0, 0, 0, 0]  # set black pixels to transparent


# scale down to different sizes
big = cv2.resize(iconmask_nobg, (157, 157))
small = cv2.resize(iconmask_nobg, (86, 86))

# save the masks
cv2.imwrite('iconmask_big.png', big)
cv2.imwrite('iconmask_small.png', small)
