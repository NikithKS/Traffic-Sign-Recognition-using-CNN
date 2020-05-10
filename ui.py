from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy
from keras.models import load_model

model=load_model('tsr-fin.h5')
labels={0: 'Uneven Road',
        1: 'Road Hump',
        2: 'Slippery Road',
        3: 'Speed limit 20',
        4: 'Speed limit 30',
        5: 'Speed limit 50',
        6: 'Speed limit 60',
        7: 'School Zone',
        8: 'Cyclists',
        9: 'Cattle crossing',
        10: 'Roadworks',
        11: 'Traffic Signals',
        12: 'Railway crossing ahead',
        13: 'Speed limit 100',
        14: 'Narrow Road',
        15: 'Lane ends',
        16: 'Turn left or straight ahead',
        17: 'Speed limit 120',
        18: 'Crossroads',
        19: 'Give Way',
        20: 'Stop',
        21: 'No Entry',
        22: 'Pedastrian Crossing',
        23: 'Turn left ahead',
        24: 'Turn right ahead',
        25: 'No parking',
        26: 'No left turn',
        27: 'No right turn',
        28: 'Straight ahead',
        29: 'Turn right or straight ahead',
        30: 'Right hand curve',
        31: 'No Stopping',
        32: 'Parking',
        33: 'End of all restrictions',
        34: 'Speed limit 80',
        35: 'Left hand curve'
}
uploaded=False
img=Image.new('RGB',(300,300))
path=""
result=""


def upload():
    global classify_but, img, path, uploaded, canvas
    try:
        canvas.destroy()
    except:
        print("canvas")
    path=filedialog.askopenfilename()
    img=Image.open(path)
    img=ImageTk.PhotoImage(img)
    canvas= Canvas(window,width=300,height=300)
    canvas.create_image(20, 20, anchor=NW, image=img)
    canvas.pack()
    uploaded=True
    classify_but.config(bg="#00e5ff")

def classify():
    if(not uploaded):
        print("class")
        return
    global path
    img=Image.open(path)
    img=img.resize((30,30))
    img=numpy.expand_dims(img,axis=0)
    img=numpy.array(img)
    pred=model.predict_classes([img])[0]
    result=labels[pred]
    result_label.config(text=result)


window=Tk()
window.title('Traffic Sign Recognition using CNN')
window.geometry('600x400')

top_frame=Frame(window,bg='grey', width=600, height=40)
top_frame.pack(side=TOP)
top_frame.pack_propagate(0)

name_but=Button(top_frame,text='Traffic Sign recognition', bg='#00e5ff',font=('dseg'))
name_but.pack()

upload_but=Button(window,text='Upload Sign', bg='#00e5ff',font=('bold'),padx=15, command=lambda:upload())
upload_but.place(relx=0.78,rely=0.40)

classify_but=Button(window,text='Classify Sign', bg='grey',font=('bold'),padx=13,command=lambda:classify())
classify_but.place(relx=0.78,rely=0.50)

bottom_frame=Frame(window,bg='grey', width=600, height=40)
bottom_frame.pack(side=BOTTOM)
bottom_frame.pack_propagate(0)

result_label=Label(bottom_frame,text=result,font=('bold',20),bg="grey")
result_label.pack(side=BOTTOM)


canvas= Canvas(window,width=300,height=300)

window.mainloop()
