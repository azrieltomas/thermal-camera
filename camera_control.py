# import RPi.GPIO as GPIO #type: ignore
import time
import gpiod
from gpiod.line import Edge

from smbus2 import SMBus

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ST7789 import ST7789

class displayIO:
    # default values for the ST7789 display - FIXED
    WIDTH = 320                     # pixels
    HEIGHT = 240                    # pixels
    SPI_PORT = 0                    # port number
    SPI_CS = 1                      # chip select pin
    SPI_DC = 9                      # dc pin
    SPI_HZ = 32 * 1000 * 1000       # frequency (set to max)
    ROTATE = 180                    # degrees
    BACKLIGHT = 13                  # backlight pin
    
    # GPIO buttons
    BUTTON_TL = 22
    BUTTON_BL = 23
    BUTTON_TR = 24
    BUTTON_BR = 25

class displayFont:
    smallSize   = 13
    medSize     = 16
    largeSize   = 18
    small       = ImageFont.truetype("include/RobotoMono.ttf", smallSize)
    med         = ImageFont.truetype("include/RobotoMono.ttf", medSize)
    large       = ImageFont.truetype("include/RobotoMono.ttf", largeSize)

class thermalcam:
    # variables
    lastButtonPress = time.time()
    
    # blocks for items
    display = None
    dispImage = None
    drawImage = None
    chip = None

    def __init__(self):
        self.setup_gpio() # setup gpio
    
    def setup_gpio(self):
        # self.chip = gpiod.Chip('gpiochip0')
        
        # # setup GPIO buttons
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(displayIO.BUTTON_BL, GPIO.IN)
        # GPIO.setup(displayIO.BUTTON_BR, GPIO.IN)
        # GPIO.setup(displayIO.BUTTON_TL, GPIO.IN)
        # GPIO.setup(displayIO.BUTTON_TR, GPIO.IN)

        # # GPIO handler
        # GPIO.add_event_detect(displayIO.BUTTON_BL, GPIO.RISING, callback=self.btn_bl_press, bouncetime=250)
        # GPIO.add_event_detect(displayIO.BUTTON_BR, GPIO.RISING, callback=self.btn_br_press, bouncetime=250)
        # GPIO.add_event_detect(displayIO.BUTTON_TL, GPIO.RISING, callback=self.btn_tl_press, bouncetime=250)
        # GPIO.add_event_detect(displayIO.BUTTON_TR, GPIO.RISING, callback=self.btn_tr_press, bouncetime=250)

        self.display = ST7789(port=displayIO.SPI_PORT,
                              cs=displayIO.SPI_CS,
                              dc=displayIO.SPI_DC,
                              backlight=displayIO.BACKLIGHT,
                              width=displayIO.WIDTH,
                              height=displayIO.HEIGHT,
                              rotation=displayIO.ROTATE,
                              spi_speed_hz=displayIO.SPI_HZ)
        
        # run default menu
        self.startup_display()
        # self.default_mode()
        self.watch_button_press()
    
    def startup_display(self):
        # run a little animation to show the device is thinking. takes a few seconds before everything is ready
        # if you could be bothered, you could load other resources at this time
        msgScreen = "Thermal Camera Starting..."

        # draw black background with centered text
        self.dispImage = Image.new('RGB', (displayIO.WIDTH, displayIO.HEIGHT), color=(0, 0, 0))
        self.drawImage = ImageDraw.Draw(self.dispImage)
        self.drawImage.text(((displayIO.WIDTH / 2), (displayIO.HEIGHT / 3) - (displayFont.largeSize / 2)), msgScreen, font=displayFont.large, fill=(255, 255, 255), anchor='mm')

        # draw a loading bar outline
        inset = 19
        rectY0 = displayIO.HEIGHT / 3 * 2
        rect = (inset, rectY0, displayIO.WIDTH - inset, rectY0 + 20)
        self.drawImage.rectangle((rect[0], rect[1], rect[2], rect[3]), fill=(0, 0, 0), outline=(255, 255, 255))

        # fill it with green over a period of 10s
        # 280 pixels @ 4 Hz = 40 redraws of 7 pixels each
        # draw over the top of the last image to save time and energy
        # pxShift = 7 # normal
        pxShift = 35  # quick
        for i in range(rect[0] + 1, rect[2] - 1, pxShift):
            self.drawImage.rectangle((i, rect[1] + 1, i + pxShift - 1, rect[3] - 1), fill=(0, 255, 0))
            self.display.display(self.dispImage)
            time.sleep(0.250)

    def watch_button_press(self):
        buttonTup = [displayIO.BUTTON_TL, displayIO.BUTTON_BL, displayIO.BUTTON_TR, displayIO.BUTTON_BR]
        with gpiod.request_lines("/dev/gpiochip0",
                                 consumer="watch-button-press",
                                 config={tuple(buttonTup): gpiod.LineSettings(edge_detection=Edge.RISING_EDGE)},
                                 ) as request:
            while True:
                for event in request.read_edge_events():
                    print(event.line_offset)
                    

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