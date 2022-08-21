from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from PIL import Image, ImageChops
from matplotlib import pyplot as plt
import numpy as np
import cv2
import numpy as np

def rotate(img, angle):
    rows,cols,c = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return dst

def sum_rows(img):
    # Create a list to store the row sums
    row_sums = []
    # Iterate through the rows
    for r in range(img.shape[0]-1):
        # Sum the row
        row_sum = sum(sum(img[r:r+1,:]))
        # Add the sum to the list
        row_sums.append(list(row_sum))
    # Normalize range to (0,255)
    print(row_sums)

    row_sums = (row_sums/max(row_sums)) * 255
    # Return
    return row_sums

def display_data(roi, row_sums, buffer):    
    # Create background to draw transform on
    bg = np.zeros((buffer*2, buffer*2), np.uint8)    
    # Iterate through the rows and draw on the background
    for row in range(roi.shape[0]-1):
        row_sum = row_sums[row]
        bg[row:row+1, :] = row_sum
    left_side = int(buffer/3)
    bg[:, left_side:] = roi[:,left_side:]   
    cv2.imshow('bg1', bg)
    k = cv2.waitKey(1)
    #out.write(cv2.cvtColor(cv2.resize(bg, (320,320)), cv2.COLOR_GRAY2BGR))
    return k

def rotate_img(src):
	angle = 0
	scores = []
	while angle <= 360:
		# Rotate the source image
		img = rotate(src, angle)    
		# Crop the center 1/3rd of the image (roi is filled with text)
		h,w,c = img.shape
		buffer = min(h, w) - int(min(h,w)/1.15)
		roi = img[int(h/2-buffer):int(h/2+buffer), int(w/2-buffer):int(w/2+buffer)]
		# Create background to draw transform on
		bg = np.zeros((buffer*2, buffer*2), np.uint8)
		# Compute the sums of the rows
		row_sums = sum_rows(roi)
		# High score --> Zebra stripes
		score = np.count_nonzero(row_sums)
		scores.append(score)
		# Image has best rotation
		if score <= min(scores):
			# Save the rotatied image
			print('found optimal rotation')
			best_rotation = img.copy()
		k = display_data(roi, row_sums, buffer)
		if k == 27: break
		# Increment angle and try again
		angle += .75

	return best_rotation



def mse(imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def compare_images(imageA, imageB, card_name):
        # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB, multichannel=True)
    print(m,'#', s, '#', card_name)
    return (m, s)
    

card_filenames = list(os.walk('./cards/'))[0][2]



cards = []
for card_filename in card_filenames:
    print('loading images', card_filename)
    img = cv2.imread('./cards/'+card_filename)
    #img = Image.open('./cards/'+card_filename).convert('RGB')
    # convert the images to grayscale
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (907, 1209))
    
    #img = img.resize((907, 1209))
    cards.append((img, card_filename))


test_img = cv2.imread("./test_cards/Adrix.jpg")
#test_img = Image.open("./test_cards/Adrix.jpg").convert('RGB')
# convert the images to grayscale
#test_img = cv2.cvtColor(test_img, cv2.COLOR_RGB2BGR)

dim = test_img.shape
#test_img = subimage(test_img, center=(dim[0]/2, dim[1]/2), theta=30)
#test_img = rotate_img(test_img)

test_img = cv2.resize(test_img, (907, 1209))
cv2.imshow("Original", test_img)
input()
input()
cv2.imwrite('output.jpg', test_img)
#test_img = test_img.resize((907, 1209))

#contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
#shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)
'''
fig = plt.figure("Images")
images = ("Original", test_img), 
# loop over the images
for (i, (name, image)) in enumerate(images):
    # show the image
    ax = fig.add_subplot(1, 3, i + 1)
    ax.set_title(name)
    plt.imshow(image, cmap = plt.cm.gray)
    plt.axis("off")
# show the figure
plt.show()
'''

for card, card_name in cards:
    # compare the images
    m, s = compare_images(test_img, card, card_name)
    #print(m,s)
    #diff = ImageChops.difference(test_img, card)
    #print(diff.getbbox(), card_name)
