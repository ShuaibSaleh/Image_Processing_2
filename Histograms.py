import numpy as np
from numpy.fft import fft, fftfreq, ifft
import cv2
import math
import os





# This function takes the image data that sent from js code and new image name
# then saves the image to the input folder and returns its path
def saveImage(imgData,imgName):
    path = f'./static/images/input/{imgName}.jpg'
    with open(path, 'wb') as f:
        f.write(imgData)

    return path

# This function takes the image path
# then reads the image as grayscale image and resize it and returns the result
def readImg(path):
    img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img,(600,600))
    return img

# This function takes two points coordinates and return the distance between them
def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


# This function takes the cutoff freq. and the image shape
# it creates low pass filter matrix and returns it
def gaussianLPF(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = math.exp(((- distance((y,x),center)**2)/(2*(D0**2))))
    return base

# This function takes the cutoff freq. and the image shape
# it creates high pass filter matrix and returns it
def gaussianHPF(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1 - math.exp(((-distance((y,x),center)**2)/(2*(D0**2))))
    return base

# This function takes the image and the filter
# it transfers the image to the freq. domain and the filter on it
# then transfers the filtered image to the time domain and returns it 
def applyFilter(img,filter):
    img_fft = np.fft.fft2(img)
    img_fft_shifted = np.fft.fftshift(img_fft)
    filtered_shifted_img = img_fft_shifted * filter
    filtered_unshifted_img = np.fft.ifftshift(filtered_shifted_img)
    inverse_lowPass = np.fft.ifft2(filtered_unshifted_img)
    filtered_img = np.real(inverse_lowPass)

    return filtered_img
    

# This function takes two paths of images and the filters combination 
# and the cutoff frequancies that user selects from the interface
# it reads the images and applies the filters on them, then add them togather
#to make the hybridimage and save it and return its path
def makeImg(img1Path,img2Path,filters_option,lpf_D0,hpf_D0):
    
    imgA = readImg(img1Path)
    imgB = readImg(img2Path)
    
    if filters_option == 0:
        
        imgA_LPF = applyFilter(imgA,gaussianLPF(lpf_D0,imgA.shape))
        imgB_HPF = applyFilter(imgB,gaussianHPF(hpf_D0,imgB.shape))
        imgC = imgA_LPF + imgB_HPF
        
    elif filters_option == 1:
        imgB_LPF = applyFilter(imgB,gaussianLPF(lpf_D0,imgB.shape))
        imgA_HPF = applyFilter(imgA,gaussianHPF(hpf_D0,imgA.shape))
        imgC = imgB_LPF + imgA_HPF
        
    else:
        pass

    os.remove("static/images/output/imageC.jpg") 
    pathOFResult= f"static/images/output/imageC.jpg"
    cv2.imwrite(pathOFResult,imgC)
    
    return pathOFResult


         
         
    

            