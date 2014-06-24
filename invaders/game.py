from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.logger import Logger


class Invader(Widget):
    image = StringProperty('images/invader.jpg')

    def update(self):
        pass


class Ship(Widget):
    image = StringProperty('images/ship.jpg')

    def update(self):
        pass


class Bullet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def update(self):
        pass


class InvadersGame(Widget):
    def __init__(self):
        super(InvadersGame, self).__init__()

        self.size = (800, 600)

        self._entities = []

    def update(self, dt):
        for e in self._entities:
            e.update()