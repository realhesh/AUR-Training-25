import numpy as np
import matplotlib.pyplot as plt
import cv2
img = cv2.imread('img.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

out = img.copy()
blue_mask = (out[:,:,0] > 200) & (out[:,:,1] < 150) & (out[:,:,2] < 150)
red_mask = (out[:,:,2] > 200) & (out[:,:,0] < 150) & (out[:,:,1] < 150)
black_mask = (out[:,:,0] < 10) & (out[:,:,1] < 10) & (out[:,:,2] < 10)
white_mask = (out[:,:,0] > 200) & (out[:,:,1] > 200) & (out[:,:,2] > 200)
out[blue_mask & ~white_mask] = [0,0,0]
out[red_mask & ~blue_mask & ~white_mask] = [255,0,0]
out[black_mask & ~red_mask & ~blue_mask & ~white_mask] = [0,0,255]
fig, axes = plt.subplots(1, 2)
axes[0].imshow(img_rgb)
axes[0].set_title('Original Image')
axes[0].axis('off')


out_rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
axes[1].imshow(out_rgb)
axes[1].set_title('Processed Image')
axes[1].axis('off')
plt.show()