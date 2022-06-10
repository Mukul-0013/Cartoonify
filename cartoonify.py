import os
import cv2
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

#Checking if a proper image has been selected or not
def check_if_empty(img):
    i = cv2.imread(img)
    if i is None:
        #Error message
        messagebox.showerror("Error", "Please Select a proper Image")
        return 1
    else:
        return 0
    return

#Buttons located to the respective functions when pressed for desired cartoonification
def b1():
    org_img_add=filedialog.askopenfilename()
    if org_img_add == "":
        return
    modify_img(1,org_img_add)

def b2():
    org_img_add=filedialog.askopenfilename()
    if org_img_add == "":
        return
    modify_img(2,org_img_add)

def b3():
    org_img_add=filedialog.askopenfilename()
    if org_img_add == "":
        return
    modify_img(3,org_img_add)

def b4():
    org_img_add=filedialog.askopenfilename()
    if org_img_add == "":
        return
    modify_img(4,org_img_add)

def b5():
    org_img_add=filedialog.askopenfilename()
    if org_img_add == "":
        return
    modify_img(5,org_img_add)

def b6():
    org_img_add=filedialog.askopenfilename()
    if org_img_add == "":
        return
    modify_img(6,org_img_add)

def modify_img(num,org_img_add):

    #If a proper image is not selected then a error message prompts
    if(check_if_empty(org_img_add)):
        return

    #Reading the Image
    org_img = cv2.imread(org_img_add)
    org_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB)

    #Resizing the image if image is large
    if(org_img.shape[0]>1400 or org_img.shape[1]>1400):
        print('Original Dimensions : ',org_img.shape)
        # scale_per = 40
        # if(org_img.shape[0]<=3000 and org_img.shape[1]<=3000):
        #     scale_per = 60
        # elif(org_img.shape[0]<=4500 and org_img.shape[1]<=4500):
        #     scale_per = 40 # percent of original size
        # elif(org_img.shape[0]<10000 and org_img.shape[1]<10000):
        #     scale_per = 20 # percent of original size
        scale_per=min((140000/org_img.shape[0]),(140000/org_img.shape[1]))
        w = int(org_img.shape[1] * scale_per / 100)
        h = int(org_img.shape[0] * scale_per / 100)
        dim = (w, h)
        # resizing the image
        org_img = cv2.resize(org_img, dim, interpolation = cv2.INTER_AREA)
        print('Resized Dimensions : ',org_img.shape)


    #Smooth Outlines
    if(num==1):
        grey= cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
        medblur = cv2.medianBlur(grey, 3)
        adap_threshold = cv2.adaptiveThreshold(medblur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 7, 5)
        # blur = cv2.GaussianBlur(org_img, (9,9) ,cv2.BORDER_DEFAULT)
        blur= cv2.edgePreservingFilter(org_img, flags=1, sigma_s=60, sigma_r=0.4)

        final_img = cv2.bitwise_and(blur ,blur, mask=adap_threshold)
        final_img = cv2.cvtColor(final_img, cv2.COLOR_RGB2BGR)
        cv2.imshow('Smooth Outlines',final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        save("Smooth_img",final_img, org_img_add)

    #Black Board & Chalks
    elif(num==2):
        # blur = cv2.GaussianBlur(org_img, (3,3) ,cv2.BORDER_DEFAULT)
        blur = cv2.GaussianBlur(org_img, (3,3) ,0)
        canny= cv2.Canny(blur,100,150)
        final_img = cv2.bitwise_and(blur, blur, mask=canny)
        final_img = cv2.cvtColor(final_img, cv2.COLOR_RGB2BGR)
        cv2.imshow('Black Board & Chalks',final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        save("BlackBoard_img",final_img, org_img_add)

    #Black Pen Sketch
    elif(num==3):
        grey= cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
        medblur = cv2.medianBlur(grey, 3)
        adap_threshold = cv2.adaptiveThreshold(medblur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 5, 2)
        final_img = adap_threshold
        final_img = cv2.cvtColor(final_img, cv2.COLOR_RGB2BGR)
        cv2.imshow('Black Pen Sketch',final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        save("BlackPen_img",final_img, org_img_add)

    #Pencil Sketch
    elif(num==4):
        pencil, colour = cv2.pencilSketch(org_img, sigma_s=80, sigma_r=0.09, shade_factor=0.13)
        final_img = cv2.cvtColor(pencil, cv2.COLOR_RGB2BGR)
        cv2.imshow('Pencil Sketch',final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        save("Pencil_img",final_img, org_img_add)

    #Colour Pencil
    elif(num==5):
        pencil, colour = cv2.pencilSketch(org_img, sigma_s=60, sigma_r=0.09, shade_factor=0.05)
        final_img = cv2.cvtColor(colour, cv2.COLOR_RGB2BGR)
        cv2.imshow('Colour Pencil Sketch',final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        save("ColourPencil_img",final_img, org_img_add)

    #Crayons
    elif(num==6):
        crayons = cv2.stylization(org_img, sigma_s=60, sigma_r=0.09)
        final_img = cv2.cvtColor(crayons, cv2.COLOR_RGB2BGR)
        cv2.imshow('Crayons',final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        save("Crayons_img",final_img, org_img_add)

#Saving the Image
def save(img,final_img, org_img_add):
    add = os.path.dirname(org_img_add)
    e=os.path.splitext(org_img_add)
    org_img_name=e[0].split('/')[-1]
    img=img+"_"+org_img_name
    wholeAdd = os.path.join(add, img+e[1])
    cv2.imwrite(wholeAdd,final_img )

#tkinter panel making and assigning buttons
def main():

    #Fonts for the buttons
    Font_b1 = ("Comic Sans MS", 14, "bold")
    Font_b2= ("Chalkduster", 13)
    Font_b3= ("Marker Felt", 14, "bold")
    Font_b4= ("Papyrus", 14,"bold")
    Font_b5= ("Palatino", 14,"bold")
    Font_b6= ("Chalboard SE", 15,"bold")
    Font_lab=("Arial Hebrew", 17 , "bold")

    #Application window
    panel=tkinter.Tk()
    panel.geometry('525x225')
    panel.title('Cartoonifying an Image')
    Label(panel, text="Click to cartoonify an image by selecting a cartoonification:", font=Font_lab).place(x=2,y=10)

    #Buttons
    #Smooth Outlines
    Button(panel,text="Smooth Outlines", command=b1,font=Font_b1,height= 3, width=13).place(x=10, y=50)
    #Black Board & Chalks
    Button(panel,text="Black Board & Chalks", command=b2,font=Font_b2,height= 3, width=20).place(x=140, y=50)
    #Black Pen Sketch
    Button(panel,text="Black Pen Sketch", command=b3,font=Font_b3,height= 4, width=15).place(x=330, y=50)
    #Pencil Sketch
    Button(panel,text="Pencil Sketch", command=b4,font=Font_b4,height= 3, width=12).place(x=50, y=150)
    #Colour Pencil
    Button(panel,text="Colour Pencil", command=b5,font=Font_b5,height= 3, width=15).place(x=180, y=150)
    #Crayons
    Button(panel,text="Crayons", command=b6,font=Font_b6,height= 3, width=15).place(x=310, y=150)
    panel.mainloop()

#Starting of the program
if __name__ == '__main__':
  main()
