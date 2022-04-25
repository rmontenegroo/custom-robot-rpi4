#!/usr/bin/env python3
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

if __name__ == '__main__':
    kit.servo[0].angle = 90
    time.sleep(1)
