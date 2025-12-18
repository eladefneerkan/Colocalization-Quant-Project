from ij import IJ
from trainableSegmentation import WekaSegmentation
import os

CLASSIFIER_PATH = "local path" 
MIN_PARTICLE_SIZE = 0.1   #µm^2 (pixels if no calibration)
SG_MIN = 2 
SG_MAX = 2
SAVE_OUTPUT = False       #set True if you want to save files
OUTPUT_DIR = "where to save (local path)"

#image (opened via Bio-Formats as hyperstack)
imp = IJ.getImage()

ws = WekaSegmentation(imp)
ws.loadClassifier(CLASSIFIER_PATH)

result = ws.applyClassifier(imp)
result_title = imp.getTitle() + "_weka_seg"
result.setTitle(result_title)
result.show()

#ensure 8-bit
IJ.run(result, "8-bit", "")

#isolate Class 1 (SG) only
IJ.setThreshold(result, SG_MIN, SG_MAX)
IJ.run(result, "Convert to Mask", "")   #binary mask of SGs only

#analyze particles on SG mask
particle_args = (
    "size=" + str(MIN_PARTICLE_SIZE) + "-Infinity "
    "show=Outlines display summarize exclude clear"
)
IJ.run(result, "Analyze Particles...", particle_args)


if SAVE_OUTPUT:
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    #SG mask
    mask_path = os.path.join(OUTPUT_DIR, result_title + "_SG_mask.tif")
    IJ.saveAs(result, "Tiff", mask_path)

    #outlines
    from ij import WindowManager
    for title in WindowManager.getImageTitles():
        if title.startswith("Drawing of " + result_title):
            outlines_imp = WindowManager.getImage(title)
            outlines_path = os.path.join(OUTPUT_DIR, result_title + "_SG_outlines.tif")
            IJ.saveAs(outlines_imp, "Tiff", outlines_path)
            break

    #CSV
    csv_path = os.path.join(OUTPUT_DIR, imp.getTitle() + "_SG_results.csv")
    IJ.saveAs("Results", csv_path)

print("Done: classified, isolated SG class, and analyzed particles.")
