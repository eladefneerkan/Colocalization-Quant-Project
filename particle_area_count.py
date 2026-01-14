# Author: Lucia Liu
# Purpose: Finds the number of particles and area of each particle for each channel in a .czi file
# Notes: Image that is dragged in must be multi-channel
# Last edited: 1/13/26

from ij import IJ, WindowManager, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from ij.measure import ResultsTable
from ij.gui import Overlay, Roi
from ij.plugin.frame import RoiManager

# Choose directory
'''
dc = DirectoryChooser("Choose folder to save output files in.")
output_dir = dc.getDirectory()

if output_dir is None:
    raise ValueError("No output directory selected.")
'''

# Get input image
imp = IJ.getImage()  # gets dragged-in image

if imp.getNChannels() == 1:
    image_titles = [imp.getTitle()]
else:
    IJ.run(imp, "Split Channels", "")
    image_titles = WindowManager.getImageTitles()


def apply_threshold():
    IJ.run("8-bit")
    IJ.run("Subtract Background...", "rolling=50")
    ip = dup.getProcessor()
    ip.setThreshold(20, 255)
    dup.updateAndDraw()
    IJ.run("Convert to Mask")


def analyze_particles(image):
    # set measurements
    IJ.run(image, "Set Measurements...", "area mean redirect=[" + image.getTitle() + "]")
    # redirect to original image (to get the mean gray value)
    # area = area of particle in micrometers
    # mean = mean gray value (brightness aka intensity)
    # centroid = average x and y center of particle

    # analyze particles
    IJ.run(image, "Analyze Particles...",
           "size=0.1-Infinity add display summarize exclude redirect=[" + image.getTitle() + "]")
    # 0.05-Infinity = filters out noise, only counts particles greater than 0.05
    # add = add to ROI manager
    # display = makes table of list of areas for each particle in an image
    # summarize = summarizes data (count, total area, avg size, % area) for each image
    # exclude = excludes the particles on the edges (since their real size might be bigger/smaller --> not accurate)

    overlay = Overlay()
    rm = RoiManager.getInstance()
    for roi in rm.getRoisAsArray():
        overlay.add(roi)

    return overlay


''''    
# Process images
for title in image_titles:
    image = WindowManager.getImage(title)
    #IJ.run(image, "Apply LUT", "lut=Green")
    fs = FileSaver(image)
    #fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_original.tif")  # save original image

    dup = image.duplicate()  # create duplicate so we keep the original image
    dup.show()
    WindowManager.setCurrentWindow(dup.getWindow())

    # set brightness
    dup.setDisplayRange(0, 75) 
    dup.updateAndDraw()

    # apply threshold
    apply_threshold()
    analyze_particles(dup)
'''

image = WindowManager.getImage(image_titles[0])

# set brightness
IJ.run(image, "Apply LUT", "lut=Green")
image.setDisplayRange(0, 75)
image.updateAndDraw()

fs = FileSaver(image)
# fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_original.tif")  # save original image

dup = image.duplicate()  # create duplicate so we keep the original image
dup.show()
WindowManager.setCurrentWindow(dup.getWindow())

# apply threshold
apply_threshold()
overlay = analyze_particles(dup)

image.setOverlay(overlay)
image.updateAndDraw()