from ij import IJ, WindowManager

IJ.open("/Users/lucialiu/Downloads/10_29_2025_fxr1_157W_PK/PK2_WT.czi")
IJ.run("Split Channels")
image_titles = WindowManager.getImageTitles()

for title in image_titles:
    imp = WindowManager.getImage(title)  # find window that matches title

    dup = imp.duplicate()  # create duplicate so we keep the original image
    dup.show()
    WindowManager.setCurrentWindow(dup.getWindow())

    # apply threshold
    IJ.run("8-bit")
    IJ.run("Auto Threshold", "method=Default dark")
    IJ.run("Convert to Mask", "method=Default background=Dark")

    # analyze particles
    IJ.run(dup, "Analyze Particles...", "show=Outlines display summarize exclude clear")