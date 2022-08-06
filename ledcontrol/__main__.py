import argparse
import datetime
from collections import namedtuple
from ledcontrol.ledcontroller import LEDController

Time = namedtuple("Time", ("h", "m"))

def parse_time(s: str):
    return Time(*s.split(":"))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-time", required=True, help="Format: HH:MM")
    parser.add_argument("--end-time", required=True, help="Format: HH:MM")
    parser.add_argument("--led-count", type=int, default=5)
    return parser.parse_args()

def main():
    args = parse_args()
    start_time = parse_time(args.start_time)
    end_time = parse_time(args.end_time)
    controller = LEDController(
        led_count=args.led_count,
        led_pin=18,
        led_data_rate=800000,
        led_dma_channel=10,
        led_pixel_order="GRBW"
    )
    controller.set_all_hsv(
        [(217, 73, 96)]*args.led_count, 0, 255, 255
    )
