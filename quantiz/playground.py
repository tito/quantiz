'''
Playground
==========

Base for implementing the game.
The playground offer all the methods needed to create / remove elements on the
playground.

He's also the link between the audio and the game.
'''


from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from quantiz.elements import QuantizElement
import cymunk as cy

PHYSICS_FRAMERATE = 1 / 30.

class QuantizPlayground(FloatLayout):

    hue = NumericProperty(0.75)
    color_pulse = NumericProperty(0)

    tempo = NumericProperty(120)

    measure = NumericProperty(0)

    beat = NumericProperty(0)

    def __init__(self, **kwargs):
        super(QuantizPlayground, self).__init__(**kwargs)
        self.audio_init()
        self.ui_init()
        self.physics_init()

    #
    # Audio part
    #
    def audio_init(self):
        # tempo = per minute, tempo / 60 = per seconds
        # 4 is 4 beat per measure
        Clock.schedule_interval(self.audio_tick, self.tempo / 60. / 4.)

    def audio_tick(self, dt):
        # FIXME: ensure we are not delayed with dt!
        self.beat = beat = (self.beat + 1) % 4
        if beat == 0:
            self.measure += 1

    #
    # UI part
    #

    def ui_init(self):
        self.bind(beat=self._ui_beat)
        Clock.schedule_interval(self._ui_increment_hue, 1 / 30.)

    def _ui_increment_hue(self, dt):
        self.hue += 0.0001
        if self.color_pulse > 0:
            self.color_pulse -= dt

    def _ui_beat(self, instance, beat):
        if beat == 0:
            self.color_pulse = 1

    #
    # Physics part
    #

    def physics_init(self):
        '''
        Initialize the physics world
        '''
        self.cspace = space = cy.Space()
        self.cbounds = []
        space.iterations = 30
        space.gravity = (0, -700)
        space.sleep_time_threshold = 0.5
        space.collision_slop = 0.5

        # create 4 segments that will act as a bounds
        for x in xrange(4):
            seg = cy.Segment(space.static_body,
                    cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
            seg.elasticity = 0.6
            #seg.friction = 1.0
            self.cbounds.append(seg)
            space.add_static(seg)

        # update bounds with good positions
        self.physics_update_bounds()

        self.bind(size=self.physics_update_bounds, pos=self.physics_update_bounds)
        Clock.schedule_interval(self.physics_step, PHYSICS_FRAMERATE)

    def physics_clean(self):
        '''
        Clean all the physics related
        '''
        pass

    def physics_update_bounds(self, *largs):
        assert(len(self.cbounds) == 4)
        a, b, c, d = self.cbounds
        x0, y0 = self.pos
        x1 = self.right
        y1 = self.top

        # it seem that changing a/b coordinate without remove/add doesn't have
        # any impact
        space = self.cspace
        space.remove_static(a)
        space.remove_static(b)
        space.remove_static(c)
        space.remove_static(d)
        a.a = (x0, y0)
        a.b = (x1, y0)
        b.a = (x1, y0)
        b.b = (x1, y1)
        c.a = (x1, y1)
        c.b = (x0, y1)
        d.a = (x0, y1)
        d.b = (x0, y0)
        space.add_static(a)
        space.add_static(b)
        space.add_static(c)
        space.add_static(d)

    def physics_step(self, dt):
        self.cspace.step(PHYSICS_FRAMERATE)
        for widget in self.children:
            if isinstance(widget, QuantizElement):
                widget.physics_update()

    def add_widget(self, widget):
        # for QuantizElement added to the field, create and automatically attach
        # the physics objects
        if isinstance(widget, QuantizElement):
            widget.physics_objects = widget.physics_attach()
            self.cspace.add(widget.physics_objects)
        return super(QuantizPlayground, self).add_widget(widget)

    def remove_widget(self, widget):
        if isinstance(widget, QuantizElement):
            widget.physics_detach()
            self.cspace.remove(widget.physics_objects)
            widget.physics_objects = []
        return super(QuantizPlayground, self).add_widget(widget)

