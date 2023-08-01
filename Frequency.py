
from IPython.display import display, Math, Latex
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import os
import cv2
import numpy as np
import numpy as np


def flatten(path="", path2=""):
    plt.clf()
    if path2 != "":
        img2 = Image.open(path2)
        img2 = np.asarray(img2)
        flat_image2 = img2.flatten()
        pathhistogramOutput = f'./static/images/output/histogramoutPut.jpg'

        plt.hist(flat_image2, 255)
        plt.ylim((0, 6000))
        plt.savefig(pathhistogramOutput)

        return pathhistogramOutput

    else:
        img = Image.open(path)
        img = np.asarray(img)
        flat_image = img.flatten()
        pathhistogram = f'./static/images/output/histogram.jpg'

        plt.hist(flat_image, 255)
        plt.ylim(0, 6000)
        plt.savefig(pathhistogram)

        return pathhistogram


def get_histogram(path, bins):
    img = Image.open(path)
    img = np.asarray(img)
    flat_image = img.flatten()
    histogram = np.zeros(bins)

    for pixel in flat_image:
        histogram[pixel] += 1

    return histogram


def cumsum(a):
    a = iter(a)
    b = [next(a)]
    for i in a:
        b.append(b[-1] + i)
    return np.array(b)


def saveCumsum(path, bins):
    hist = get_histogram(path, bins)
    cums = cumsum(hist)
    pathcs = f'./static/images/output/cumsum.jpg'
    os.remove(pathcs)
    plt.plot(cums)
    plt.savefig(pathcs)


def normCumsum(path, bins):
    hist = get_histogram(path, bins)
    cums = cumsum(hist)
    return cums


def normlazition(path, bins=256):
    normalizecs = normCumsum(path, bins)
    img = Image.open(path)
    img = np.asarray(img)

    flat_image = img.flatten()
    nj = (normalizecs - normalizecs.min()) * 255
    N = normalizecs.max() - normalizecs.min()
    normalizecs = nj / N
    normalizecs = normalizecs.astype('uint8')
    img_new = normalizecs[flat_image]
    image_new = np.reshape(img_new, img.shape)

    filename = f'./static/images/output/normalizecs.jpg'
    os.remove(filename)
    cv2.imwrite(filename, image_new)

    return filename


def histogramEqual(path, bins=256):
    comulative = normCumsum(path, bins)
    img = Image.open(path)
    img = np.asarray(img)
    flat_image = img.flatten()

    img_new = comulative[flat_image]/255
    image_new = np.reshape(img_new, img.shape)

    filename = f'./static/images/output/histogramEqual.jpg'
    os.remove(filename)
    cv2.imwrite(filename, image_new)

    return filename


#  abdulrahman

def global_threshold(image, threshold_value):
    _, thresholded = cv2.threshold(
        image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded


def local_threshold(image, block_size, c):
    # block_size (int) is the size of the neighbourhood block
    # c (int) is the constant subtracted from the mean.
    thresholded = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c)
    return thresholded


def color_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def plot_red_hist(image_file, out_file):
    img = cv2.imread(image_file)
    # extract the red channel
    red_channel = img[:, :, 2]
    # calculate the histogram
    hist, bins = np.histogram(red_channel.ravel(), 256, [0, 256])
    # plot the histogram
    plt.hist(red_channel.ravel(), 256, [0, 256], color='red')
    plt.xlim([0, 256])
    plt.xlabel('Red Intensity')
    plt.ylabel('Frequency')
    plt.title('Red Channel Histogram')
    # save the figure as an image
    plt.savefig(out_file)
    # show the figure
    # plt.show()
    return out_file


def plot_green_hist(image_file, out_file):
    img = cv2.imread(image_file)
    # extract the green channel
    green_channel = img[:, :, 1]
    hist, bins = np.histogram(green_channel.ravel(), 256, [0, 256])
    plt.hist(green_channel.ravel(), 256, [0, 256], color='green')
    plt.xlim([0, 256])
    plt.xlabel('Green Intensity')
    plt.ylabel('Frequency')
    plt.title('Green Channel Histogram')

    plt.savefig(out_file)

    # plt.show()
    return out_file


def plot_blue_hist(image_file, out_file):
    img = cv2.imread(image_file)
    blue_channel = img[:, :, 0]
    hist, bins = np.histogram(blue_channel.ravel(), 256, [0, 256])
    plt.hist(blue_channel.ravel(), 256, [0, 256], color='blue')
    plt.xlim([0, 256])
    plt.xlabel('Blue Intensity')
    plt.ylabel('Frequency')
    plt.title('Blue Channel Histogram')
    plt.savefig(out_file)

    # plt.show()
    return out_file
