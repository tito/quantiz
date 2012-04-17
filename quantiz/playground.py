# FIXME split that file.

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock

class QuantizPlayground(FloatLayout):

    hue = NumericProperty(0.75)

    def __init__(self, **kwargs):
        super(QuantizPlayground, self).__init__(**kwargs)
        Clock.schedule_interval(self.increment_hue, 1 / 15.)

    def increment_hue(self, dt):
        self.hue += 0.0001
