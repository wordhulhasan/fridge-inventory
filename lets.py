import dropbox
import picamera
import RPi.GPIO as GPIO
import time
from glob import iglob
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

camera=picamera.PiCamera()
client = dropbox.client.DropboxClient('j-nt--giuPAAAAAAAAADSubiFXZF5V9N39PaF1zAcONS27UcXj2UupafB41lR5r1')
print 'linked account: ',client.account_info()
PATH='/home/pi'


def captureImage():
    
    camera.capture('img.jpg')
    os.system("sudo fswebcam img2.jpg")


def FileUpload():
    f=open('img.jpg','rb')
    f2=open('img2.jpg','rb')
    response=client.put_file('/db-test/Apps/img.jpg',f,overwrite=True)
    response=client.put_file('/db-test/Apps/img2.jpg',f2,overwrite=True)
    print "uploaded",response
    f.close()
    f2.close()

while True:
       i=GPIO.input(11)
       if i==0:                 #When output from motion sensor is LOW
             print "No intruders",i
             GPIO.output(3, 0)  #Turn OFF LED
             time.sleep(0.1)
       elif i==1:               #When output from motion sensor is HIGH
             print "Intruder detected",i
             GPIO.output(3, 1)  #Turn ON LED
             time.sleep(4)
             captureImage()
             FileUpload()


