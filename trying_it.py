import cv2, threading, os, time
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk
from threading import Thread
from os import listdir
from os.path import isfile, join
import dlib
from imutils import face_utils, rotate_bound
import math
import time

rightear = cv2.CascadeClassifier('filters/haarcascade_mcs_rightear.xml')
leftear = cv2.CascadeClassifier('filters/haarcascade_mcs_leftear.xml')

#Gives Regions of Face parts like eyes, nose, ears etc,.
def get_face_boundbox(points, face_part):
    if face_part == 1:
        #Eye Brows
        (x, y, w, h) = calculate_boundbox(points[17:27])
    elif face_part == 2:
        #Left Eye Brow
        (x, y, w, h) = calculate_boundbox(points[22:27]) 
    elif face_part == 3:
        #Eyes
        (x, y, w, h) = calculate_boundbox(points[36:48])
    elif face_part == 4:
        #Left Eye
        (x, y, w, h) = calculate_boundbox(points[42:48])
    elif face_part == 5:
        #Nose
        (x, y, w, h) = calculate_boundbox(points[27:35])
    elif face_part == 6:
        #Face Sides
        (x, y, w, h) = calculate_boundbox(points[0:17])
    elif face_part == 7:
        #Right Ear
        (x, y, w, h) = calculate_boundbox(points[3:6])
    elif face_part == 8:
        #Left Ear
        (x, y, w, h) = calculate_boundbox(points[12:16])
    return (x, y, w, h)


def calculate_boundbox(list_coordinates):
    x = min(list_coordinates[:, 0])
    y = max(list_coordinates[:, 1])
    w = max(list_coordinates[:, 0]) - x
    h = y - min(list_coordinates[:, 1])
    return (x, y, w, h)

def calculate_body_boundbox(x, x1, y, y1):
    w = abs(x - x1)
    h = abs(y - y1)
    return (w, h)


#Showing sprite by adjusting its position
def show_sprite(image, sprite, x_offset, y_offset):
    (height, width) = (sprite.shape[0], sprite.shape[1])
    (image_height, image_width) = (image.shape[0], image.shape[1])

    if y_offset + height >= image_height:
        sprite = sprite[0:image_height - y_offset, :, :]

    if x_offset + width >= image_width:
        sprite = sprite[:, 0:image_width - x_offset, :]

    if x_offset < 0: 
        sprite = sprite[:, abs(x_offset)::, :]
        w = sprite.shape[1]
        x_offset = 0

    for c in range(3):
        image[y_offset:y_offset + height, x_offset:x_offset + width, c] =  \
        sprite[:, :, c] * (sprite[:, :, 3]/255.0) +  image[y_offset:y_offset + height, x_offset:x_offset + width, c] * (1.0 - sprite[:, :, 3]/255.0)
    return image


#Adjusting the object to the face
def adjusting_sprite(sprite, width, head_ypos, ontop = True):
    #Getting height, width of the sprite
    (height_sprite, width_sprite) = (sprite.shape[0], sprite.shape[1])
    #Scaling size of the sprite to the human face
    scaling_factor = width/width_sprite
    if SPRITES[5] or SPRITES[6]:
        if(dropdown.get() == 'S'):
            sprite = cv2.resize(sprite, (0,0), fx = 0.5, fy = 0.5)
        elif(dropdown.get() == 'M'):
            sprite = cv2.resize(sprite, (0,0), fx = 0.6, fy = 0.6)
        elif(dropdown.get() == 'L'):
            sprite = cv2.resize(sprite, (0,0), fx = 0.7, fy = 0.7)
        elif(dropdown.get() == 'XL'):
            sprite = cv2.resize(sprite, (0,0), fx = 0.8, fy = 0.8)
        else:
            sprite = cv2.resize(sprite, (0,0), fx = 1.0, fy = 1.0)
    else:
        sprite = cv2.resize(sprite, (0,0), fx = scaling_factor, fy = scaling_factor)
    (height_sprite, width_sprite) = (sprite.shape[0], sprite.shape[1])
    y_origin =  head_ypos - height_sprite if ontop else head_ypos
    if SPRITES[5] or SPRITES[6]:
        y_origin = head_ypos
    if (y_origin < 0):
        sprite = sprite[abs(y_origin)::, :, :] 
        y_origin = 0
    return (sprite, y_origin)


#Applying the virtual trial room functionality
def apply_sprite(image, sprite_path, width, x, y, angle, ontop = True):
    #Reading the image which needs to be projected
    sprite = cv2.imread(sprite_path, -1)
    #Adjusting object based gestures of face
    sprite = rotate_bound(sprite, angle)
    (sprite, y_position) = adjusting_sprite(sprite, width, y, ontop)
    #Showing the sprite
    if SPRITES[5] or SPRITES[6]:
        image = show_sprite(image, sprite, x - 100, y_position - 50)
    else:
        image = show_sprite(image, sprite, x, y_position)


#Calculating the inclination of face
def calculate_inclination(point1, point2):
    x1, x2, y1, y2 = point1[0], point2[0], point1[1], point2[1]
    inclination = 180/math.pi * math.atan((float(y2 - y1))/(x2 - x1))
    return inclination

    
