'''
Generator element
=================

Notes:
- the generator look like a circle, the position act as the center.
- generator are not handled at all by the physics engine

'''


from kivy.properties import NumericProperty, ListProperty
from quantiz.elements import QuantizElement
from quantiz.elements.ball import QuantizBall
from math import sqrt


class QuantizGenerator(QuantizElement):

    radius = NumericProperty(32)

    hue = NumericProperty(.5)

    rhythm = ListProperty([1, 1, 1, 1])

    beat = NumericProperty(0)

    def collide_point(self, x, y):
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2) < self.radius

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        touch.grab(self)
        touch.ud.gx = touch.x - self.x
        touch.ud.gy = touch.y - self.y
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return False
        self.x = touch.x - touch.ud.gx
        self.y = touch.y - touch.ud.gy
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return False
        self.x = touch.x - touch.ud.gx
        self.y = touch.y - touch.ud.gy
        touch.ungrab(self)
        return True

    def on_parent(self, instance, parent):
        # we are attached, activate ball generation
        if parent:
            parent.bind(beat=self._generator_beat)

    def _generator_beat(self, instance, beat):
        self.beat = beat
        if not self.rhythm[beat]:
            return
        self._generate_ball()

    def _generate_ball(self):
        ball = QuantizBall(pos=self.pos)
        self.parent.add_widget(ball)

