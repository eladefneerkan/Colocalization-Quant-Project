# Author: Lucia Liu
# Purpose: Finds the number of particles and area of each particle for each channel in a .czi file
# Notes: Image that is dragged in must be multi-channel
# Last edited: 12/16/25

from ij import IJ, WindowManager, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from ij.measure import ResultsTable
from ij.gui import Plot
from ij.plugin.frame import RoiManager

# Choose directory
dc = DirectoryChooser("Choose folder to save output files in.")
output_dir = dc.getDirectory()

if output_dir is None:
    raise ValueError("No output directory selected.")

# Get input image
imp = IJ.getImage()  # gets dragged-in image

if not imp.getTitle().lower().endswith(".czi"):
    raise ValueError("Incompatible file type - must be a multichannel .czi file")

IJ.run(imp, "Split Channels", "")
image_titles = WindowManager.getImageTitles()

'''
def graph_histogram(rt):
	area = rt.getColumnAsDoubles(rt.getColumnIndex("Area"))
	plot = Plot("Raw Distribution of Areas", "Area", "Frequency")
	plot.addHistogram(area)
	plot.show()
'''

# Process images
for title in image_titles:
    image = WindowManager.getImage(title)

    fs = FileSaver(image)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_original.tif")  # save original image

    dup = image.duplicate()  # create duplicate so we keep the original image
    dup.show()
    WindowManager.setCurrentWindow(dup.getWindow())

    # apply threshold
    IJ.run("8-bit")
    IJ.run("Subtract Background...", "rolling=50")
    IJ.run("Auto Threshold", "method=Otsu white")
    IJ.run("Convert to Mask")

    fs = FileSaver(dup)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_thresholded.tif")  # save thresholded image

    # set measurements
    IJ.run(dup, "Set Measurements...", "area mean centroid redirect=[" + image.getTitle() + "]")
    # redirect to original image (to get the mean gray value)
    # area = area of particle in micrometers
    # mean = mean gray value (brightness aka intensity)
    # centroid = average x and y center of particle

    # analyze particles
    IJ.run(dup, "Analyze Particles...",
           "size=0.1-Infinity show=Outlines display summarize exclude redirect=[" + image.getTitle() + "]")
    # 0.1-Infinity = filters out noise, only counts particles greater than 0.1
    # Outlines = shows image w/ outline and numbered particles
    # display = makes table of list of areas for each particle in an image
    # summarize = summarizes data (count, total area, avg size, % area) for each image
    # exclude = excludes the particles on the edges (since their real size might be bigger/smaller --> not accurate)
    # add = add ROIs (Region of Interest) to ROI Manager

    outline_img = WindowManager.getCurrentImage()
    fs = FileSaver(outline_img)
    fs.saveAsTiff(output_dir + title.replace(".czi", "") + "_outline.tif")  # save outline image

    rt = ResultsTable.getResultsTable()
    rt.save(output_dir + title.replace(".czi", "") + "_results.csv")
    rt.reset()

    # close images to avoid clutter --> comment out following if you want to see them
    image.changes = False
    image.close()
    dup.changes = False
    dup.close()
    outline_img.changes = False
    outline_img.close()
    rt_window = WindowManager.getFrame("Results")
    if rt_window is not None:
        rt_window.close()

# save summary
summary = ResultsTable.getResultsTable("Summary")
summary.save(output_dir + imp.getTitle().replace(".czi", "") + "_summary.csv")
summary_window = WindowManager.getFrame("Summary")
if summary_window is not None:
    summary_window.close()  # close summary window