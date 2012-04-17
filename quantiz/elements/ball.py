from quantiz.elements import QuantizElement
from kivy.properties import NumericProperty
import cymunk as cy

class QuantizBall(QuantizElement):

    radius = NumericProperty(16)

    hue = NumericProperty(.5)

    def physics_attach(self):
        # create a falling circle
        body = cy.Body(100, 1e9)
        body.position = self.pos
        circle = cy.Circle(body, self.radius)
        circle.elasticity = 0.6
        #circle.friction = 1.0

        self.cbody = body
        self.ccircle = circle
        return (body, circle)

    def physics_update(self):
        v = self.cbody.position
        self.pos = (v.x, v.y)

    def collide_point(self, x, y):
        return False

    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False

