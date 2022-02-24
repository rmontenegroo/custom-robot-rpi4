import pigpio
import math


class BaseComponent(object):

    def __init__(self, label, gpio):
        self._gpio = gpio
        self._label = label


    @property
    def label(self):
        return self._label


    @property
    def gpio(self):
        return self._gpio



class OnePinComponent(BaseComponent):

    def __init__(self, label, gpio, pin, mode, initialState=None):
        BaseComponent.__init__(self, label, gpio)

        self._pin = pin
        self._mode = mode
        self._initialState = None
        self._state = initialState

        self._gpio.set_mode(self._pin, self._mode)

        if self._initialState is not None \
                and self._mode == pigpio.OUTPUT:

            self._gpio.write(self._pin, self._initialState)


    @property
    def state(self):
        return self._state


    @state.setter
    def state(self, value):
        self._state = value


    @property
    def pin(self):
        return self._pin


    @property
    def mode(self):
        return self._mode


    @property
    def initialState(self):
        return self._initialState



class OnOffComponent(OnePinComponent):


    def __init__(self, label, gpio, pin, on=pigpio.HIGH, off=pigpio.LOW, initialState=None):
        OnePinComponent.__init__(self, label, gpio, pin, mode=pigpio.OUTPUT, initialState=initialState)

        self._on = on
        self._off = off
    

    def on(self):
        self._state = self._on


    def off(self):
        self._state = self._off


    def toggle(self):
        self._state = self._on if self._state == self._off else self._off
    

    def set(self):
        self._gpio.write(self._pin, self._state)



class PWMComponent(BaseComponent):

    def __init__(self, label, gpio, pin, frequency, minDC=500, maxDC=2500, initialState=None):
        BaseComponent.__init__(self, label, gpio)

        self._pin = pin
        self._mode = pigpio.OUTPUT
        self._initialState = initialState
        self._frequency = frequency
        self._minDC = minDC
        self._maxDC = maxDC

        self._gpio.set_mode(self._pin, self._mode)
        self._gpio.set_PWM_frequency(self._pin, self._frequency)

        if self._initialState is not None and self._mode == pigpio.OUTPUT:
            self._state = initialState
        else:
            self._state = math.ceil((self._minDC + self._maxDC)/2)


    def set(self):
        self._gpio.set_servo_pulsewidth(self._pin, self._state)

    def cleanup(self):
        self._gpio.set_servo_pulsewidth(self._pin, 0)

    @property
    def minDC(self):
        return self._minDC


    @property
    def maxDC(self):
        return self._maxDC


    @property
    def frequency(self):
        return self._frequency


    @property
    def state(self):
        return self._state


    @state.setter
    def state(self, value):
        if value >= self._minDC and value <= self._maxDC:
            self._state = value


    @property
    def pin(self):
        return self._pin


    @property
    def mode(self):
        return self._mode


    @property
    def initialState(self):
        return self._initialState
