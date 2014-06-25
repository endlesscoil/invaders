import sys

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.logger import Logger


class Invader(Widget):
    image = StringProperty('images/invader.jpg')

    def update(self):
        return True


class Ship(Widget):
    image = StringProperty('images/ship.jpg')

    def update(self):
        return True

    def fire(self, velocity=(0, 5)):
        bullet = Bullet()

        bullet.center_x = self.center_x
        bullet.center_y = self.y + 5
        bullet.velocity = velocity

        return bullet


class Bullet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos

        if self.center_y > self.parent.height:
            return False

        return True


class InvadersGame(Widget):
    def __init__(self):
        super(InvadersGame, self).__init__()

        self.size = (800, 600)
        self._entities = []

        self._add_entity(self.player_ship, skip_widget=True)
        self._add_entity(self.test_invader, skip_widget=True)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def update(self, dt):
        for e in self._entities[:]:
            status = e.update()
            if not status:
                self._entities.remove(e)

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        #Logger.debug(keycode)

        if keycode[1] == 'escape':
            sys.exit(1)

        elif keycode[1] == 'spacebar':
            bullet = self.player_ship.fire()
            self._add_entity(bullet)

        elif keycode[1] in ('left', 'right', 'up', 'down'):
            if keycode[1] == 'left':
                self.player_ship.center_x -= 10
            elif keycode[1] == 'right':
                self.player_ship.center_x += 10

        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _add_entity(self, entity, skip_widget=False):
        self._entities.append(entity)
        if not skip_widget:
            self.add_widget(entity)
