import RPi.GPIO as GPIO
import RGBController as rgb
from picamera import PiCamera
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from time import sleep
from datetime import datetime

def takePic(currLight = rgb.LIGHTOFF, p_name = "default"):
    '''
    when using this function, pass RGBController.bPin to currLight
    currLight: current shining light
    this function uses camera module to take picture
    blinks green before taking picture
    save to /home/pi/Desktop/<m-d-y_h_m_s>.jpg
    returns full path
    '''
    camera = PiCamera()
    try:
        # p_time = datetime.now().strftime("%m-%d-%Y_%H_%M_%S")
        p_path = '/home/pi/Desktop/PythonCode/' + p_name + '.jpg'
        # rgb.blink(rgb.bPin, currLight = currLight)
	camera.resolution = (1080,720)
        camera.capture(p_path)
        print("picture taken")
        camera.close()
    except Exception as e:
        print("Error occured during takePic():")
        print(str(e))
    finally:
        camera.close()

    return p_path

def drawOnPic(p_path, content):
    '''
    p_path: full path without extension of picture to be manipulated
    content: string to put onto the picture
    saves to p_path
    returns full path
    '''
    try:
        with Image.open(p_path) as img:
            print("drawing")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 80)
            draw.text((252,12), content, (255,255,255), font = font)
            draw.text((250,10), content, (0,0,0), font = font)
            img.save(p_path)
            return p_path

    except Exception as e:
        print("Error occur during drawOnPic()")
        print(str(e))
        return ""
