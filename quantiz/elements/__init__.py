'''
Quantiz Element
===============

Base class to implement all the Quantiz elements.
'''

from kivy.uix.widget import Widget


class QuantizElement(Widget):

    def physics_attach(self):
        '''
        Create all the necessary physics object for this element. All the
        returned objects will be added to the physics space.
        '''
        return []

    def physics_update(self):
        '''
        Physics objects have been updated, you must update the graphics
        according to the physics objects.
        '''
        pass

    def physics_detach(self):
        '''
        The element is beeing deleted from the physics engine, if anything is
        needed to be done, do it here.
        '''
        pass

