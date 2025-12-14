from ij import IJ, WindowManager, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from ij.measure import ResultsTable

# Choose directory
dc = DirectoryChooser("Choose folder to save output files in.")
output_dir = dc.getDirectory()

if output_dir is None:
    raise ValueError("No output directory selected.")

# Get input image
imp = IJ.getImage()  # gets dragged-in image

if not imp.getTitle().lower().endswith(".czi"):
    raise ValueError("Incompatible file type - must be a .czi file")

IJ.run(imp, "Split Channels", "")
image_titles = WindowManager.getImageTitles()