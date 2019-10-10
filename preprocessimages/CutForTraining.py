# cd /Users/miroslav.polacek/Dropbox\ \(VBC\)/'Group Folder Swarts'/Research/CNNRings/Mask_RCNN/preprocessImages

from PIL import Image
import os.path, sys
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
from shapely.geometry import box
matplotlib.rcParams['interactive'] == True

pathin = "/Users/miroslav.polacek/Documents/Process"
pathout = "/Users/miroslav.polacek/Documents/ToAnnotate"
#pathin = "/Volumes/swarts/lab/DendroImages/00008JPEG"
#pathout = "/Volumes/swarts/lab/DendroImages/ToAnnotate"

def CutTrain(pathin = pathin, pathout = pathout, overlap = 0):
    
    for f in os.listdir(pathin):
        if f.endswith('jpg'):
            print(f)
            im = Image.open(os.path.join(pathin,f))
            
            imgwidth, imgheight = im.size
            plt.figure()
            for i in range(0,imgwidth, int(imgheight-(imgheight*overlap))):
                b = (i, 0, (i+imgheight), imgheight)
                
                bplot = box(*b) #next 3 rows from here i just try to plot box on the image
                x,y = bplot.exterior.xy
                plt.plot(x,y)
                plt.imshow(im) #to plot an image that is being processed
                a = im.crop(b)
                a.save(os.path.join(pathout, str(i)+ '_' + f))
            plt.show()    

if __name__ == "__main__":
    CutTrain()
