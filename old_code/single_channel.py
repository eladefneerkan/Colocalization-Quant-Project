from ij import IJ
from trainableSegmentation import WekaSegmentation

imp = IJ.getImage()

#forced scale change
IJ.run(imp, "RGB Color", "")

CLASSIFIER_PATH = "/your/path/here.model"

ws = WekaSegmentation(imp)
ws.loadClassifier(CLASSIFIER_PATH)

result = ws.applyClassifier(imp)
result.setTitle("weka_seg_result")
result.show()

IJ.run(result, "8-bit", "")

IJ.setThreshold(result, 1, 255)

IJ.run(result, "Convert to Mask", "")

IJ.run(result, "Analyze Particles...", "show=Outlines display summarize exclude clear")
