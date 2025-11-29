# Author: Lucia Liu
# Purpose: Finds the number of particles and area of each particle for each channel in a .czi file 
# Last edited: 11/28/25

from ij import IJ, WindowManager

imp = IJ.getImage()  # gets dragged-in image

if not imp.getTitle().lower().endswith(".czi"):
    raise ValueError("Incompatible file type - must be a .czi file")

IJ.run(imp, "Split Channels", "")
image_titles = WindowManager.getImageTitles()

for title in image_titles:
    dup = WindowManager.getImage(title).duplicate()  # create duplicate so we keep the original image
    dup.show()
    WindowManager.setCurrentWindow(dup.getWindow())

    # apply threshold
    IJ.run("8-bit")
    IJ.run("Auto Threshold", "method=Default dark")
    IJ.run("Convert to Mask", "method=Default background=Dark")

    # analyze particles
    IJ.run(dup, "Analyze Particles...", "show=Outlines display summarize exclude")
        # Outlines = shows image w/ outline and numbered particles
        # display = makes table of list of areas for each particle in an image
        # summarize = summarizes data (count, total area, avg size, % area) for each image
        # exclude = excludes the particles on the edges (since their real size might be bigger/smaller --> not accurate)