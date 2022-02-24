import pigpio



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

    def __init__(self, label, gpio, pin, mode, initialValue=None):
        BaseComponent.__init__(self, label, gpio)

        self._pin = pin
        self._mode = mode
        self._initialValue = None
        self._state = initialValue

        self._gpio.set_mode(self._pin, self._mode)

        if self._initialValue is not None \
                and self._mode == pigpio.OUTPUT:

            self._gpio.write(self._pin, self._initialValue)


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
    def initialValue(self):
        return self._initialValue



class OnOffComponent(OnePinComponent):

    def __init__(self, label, gpio, pin, mode, on=pigpio.HIGH, off=pigpio.LOW, initialValue=None):
        OnePinComponent.__init__(self, label, gpio, pin, mode, initialValue=initialValue)

        self._on = on
        self._off = off
    

    def on(self):
        self._state = self._on


    def off(self):
        self._state = self._off


    def toggle(self):
        self._state = self._on if self._state == self._off else self._off
    

