# led-control WS2812B LED Controller Server
# Copyright 2019 jackw01. Released under the MIT License (see LICENSE for details).

from .rpi_ws281x import PixelStrip, Color, blackbody_to_rgb, blackbody_correction_rgb
from .lib import *

__version__ = '4.2.2'
