import os
import nfc
import sys
import time
import binascii
import RPi.GPIO as GPIO

gp_out = 4
wait_time = 3

left = (0.5 / 20) * 100
right = (2.4 / 20) * 100
center = (1.45 / 20) * 100

target_req = nfc.clf.RemoteTarget("212F")
target_req.sensf_req = bytearray.fromhex("0000030000")

my_idm = os.environ.get('IDM')

def servo_function():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gp_out, GPIO.OUT)
        servo = GPIO.PWM(gp_out, 50)
        servo.start(0)
        for i in range(1):
            servo.ChangeDutyCycle(left)
            time.sleep(0.5)
            servo.ChangeDutyCycle(center)
            time.sleep(0.5)
        servo.stop()
        GPIO.cleanup(gp_out)
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()
        sys.exit()


while True:
    try:
        clf = nfc.ContactlessFrontend("usb")
        target = clf.sense(target_req, iterations = 3, interval = wait_time)
        if target:
            tag = nfc.tag.activate(clf, target)
            tag.sys = 3
            idm_bytes = binascii.hexlify(tag.idm)
            idm = idm_bytes.decode("utf-8")
            print(my_idm)
            if idm == my_idm:
                servo_function()
        clf.close()
    except KeyboardInterrupt:
        sys.exit()

