from RPi import GPIO as gpio

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

        self._gpio.setup(self._pin, self._mode)

        if self._initialState is not None and self._mode == gpio.OUT:
            self._gpio.output(self._pin, self._initialState)


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


    def __init__(self, label, gpio, pin, on=gpio.HIGH, off=gpio.LOW, initialState=None):
        OnePinComponent.__init__(self, label, gpio, pin, mode=gpio.OUT, initialState=initialState)

        self._on = on
        self._off = off
    

    def on(self):
        self._state = self._on


    def off(self):
        self._state = self._off


    def toggle(self):
        self._state = self._on if self._state == self._off else self._off
    

    def set(self):
        self._gpio.output(self._pin, self._state)



class PWMComponent(BaseComponent):

    def __init__(self, label, gpio, pin, frequency, initialState=None):
        BaseComponent.__init__(self, label, gpio)

        self._pin = pin
        self._mode = gpio.OUT
        self._initialState = initialState
        self._frequency = frequency

        self._gpio.setup(self._pin, self._mode)
        self._pwm = self._gpio.PWM(self._pin, self._frequency)

        if self._initialState is not None and self._mode == gpio.OUT:
            self._state = initialState
        else:
            self._state = 0

        self._pwm.start(self._state)


    def set(self):
        self._pwm.ChangeDutyCycle(self._state)


    def cleanup(self):
        self._pwm.stop()


    @property
    def frequency(self):
        return self._frequency


    @property
    def state(self):
        return self._state


    @property
    def pin(self):
        return self._pin


    @property
    def mode(self):
        return self._mode


    @property
    def initialState(self):
        return self._initialState

        
