import argparse
import datetime
import time
import math
from collections import namedtuple
from ledcontrol.ledcontroller import LEDController

import ledcontrol.driver as driver

class Settings:
    global_color_temp = 6500
    correction_r = 255
    correction_g = 190
    # correction_b = 270
    correction_b = 170


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--led-count", type=int, default=5)
    parser.add_argument("--seconds", type=int, default=1)
    parser.add_argument("action", choices=("startup", "shutdown", "clear"))
    return parser.parse_args()

def circular_mean(a1, a2, p):
    return math.atan2(
        (1-p)*math.sin(a1) + p*math.sin(a2),
        (1-p)*math.cos(a1) + p*math.cos(a2),
    ) % (2*math.pi)

class Color(namedtuple("Color", ("h", "s", "v"))):
    def mix_hues(self, other, p):
        return circular_mean(self.h*2*math.pi, other.h*2*math.pi, p) / (2*math.pi)

    def mix(self, other, p):
        return Color(
            self.mix_hues(other, p),
            (1-p)*self.s + p*other.s,
            (1-p)*self.v + p*other.v,
        )

colors = [
    Color(
        0.6175635842715993,
        1,
        0
    ),
    Color(
        0.6175635842715993,
        0.7274992244615467,
        0.5
    ),
    Color(
        0.7439005234662223,
        0.7002515180395283,
        0.6
    ),
    Color(
        0.9222222222222223,
        0.9460097254004577,
        0.7
    ),
    Color(
        0.9936081381405101,
        0.6797928024431981,
        0.8
    ),
    Color(
        0.11311430089613972,
        0.9260097254004577,
        1
    ),
    Color(
        0.11311430089613972,
        0,
        1
    ),

]



def calculate_color_correction():
    'Calculate and store color temperature correction'
    rgb = driver.blackbody_to_rgb(Settings.global_color_temp)
    c = [Settings.correction_r * int(rgb[0] * 255) // 255,
          Settings.correction_g * int(rgb[1] * 255) // 255,
          Settings.correction_b * int(rgb[2] * 255) // 255]
    return (c[0] << 16) | (c[1] << 8) | c[2]


class Controller:
    def __init__(self, led_count, interval_sec):
        self.controller = LEDController(
            led_count=led_count,
            led_pin=18,
            led_data_rate=800000,
            led_dma_channel=10,
            led_pixel_order="GRBW"
        )
        self.led_count = led_count
        self.interval_sec = interval_sec
        self.correction = calculate_color_correction()

    def set_color(self, color):
        self.controller.set_all_hsv(
            [color]*self.led_count, self.correction, 1.0, 1.0
        )

    def animate(self, colors):
        for i in range(len(colors) -1):
            step1, step2 = colors[i], colors[i+1]
            for j in range(self.interval_sec+1):
                color = step1.mix(step2, j/self.interval_sec)
                self.set_color(color)
                time.sleep(1)

    def clear(self):
        self.set_color(Color(0,0,0))

def main():
    args = parse_args()
    controller = Controller(args.led_count, args.seconds)
    if args.action == "clear":
        controller.clear()
        return
    colors_to_use = colors if args.action == "startup" else colors[::-1]
    controller.animate(colors_to_use )

main()
