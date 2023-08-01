from flask import Flask, render_template, request
from flask_cors import CORS
import os
import base64  # convert from string to  bits
import json
import cv2
import numpy as np
import time
import calendar
import Histograms as hi
from Filters import Filters as Fl
import Frequency as hs2


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

CORS(app)


@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("filter.html")


@app.route("/makeHybridImages", methods=["GET", "POST"])
def makeHybridImages():

    if request.method == "POST":

        imageA_data = base64.b64decode(
            request.form["imageA_data"].split(',')[1])
        imageB_data = base64.b64decode(
            request.form["imageB_data"].split(',')[1])
        filters_option = int(request.form["filters_option"])
        lpf_D0 = int(request.form["lpf_D0"])
        hpf_D0 = int(request.form["hpf_D0"])

        print(type(filters_option))

        imgA_path = hi.saveImage(imageA_data, "imageA")
        imgB_path = hi.saveImage(imageB_data, "imageB")

        result = hi.makeImg(imgA_path, imgB_path,
                            filters_option, lpf_D0, hpf_D0)

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        return json.dumps({1: f'<img src="{result}?t={time_stamp}" id="imageC" alt="" >'})

    else:
        return render_template("makeHybridImages.html")


@app.route("/saveImg", methods=["GET", "POST"])
def saveImag():
    if request.method == "POST":

        pathNoise = ""
        pathFilter = ""
        imageA_data = base64.b64decode(request.form["path"].split(',')[1])
        Noise_type = request.form["Noise_type"]
        Filter_Type = request.form["Filter_Type"]
        SizeFilter = int(request.form["SizeFilter"])

        path = hi.saveImage(imageA_data, "inputfilterImage")

        if Noise_type == "Uniform":
            noiseImage = Fl.addUniformNoise(path)
            pathNoise = Fl.saveoutputNoise(noiseImage)

        if Noise_type == "Gaussian":
            noiseImage = Fl.addGaussianNoise(path)
            pathNoise = Fl.saveoutputNoise(noiseImage)

        if Noise_type == "Salt":
            noiseImage = Fl.add_salt_noise(path)
            pathNoise = Fl.saveoutputNoise(noiseImage)

        if Filter_Type == "Gaussian":
            filter = Fl.Gaussian_filter(SizeFilter)
            outputimage = Fl.convolve2D(cv2.imread(pathNoise, 0), filter)
            pathFilter = Fl.saveoutputFilter(outputimage)

        if Filter_Type == "Average":
            filter = Fl.Gaussian_filter(SizeFilter)
            outputimage = Fl.convolve2D(cv2.imread(pathNoise, 0), filter)
            pathFilter = Fl.saveoutputFilter(outputimage)

        if Filter_Type == "Median":
            outputimage = Fl.median_Filter(
                SizeFilter, cv2.imread(pathNoise, 0))
            pathFilter = Fl.saveoutputFilter(outputimage)

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        return json.dumps({1: f'<img src="{pathNoise}?t={time_stamp}" id="Addnoise" alt="" >',
                           2: f'<img src="{pathFilter}?t={time_stamp}" id="ApplyFilter" alt="" >'})

    else:
        return render_template("filter.html")


@app.route("/normalization", methods=["GET", "POST"])
def normalization():
    return render_template("normalization.html")


@app.route("/normalizationserver", methods=["GET", "POST"])
def normalizationserver():
    if request.method == "POST":
        path2 = ""
        histogramoutputimage = ""
        image = base64.b64decode(request.form["path"].split(',')[1])
        selectionBox = request.form["option"]
        path = hi.saveImage(image, "normalizationinputimage")
        histograminputimage = hs2.flatten(path)

        if selectionBox == "equalization":
            path2 = hs2.histogramEqual(path)
        #   os.remove(f'./static/images/output/histogramoutPut.jpg')
            histogramoutputimage = hs2.flatten(path="", path2=path2)

        if selectionBox == "normalization":
            path2 = hs2.normlazition(path)
        #   os.remove(f'./static/images/output/histogramoutPut.jpg')
            histogramoutputimage = hs2.flatten(path="", path2=path2)

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    return json.dumps({1: f'<img src="{histograminputimage}?t={time_stamp}" id="imageoutput" alt="" >',
                       2: f'<img src="{path2}?t={time_stamp}" id="imageNormalization" alt="" >',
                       3: f'<img src="{histogramoutputimage}?t={time_stamp}" id="histimageNormalization" alt="" >'})


@app.route("/edgedetection", methods=["GET", "POST"])
def edgedetection():
    return render_template("edge.html")


@app.route("/edgeImg", methods=["GET", "POST"])
def edgeImg():
    if request.method == "POST":

        pathEdge = ""
        image_data = base64.b64decode(request.form["path"].split(',')[1])
        Edge_method = request.form["edgedetectmethod"]

        path = hi.saveImage(image_data, "inputEdgeImage")

    if Edge_method == "Sobel":
        image, filter_x, filter_y = Fl.sobel_operator(path)
        gradient_x = Fl.convolve2D(image, filter_x)
        gradient_y = Fl.convolve2D(image, filter_y)
        edgedImage = Fl.grad_magnitude(gradient_x, gradient_y)
        edgedImage *= 255.0 / edgedImage.max()
        pathEdgedImg = Fl.saveoutputEdges(edgedImage)

    if Edge_method == "Roberts":
        image, filter_x, filter_y = Fl.roberts_operator(path)
        gradient_x = Fl.convolve2D(image, filter_x)
        gradient_y = Fl.convolve2D(image, filter_y)
        edgedImage = Fl.grad_magnitude(gradient_x, gradient_y)
        pathEdgedImg = Fl.saveoutputEdges(edgedImage)

    if Edge_method == "Prewitt":
        image, filter_x, filter_y = Fl.prewitt_operator(path)
        gradient_x = Fl.convolve2D(image, filter_x)
        gradient_y = Fl.convolve2D(image, filter_y)
        edgedImage = Fl.grad_magnitude(gradient_x, gradient_y)
        edgedImage /= 255.0
        pathEdgedImg = Fl.saveoutputEdges(edgedImage)

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    return json.dumps({1: f'<img src="{pathEdgedImg}?t={time_stamp}" id="ApplyEdges" alt="" >'})


@app.route("/histograms", methods=["GET", "POST"])
def histograms():
    if request.method == "POST":
        imageA_data = base64.b64decode(
            request.form["imageA_data"].split(',')[1])

        histogram_types = int(request.form["histogram_types"])

        if histogram_types == 0:
            imgA_path = hi.saveImage(imageA_data, "histo_img")
            resultHisto = hs2.plot_red_hist(
                imgA_path, "static/images/red_histo_img.jpg")

        elif histogram_types == 1:
            imgA_path = hi.saveImage(imageA_data, "histo_img")
            resultHisto = hs2.plot_green_hist(
                imgA_path, "static/images/green_histo_img.jpg")

        elif histogram_types == 2:
            imgA_path = hi.saveImage(imageA_data, "histo_img")
            resultHisto = hs2.plot_blue_hist(
                imgA_path, "static/images/blue_histo_img.jpg")

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        return json.dumps({1: f'<img src="{resultHisto}?t={time_stamp}" id="imageC" alt="" >'})

    else:
        return render_template("histograms.html")


if __name__ == "__main__":
    app.run(port=7750, debug=True)
