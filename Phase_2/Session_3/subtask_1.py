import numpy as np
import matplotlib.pyplot as plt
import cv2

def convolve(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    padding_sz=(kernel.shape[1]-1)//2
    image = np.pad(image,padding_sz)
    image_rows = image.shape[0]
    image_columns = image.shape[1]
    answer = np.zeros((image_rows,image_columns))
    kernel_rows = kernel.shape[0]
    kernel_columns = kernel.shape[1]
    for i in range(0,image_rows - kernel_rows+1):
        for j in range(0,image_columns - kernel_columns+1):
            answer[i][j] = abs(np.sum(image[i:i+kernel_rows,j:j+kernel_columns]*kernel))
    return answer

img=cv2.imread('image.jpg',cv2.IMREAD_GRAYSCALE)
fig,axes=plt.subplots(2,2,figsize =(8,8))
axes[0,0].imshow(img,cmap='gray')
axes[0,0].set_title('Original Image')
axes[0,0].axis('off')

axes[0,1].imshow(convolve(img,np.ones((5,5))/25),cmap='gray')
axes[0,1].set_title('Box Filter')
axes[0,1].axis('off')

axes[1, 0].imshow(convolve(img, np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])),
cmap='gray')
axes[1, 0].set_title('Horizontal Sobel Filter')
axes[1, 0].axis('off')
axes[1, 1].imshow(convolve(img, np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])),
cmap='gray')

axes[1, 1].set_title('Vertical Sobel Filter')
axes[1, 1].axis('off')
plt.show()