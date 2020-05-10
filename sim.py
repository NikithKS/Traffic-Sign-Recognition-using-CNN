from tkinter import *
import math
import random
import time
import threading
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy
from keras.models import load_model

model=load_model('tsr-fin.h5')
uploaded=False
img=Image.new('RGB',(300,300))
path=""
result=""
current=60

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

speeds={0: [30,-1],
        1: [20,-1],
        2: [30,30],
        3: [17,17],
        4: [26,26],
        5: [46,46],
        6: [55,55],
        7: [36,36],
        8: [36,36],
        9: [30,-1],
        10: [20,-1],
        11: [25,-1],
        12: [-1,-1],
        13: [95,96],
        14: [40,40],
        15: [40,-1],
        16: [-1,-1],
        17: [118,116],
        19: [-1,-1],
        20: [0, -1],
        21: [0, 60],
        22: [20,-1],
        23: [25,-1],
        24: [25,-1],
        25: [-1,-1],
        26: [-1,-1],
        27: [-1,-1],
        28: [-1,-1],
        29: [-1,-1],
        29: [-1,-1],
        31: [-1,-1],
        32: [-1,-1],
        33: [60,60],
        34: [78,75],
        35: [35,-1],
}

def point(speed):
    if(speed<0):
        speed=0
    global speedo,pointer,speed_label
    speed_radian=speed*math.pi/180
    # print(speed)
    x_end=100-80*math.cos(speed_radian)
    y_end=100-80*math.sin(speed_radian)
    speedo.coords(pointer,(100,100,x_end,y_end))
    speed_text=str(speed)
    speed_label.config(text=speed_text)
    threading.Thread(target=window.update()).start()

def shift(fro,to):
    if(fro>to):
        decrease(fro,to)
    elif(fro<to):
        increase(fro,to)


def increase(fro, to):
    while(fro<to):
        fro+=7
        point(fro)
        time.sleep(0.5)

def decrease(fro, to):
    while(fro>to):
        fro-=5
        point(fro)
        time.sleep(0.5)

def stay(speed):
    while(True):
        n=random.randint(-1,2)
        point(speed+n)
        time.sleep(0.5)

def upload():
    global classify_but, img, path, uploaded, canvas
    try:
        canvas.destroy()
    except:
        pass
    path=filedialog.askopenfilename()
    img=Image.open(path)
    img=ImageTk.PhotoImage(img)
    canvas= Canvas(window,width=300,height=300)
    canvas.create_image(20, 20, anchor=NW, image=img)
    canvas.pack(side=BOTTOM)
    uploaded=True
    classify_but.config(bg="#00e5ff")

def classify():
    if(not uploaded):
        print("Upload image")
        return
    global path
    img=Image.open(path)
    img=img.resize((30,30))
    img=numpy.expand_dims(img,axis=0)
    img=numpy.array(img)
    pred=model.predict_classes([img])[0]
    result=labels[pred]+" Detected"
    result_label.config(text=result)
    alter(pred)

def alter(pred):
    global current
    to_speed=speeds[pred][0]
    stay_speed=speeds[pred][1]
    if(to_speed>=0):
        shift(current,to_speed)
    if(stay_speed>=0):
        shift(to_speed,stay_speed)
        current=stay_speed
    elif(to_speed>=0):
        shift(to_speed,current)
    stay(current)


window=Tk()
window.title('Traffic Sign Recognition using CNN')
window.geometry('700x600')

top_frame=Frame(window,bg='grey', width=600, height=40)
top_frame.pack(side=TOP)
top_frame.pack_propagate(0)

name_but=Button(top_frame,text='Traffic Sign recognition', bg='#00e5ff',font=('dseg'))
name_but.pack()

upload_but=Button(window,text='Upload Sign', bg='#00e5ff',font=('bold'),padx=15, command=lambda:upload())
upload_but.place(relx=0.78,rely=0.40)

classify_but=Button(window,text='Classify Sign', bg='grey',font=('bold'),padx=13,command=lambda:classify())
classify_but.place(relx=0.78,rely=0.50)

speed_label=Label(window,font=('Ani',30))
speed_label.pack(side=TOP)

bottom_frame=Frame(window,bg='grey', width=600, height=40)
bottom_frame.pack(side=BOTTOM)
bottom_frame.pack_propagate(0)

result_label=Label(bottom_frame,text=result,font=('bold',20),bg="grey")
result_label.pack(side=BOTTOM)

canvas= Canvas(window,width=300,height=300)

speedo = Canvas(window, width=210, height=110)
speedo.pack()

speed_label=Label(window,font=('Ani',30))
speed_label.pack(side=TOP)

speedo.create_arc(0, 10, 200, 200,  start=0, extent=180, width=5, fill="grey")

speedo.create_text(12,97, text="0")
speedo.create_text(17,70, text="20")
speedo.create_text(33,48, text="40")
speedo.create_text(58,29, text="60")
speedo.create_text(85,20, text="80")

# speedo.create_text(100,20, text="|")

speedo.create_text(118,20, text="100")
speedo.create_text(143,32, text="120")
speedo.create_text(167,48, text="140")
speedo.create_text(179,70, text="160")
speedo.create_text(185,97, text="180")

speedo.create_oval(95,95,105,105,fill="black")

pointer=speedo.create_line(100, 100, 140, 31, width=5, fill="blue",arrow='last',arrowshape=[10,5,0])
shift(0,current)
stay(current)

mainloop()
