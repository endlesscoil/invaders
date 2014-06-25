import sys
import random

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.logger import Logger


class Invader(Widget):
    image = StringProperty('images/invader.jpg')

    MOVE_TIME = 3

    def __init__(self, **kwargs):
        super(Invader, self).__init__(**kwargs)

        self.last_update = None
        self.elapsed = 0
        self.collision_detected = False

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed > self.MOVE_TIME or self.last_update is None:
            self.center_y -= 10
            self.last_update, self.elapsed = self.elapsed, 0

        return True


class Ship(Widget):
    image = StringProperty('images/ship.jpg')
    move_direction = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Ship, self).__init__(**kwargs)

        self.collision_detected = False

    def update(self, dt):
        if self.move_direction != 0:
            self.center_x += self.move_direction * 5

            if self.x <= 0:
                self.x = 0
            elif self.x + self.width >= self.parent.width:
                self.x = self.parent.width - self.width

        return True

    def fire(self, velocity=(0, 5)):
        bullet = Bullet()

        bullet.center_x = self.center_x
        bullet.center_y = self.y + self.height + 5
        bullet.velocity = velocity

        return bullet


class Bullet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)

        self.collision_detected = False

    def update(self, dt):
        self.pos = Vector(*self.velocity) + self.pos

        # Check for collisions
        for e in self.parent._entities:
            if e is not self and e.collide_widget(self):
                e.collision_detected = True

                return False

        # Check if we've gone off-screen
        if self.center_y > self.parent.height:
            return False

        # Still alive.
        return True


class InvadersGame(Widget):
    def __init__(self):
        super(InvadersGame, self).__init__()

        self.size = (800, 600)
        self._entities = []

        self._add_entity(self.player_ship, skip_widget=True)
        self._add_entity(self.test_invader, skip_widget=True)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)

    def update(self, dt):
        for e in self._entities[:]:
            status = e.update(dt)
            if not status or e.collision_detected:
                self._remove_entity(e)

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        #Logger.debug(keycode)

        if keycode[1] == 'escape':
            sys.exit(1)

        elif keycode[1] == 'spacebar':
            bullet = self.player_ship.fire()
            self._add_entity(bullet)

        elif keycode[1] in ('left', 'right', 'up', 'down'):
            if keycode[1] == 'left':
                self.player_ship.move_direction = -1
            elif keycode[1] == 'right':
                self.player_ship.move_direction = 1

        elif keycode[1] == 'z':
            invader = Invader()
            invader.center = (random.randint(0, self.width), random.randint(self.height * 0.66, self.height))

            self._add_entity(invader)

        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in ('left', 'right', 'up', 'down'):
            self.player_ship.move_direction = 0

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _add_entity(self, entity, skip_widget=False):
        self._entities.append(entity)
        if not skip_widget:
            self.add_widget(entity)

    def _remove_entity(self, entity):
        self.remove_widget(entity)
        self._entities.remove(entity)
