
import matplotlib.pyplot as plt
import cv2 
import numpy as np
import random


class Filters:

    def addUniformNoise(path):
        image=cv2.imread(path,0)
        # normalization 
        image = image/255
        # uniform noise
        x, y = image.shape
        start = 0
        end = 0.5
        array_of_noise = np.zeros((x,y), dtype=np.float64)
        for i in range(x):
            for j in range(y):
                array_of_noise[i][j] = np.random.uniform(start,end)
        # add noise to immage
        noise_img = image + array_of_noise
        #  to round value
        imageaddedNoise=np.clip(noise_img,0,255)
        return  imageaddedNoise *255



    def addGaussianNoise(path , sigma=0.7 , mean=0 ):
        imag=cv2.imread(path,0)
        imag=imag/255
        yDiminsion, xDiminsion  =imag.shape

        # Initializing value of x,y as grid of kernel size
        # in the range of kernel size

        x, y = np.meshgrid(np.linspace(-1, 1,xDiminsion), np.linspace(-1, 1, yDiminsion))
        dst = np.sqrt(x**2+y**2)
        # lower normal part of gaussian
        normal = 1/(2 * np.pi * sigma**2)
        # # Calculating Gaussian filter
        gaussNoise = np.exp(-((dst-mean)**2 / (2.0 * sigma**2))) * normal
        return (gaussNoise+imag)*255
    
    def add_salt_noise(path):
        image=cv2.imread(path , 0)
        row , col = image.shape
        number_of_pixels = random.randint(300 , 10000)
        for i in range(number_of_pixels):
            y_coord_salt=random.randint(0, row - 1)
            x_coord_salt=random.randint(0, col - 1)
            y_coord_papper=random.randint(0, row - 1)
            x_coord_papper=random.randint(0, col - 1)
            image[y_coord_salt ,x_coord_salt]=255
            image[y_coord_papper ,x_coord_papper]=0

        return image
        


    # #  done 
    def Gaussian_filter(kernel_size, sigma=1, mean=0):

        # Initializing value of x,y as grid of kernel size
        # in the range of kernel size
        x, y = np.meshgrid(np.linspace(-1, 1, kernel_size), np.linspace(-1, 1, kernel_size))

        dst = np.sqrt(x**2+y**2)
        # lower normal part of gaussian
        normal = 1/(2 * np.pi * sigma**2)
        # Calculating Gaussian filter
        gauss = np.exp(-((dst-mean)**2 / (2.0 * sigma**2))) * normal
        return gauss
    
    
    def average_filter(kernel_size):
        average_list=np.ones(shape=(kernel_size,kernel_size),dtype=int)
        sumElement=np.sum(average_list)
        average_list=average_list*(1/sumElement)
        return average_list
    

    def median_Filter(sizeOfFilter=3 , image=[[]]):
        if sizeOfFilter%2 ==0 :
            sizeOfFilter+=1

        outputList=np.zeros(shape=(image.shape[0] , image.shape[1]))
        listBeforFilter=np.ones(shape=(sizeOfFilter ,sizeOfFilter))

        for i in range(image.shape[0]-int(sizeOfFilter/2)):
            for j in range(image.shape[1]-int(sizeOfFilter/2)):

                listBeforFilter=image[i:i+sizeOfFilter , j:sizeOfFilter+j]
                listBeforFilter[int(sizeOfFilter/2),int(sizeOfFilter/2)]=np.median(listBeforFilter)
                outputList[i:i+sizeOfFilter , j:sizeOfFilter+j]=listBeforFilter

        return outputList
    




    def saveoutputNoise(imgData ):
        pathNoise=f'./static/images/output/Addnoise.jpg'
        cv2.imwrite(pathNoise, imgData)
        
        return pathNoise
    
    def saveoutputFilter(imgData ):
        path=f'./static/images/output/AddFilter.jpg'
        cv2.imwrite(path, imgData)
        
        return path







    def convolve2D(image=[], kernel=[], padding=0, strides=1):
        # Cross Correlation
        kernel = np.flipud(np.fliplr(kernel))

        # Gather Shapes of Kernel + Image + Padding
        xKernShape = kernel.shape[0]
        yKernShape = kernel.shape[1]
        xImgShape = image.shape[0]
        yImgShape = image.shape[1]

        # Shape of Output Convolution
        xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
        yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
        output = np.zeros((xOutput, yOutput))

        # Apply Equal Padding to All Sides
        if padding != 0:
            imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
            imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        else:
            imagePadded = image

        # Iterate through image
        for y in range(image.shape[1]):
            # Exit Convolution
            if y > image.shape[1] - yKernShape:
                break
            # Only Convolve if y has gone down by the specified Strides
            if y % strides == 0:
                for x in range(image.shape[0]):
                    # Go to next row once kernel is out of bounds
                    if x > image.shape[0] - xKernShape:
                        break
                    try:
                        # Only Convolve if x has moved by the specified Strides
                        if x % strides == 0:
                            output[x, y] = (kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()
                    except:
                        break

        return output
    def sobel_operator(path):
        image=cv2.imread(path,0)

        filter_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]) 
        filter_y =np.flip(filter_x.T, axis=0)
   
        # gradient_magnitude *= 255.0 / gradient_magnitude.max()

        return image,filter_x,filter_y
    def roberts_operator(path):
        roberts_cross_x = np.array( [[ 0, 1 ],
                                    [ -1, 0 ]] )
        roberts_cross_y = np.array( [[1, 0 ],
                             [0,-1 ]] )

        image=cv2.imread(path,0)
        image = image.astype('float64')
        image /=255.0
    
        # plt.imshow(edged_img,cmap='gray')
        return image,roberts_cross_x,roberts_cross_y
    def prewitt_operator(path):
        prewittX = [
            [-1,  0,  1],
            [-1,  0,  1],
            [-1,  0,  1]]
        prewittY = [
            [-1, -1, -1],
            [ 0,  0,  0],
            [ 1,  1,  1]]
        image=cv2.imread(path,0)

        return image,prewittX,prewittY
    def grad_magnitude(grad_x,grad_y):
        gradient_magnitude= np.sqrt( np.square(grad_x) + np.square(grad_y))
        gradient_magnitude*=255.0
        return gradient_magnitude 

    def saveoutputEdges(edgedimage):
        pathEdgedImg=f'./static/images/output/EdgedImg.jpg'
        cv2.imwrite(pathEdgedImg, edgedimage)
        return pathEdgedImg

            
