from ij import IJ, WindowManager  #From threshold_area_count (unedited)
from trainableSegmentation import WekaSegmentation  # NEW (WEKA)

imp = IJ.getImage() #From threshold_area_count (unedited)

if not imp.getTitle().lower().endswith(".czi"): #From threshold_area_count (unedited)
    raise ValueError("Incompatible file type - must be a .czi file")  #From threshold_area_count (unedited)

IJ.run(imp, "Split Channels", "")  #From threshold_area_count (unedited)
image_titles = WindowManager.getImageTitles()  #From threshold_area_count (unedited)


#look at the end of file intructions for more clarity for line 15
CLASSIFIER_PATH = "/path/to/your_weka_model.model" 

for title in image_titles:  #From threshold_area_count (unedited)
    img = WindowManager.getImage(title)  #addition
    dup = img.duplicate()                #addition
    dup.setTitle(title + "_dup")         #addition
    dup.show()  #From threshold_area_count (unedited)

    ws = WekaSegmentation(dup) 

    # load previously trained model (look at the end of file instructions)
    ws.loadClassifier(CLASSIFIER_PATH)  

    result = ws.applyClassifier(dup) 
    result.setTitle(title + "_weka_seg")
    result.show()

    IJ.run(result, "8-bit", "") #From threshold_area_count (edited)

    #look at the second part of end of file instructions
    IJ.setThreshold(result, 1, 255) 

    IJ.run(result, "Convert to Mask", "")   #From threshold_area_count (edited)

    IJ.run(result, "Analyze Particles...", "show=Outlines display summarize exclude clear") #From threshold_area_count (edited)


'''
1) Train with Weka
    a) open image first through BiOP
    b) Plugins → Segmentation → Trainable Weka Segmentation
    c) train by drawing classes
    d) save results to .model file
2) update this line to .model file path
    CLASSIFIER_PATH = "/absolute/path/to/your/model.model"
3) open script in Fiji + run
    Plugins → New → Script
'''

'''
Open the image in Fiji and the threshold edit page
Use sliders to find min and max values for proper isolation
Place into script
IJ.setThreshold(placeholder, min_value, max_value)
'''