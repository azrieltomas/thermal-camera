import RPi.GPIO as GPIO #type: ignore
import time

class displayIO:
    # GPIO buttons
    BUTTON_TL = 22
    BUTTON_BL = 23
    BUTTON_TR = 24
    BUTTON_BR = 25


class thermalcam:
    # variables
    lastButtonPress = time.time()

    def __init__(self):
        self.setup_gpio() # setup gpio
    
    def setup_gpio(self):
        # setup GPIO buttons
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(displayIO.BUTTON_BL, GPIO.IN)
        GPIO.setup(displayIO.BUTTON_BR, GPIO.IN)
        GPIO.setup(displayIO.BUTTON_TL, GPIO.IN)
        GPIO.setup(displayIO.BUTTON_TR, GPIO.IN)

        # GPIO handler
        GPIO.add_event_detect(displayIO.BUTTON_BL, GPIO.RISING, callback=self.btn_bl_press, bouncetime=250)
        GPIO.add_event_detect(displayIO.BUTTON_BR, GPIO.RISING, callback=self.btn_br_press, bouncetime=250)
        GPIO.add_event_detect(displayIO.BUTTON_TL, GPIO.RISING, callback=self.btn_tl_press, bouncetime=250)
        GPIO.add_event_detect(displayIO.BUTTON_TR, GPIO.RISING, callback=self.btn_tr_press, bouncetime=250)

        self.default_mode()
    
    def default_mode(self):
        while True:
            time.sleep(0.1)

    def btn_tl_press(self, channel):
        self.lastButtonPress = time.time()
        print('Top Left')
    
    def btn_bl_press(self, channel):
        self.lastButtonPress = time.time()
        print('Bottom Left')

    def btn_tr_press(self, channel):
        self.lastButtonPress = time.time()
        print('Top Right')

    def btn_br_press(self, channel):
        self.lastButtonPress = time.time()
        print('Bottom Right')


########################################################################################################################
if __name__ == '__main__':
    tCam = thermalcam()