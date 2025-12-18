from ij import IJ, WindowManager, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
from trainableSegmentation import WekaSegmentation
import os

# Settings
CLASSIFIER_PATH = "local path to classifier"   # DON'T FORGET TO ADD THIS
MIN_PARTICLE_SIZE = 0.1    # µm^2 (pixels if no calibration)
SG_MIN = 2                 # Weka class range min (leave as is if you're unsure)
SG_MAX = 2                 # Weka class range max (leave as is if you're unsure)
SAVE_SG_OUTPUT = True

# Choose Directory
dc = DirectoryChooser("Choose folder to save output files in.")
output_dir = dc.getDirectory()
if output_dir is None:
    raise ValueError("No output directory selected.")

# error check
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

# get input
imp = IJ.getImage()  # opened via Bio-Formats as hyperstack

# Apply Weka Segmentation to Input
ws = WekaSegmentation(imp)
ws.loadClassifier(CLASSIFIER_PATH)

weka_result = ws.applyClassifier(imp)
weka_title = imp.getTitle() + "_weka_seg"
weka_result.setTitle(weka_title)
weka_result.show()

# error check
IJ.run(weka_result, "8-bit", "")

# isolate Class 1 (SG) only
IJ.setThreshold(weka_result, SG_MIN, SG_MAX)
IJ.run(weka_result, "Convert to Mask", "")

# analyze particles on SG mask
particle_args = (
    "size=" + str(MIN_PARTICLE_SIZE) + "-Infinity "
    "show=Outlines display summarize exclude clear"
)
IJ.run(weka_result, "Analyze Particles...", particle_args)

# save SG-related outputs
from ij import WindowManager as WM

if SAVE_SG_OUTPUT:
    # SG mask
    mask_path = os.path.join(output_dir, weka_title + "_SG_mask.tif")
    IJ.saveAs(weka_result, "Tiff", mask_path)

    # SG outlines
    outlines_imp = None
    for title in WM.getImageTitles():
        if title.startswith("Drawing of " + weka_title):
            outlines_imp = WM.getImage(title)
            outlines_path = os.path.join(output_dir, weka_title + "_SG_outlines.tif")
            IJ.saveAs(outlines_imp, "Tiff", outlines_path)
            break

    # SG results table
    csv_path = os.path.join(output_dir, imp.getTitle() + "_SG_results.csv")
    IJ.saveAs("Results", csv_path)

# close Weka images & results to avoid clutter / cross-contamination
if outlines_imp is not None:
    outlines_imp.changes = False
    outlines_imp.close()

weka_result.changes = False
weka_result.close()

# clear Results and Summary tables after Weka step
rt = ResultsTable.getResultsTable()
rt.reset()
rt_window = WM.getFrame("Results")
if rt_window is not None:
    rt_window.close()

summary = ResultsTable.getResultsTable("Summary")
if summary is not None:
    summary.reset()
summary_window = WM.getFrame("Summary")
if summary_window is not None:
    summary_window.close()


# Particle Analysis for each Channel

# determine number of channels
if imp.getNChannels() == 1:
    image_titles = [imp.getTitle()]
else:
    IJ.run(imp, "Split Channels", "")
    image_titles = WM.getImageTitles()

# process each image
for title in image_titles:
    image = WM.getImage(title)

    if image is None:
        continue

    # save original image
    fs = FileSaver(image)
    fs.saveAsTiff(os.path.join(output_dir, title.replace(".czi", "") + "_original.tif"))

    # create duplicate so we keep the original image
    dup = image.duplicate()
    dup.show()
    WM.setCurrentWindow(dup.getWindow())

    # apply threshold
    IJ.run("8-bit")
    IJ.run("Subtract Background...", "rolling=50")
    IJ.run("Auto Threshold", "method=MaxEntropy")
    IJ.run("Convert to Mask")

    # save thresholded image
    fs = FileSaver(dup)
    fs.saveAsTiff(os.path.join(output_dir, title.replace(".czi", "") + "_thresholded.tif"))

    # set measurements
    IJ.run(dup, "Set Measurements...", "area mean centroid redirect=[" + image.getTitle() + "]")
    # set measurements (redirect to original for mean gray value)
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

    # save outline image
    outline_img = WM.getCurrentImage()
    fs = FileSaver(outline_img)
    fs.saveAsTiff(os.path.join(output_dir, title.replace(".czi", "") + "_outline.tif"))

    # save Results CSV + reset table
    rt = ResultsTable.getResultsTable()
    rt.save(os.path.join(output_dir, title.replace(".czi", "") + "_results.csv"))
    rt.reset()

    # close images to avoid clutter --> comment out the following if you want to see them
    image.changes = False
    image.close()
    dup.changes = False
    dup.close()
    outline_img.changes = False
    outline_img.close()

    rt_window = WM.getFrame("Results")
    if rt_window is not None:
        rt_window.close()

# save global summary table
summary = ResultsTable.getResultsTable("Summary")
if summary is not None:
    summary.save(os.path.join(output_dir, imp.getTitle().replace(".czi", "") + "_summary.csv"))

summary_window = WM.getFrame("Summary")
if summary_window is not None:
    summary_window.close()

print("Done: Weka classification + SG analysis + channel-wise threshold analysis.")