#Principal Loop where openCV (magic) occurs
def cvloop(run_event):
    global panelA
    global SPRITES
    global image_path
    
    i = 0
    #Capturing Video
    video_capturing = cv2.VideoCapture(0)
    (x, y, w, h) = (0, 0, 10, 10) #whatever initial values

    #Filters path
    detector = dlib.get_frontal_face_detector()

    model = "filters/shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(model) # link to model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

    #Body Skelton
    protoFile = "filters/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "filters/pose_iter_440000.caffemodel"
    nPoints = 15

    inWidth = 368
    inHeight = 368
    threshold = 0.1
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    while run_event.is_set():
        #Storing video into image variable
        ret, image = video_capturing.read()
        #To obtain gray shade of the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)

        if SPRITES[2]:
            right_ear = rightear.detectMultiScale(gray, 1.1, 4)
            left_ear = leftear.detectMultiScale(gray, 1.1, 3)
            for (x, y, w, h) in right_ear:
                print('rear')
                apply_sprite(image, image_path, w, x - 5, y + int(3*h/4), 0, ontop = False)
                    
            for (x, y, w, h) in left_ear:
                print('lear')
                apply_sprite(image, image_path, w, x + 5, y + int(3*h/4), 0, ontop = False)

        if SPRITES[5] or SPRITES[6]:
            imageCopy = np.copy(image)
            imageWidth = image.shape[1]
            imageHeight = image.shape[0]
            inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
            net.setInput(inpBlob)
            output = net.forward()
            H = output.shape[2]
            W = output.shape[3]
            # Empty list to store the detected keypoints
            points = []

            for i in range(nPoints):
                # confidence map of corresponding body's part.
                probMap = output[0, i, :, :]
                # Find global maxima of the probMap.
                minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
                # Scale the point to fit on the original image
                x = (imageWidth * point[0]) / W
                y = (imageHeight * point[1]) / H
                if prob > threshold :
                    cv2.circle(imageCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                    cv2.putText(imageCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
                    # Add the point to the list if the probability is greater than the threshold
                    points.append([int(x), int(y)])
                else :
                    points.append(None)
            if SPRITES[5]:
                reqPoints = [points[5], points[2], points[9]]
            elif SPRITES[6]:
                reqPoints = [points[5], points[2], points[8]]
            if(reqPoints[0] != None and reqPoints[1] != None and reqPoints[2] != None):
                (w, h) = calculate_body_boundbox(reqPoints[0][0], reqPoints[1][0], reqPoints[1][1], reqPoints[2][1])
                print(reqPoints[1][0], reqPoints[1][1], w, h)
                print(reqPoints[:][0])
                print(reqPoints[:][1])
                apply_sprite(image, image_path, w, reqPoints[1][0], reqPoints[1][1], 0, ontop = True)


        for face in faces:
            #Cordinates of FACE in the video
            (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())

            #Predicting points of FACE in the obtained cordinates
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            inclination = calculate_inclination(shape[17], shape[26]) #inclination based on eyebrows

            #Condition to see if mouth is open(Difference between y cordinate landmarks of upper and lower lips
            is_mouth_open = (shape[66][1] - shape[62][1]) >= 10

            if SPRITES[0]:
                #No projection
                apply_sprite(image, image_path, w, x, y + 40, inclination, ontop = True)
    
            if SPRITES[1]:
                #For Necklace
                (neck_x, neck_y, neck_w, neck_h) = get_face_boundbox(shape, 6)
                apply_sprite(image, image_path, neck_w, neck_x, neck_y + neck_h, inclination)

            if SPRITES[3]:
                (forehead_x, forehead_y, forehead_w, forehead_h) = get_face_boundbox(shape, 1)
                apply_sprite(image, image_path, int(forehead_w * 2), int(forehead_x - forehead_w/2), int(forehead_y), inclination)

            if SPRITES[4]:
                #For Sun Glasses
                (eyes_x, eyes_y, eyes_w, eyes_h) = get_face_boundbox(shape, 3)
                apply_sprite(image, image_path, eyes_w * 1.5, int(eyes_x - (eyes_w/4)), int(eyes_y + 2 * eyes_h), inclination)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panelA.configure(image = image)
        panelA.image = image

    video_capturing.release()


#Turning ON and OFF of projection
def projection_on_off(category_number):
    global SPRITES, BTNS
    print(SPRITES[category_number])
    SPRITES[category_number] = (1 - SPRITES[category_number])


#Adding Sprite(object) for projection purpose the video being captured
def add_sprite_basedon_category(image):
    global image_path
    image_path = image
    projection_on_off(int(image.rsplit('/',1)[0][-1]))


#Creates a layout for Trying the items
def try_on(image_path, drop):   
    btn1 = Button(root, text = "Try It ON", command = lambda:add_sprite_basedon_category(image_path))

    if drop:
        dropdown.set("Choose the Size")
        options = OptionMenu(root, dropdown, "S", "M", "L", "XL", "XXL")
        options.pack(side = "left", fill = "both", expand = "True", padx = "5", pady = "5")
        btn1.pack(side = "right", fill = "both", expand = "True", padx = "5", pady = "5")
    else:
        btn1.pack(side = "top", fill = "both", expand = "no", padx = "5", pady = "5")


print('hiii')
# Initialize GUI object
root = Tk()
root.title("Virtual Trial Room")
this_dir = os.path.dirname(os.path.realpath(__file__))

btn1 = None
dropdown = StringVar(root)
panelA = Label(root)
panelA.pack(padx = 10, pady = 10)

SPRITES = [0, 0, 0, 0, 0, 0, 0]
BTNS = [btn1]
image_path = ''

path = sys.argv[1]
drop = False
if(int(path.rsplit('/',1)[0][-1]) >= 5):
    drop = True
try_on(path, drop)
run_event = threading.Event()
run_event.set()
action = Thread(target = cvloop, args = (run_event,))
action.setDaemon(True)
action.start()

def terminate():
        global root, run_event, action
        run_event.clear()
        time.sleep(1)
        root.destroy()

root.protocol("WM_DELETE_WINDOW", terminate)
root.mainloop() 
