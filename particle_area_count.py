# Author: Lucia Liu
# Purpose: Finds the number of particles and area of each particle for each channel in a .czi file
# Notes: Image that is dragged in must be multi-channel
# Last edited: 1/13/26

from ij import IJ, WindowManager, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from ij.measure import ResultsTable
from ij.gui import Overlay, Roi
from ij.plugin.frame import RoiManager

IMG_MAX = 75  # lower max to brighten image
THRESHOLD_MIN = 20  # lower threshold to recognize more particles


def adjust_brightness(image, max):
    edited_image = image.duplicate()
    IJ.run(edited_image, "8-bit", "")
    ip = edited_image.getProcessor()
    scale = 255 / (max - 0)
    ip.multiply(scale)
    edited_image.updateAndDraw()
    return edited_image


def apply_threshold(image, min):
    IJ.run("8-bit")
    IJ.run("Subtract Background...", "rolling=50")
    ip = image.getProcessor()
    ip.setThreshold(min, 255)
    image.updateAndDraw()
    IJ.run("Convert to Mask")
    return image


def analyze_particles(image):
    # set measurements
    IJ.run(image, "Set Measurements...", "area mean redirect=[" + image.getTitle() + "]")
    # redirect to original image (to get the mean gray value)
    # area = area of particle in micrometers
    # mean = mean gray value (brightness aka intensity)

    # analyze particles
    IJ.run(image, "Analyze Particles...",
           "size=0.1-Infinity show=Outlines add display summarize include exclude redirect=[" + image.getTitle() + "]")
    # 0.1-Infinity = filters out noise, only counts particles greater than 0.1 µm^2
    # Outlines = shows image w/ outline and numbered particles
    # add = add to ROI manager
    # display = makes table of list of areas for each particle in an image
    # summarize = summarizes data (count, total area, avg size, % area) for each image
    # exclude = excludes the particles on the edges (since their real size might be bigger/smaller --> not accurate)
    # include = include holes

    outline = WindowManager.getCurrentImage()

    overlay = Overlay()
    rm = RoiManager.getInstance()
    for roi in rm.getRoisAsArray():
        overlay.add(roi)
    rm.reset()
    rm.setVisible(False)

    results = ResultsTable.getResultsTable()
    summary = ResultsTable.getResultsTable("Summary")

    return outline, overlay, results, summary


def main():
    # Choose directory
    dc = DirectoryChooser("Choose folder to save output files in.")
    output_dir = dc.getDirectory()

    if output_dir is None:
        raise ValueError("No output directory selected.")

    # Get input image
    imp = IJ.getImage()  # gets dragged-in image

    if imp.getNChannels() == 1:
        image_titles = [imp.getTitle()]
    else:
        IJ.run(imp, "Split Channels", "")
        image_titles = WindowManager.getImageTitles()

    title = image_titles[0]  # 1st channel
    image = WindowManager.getImage(title)

    fs = FileSaver(image)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_original.tif")  # save original image

    # adjust brightness
    edited_image = adjust_brightness(image, IMG_MAX)
    fs = FileSaver(edited_image)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_edited.tif")  # save image with adjusted brightness

    # create duplicate to apply threshold
    dup = image.duplicate()
    dup.show()
    WindowManager.setCurrentWindow(dup.getWindow())

    # apply threshold
    apply_threshold(dup, THRESHOLD_MIN)
    fs = FileSaver(dup)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_thresholded.tif")

    # analyze particles
    outline, overlay, results, summary = analyze_particles(dup)
    edited_image.setOverlay(overlay)
    edited_image.updateAndDraw()
    flattened = edited_image.flatten()

    # save results
    fs = FileSaver(flattened)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_overlay.tif")
    fs = FileSaver(outline)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_outline.tif")
    results.save(output_dir + title.replace(".czi", "") + "_results.csv")
    results.reset()
    summary.save(output_dir + imp.getTitle().replace(".czi", "") + "_summary.csv")

    # close windows
    image.changes = False
    image.close()
    dup.changes = False
    dup.close()
    outline.changes = False
    outline.close()
    results_window = WindowManager.getFrame("Results")
    if results_window is not None:
        results_window.close()
    summary_window = WindowManager.getFrame("Summary")
    if summary_window is not None:
        summary_window.close()


main()