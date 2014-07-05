import sys
import random

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.core.audio import SoundLoader

from .entities import Invader, Fleet

class InvadersGame(Widget):
    def __init__(self):
        super(InvadersGame, self).__init__()

        self.size = (800, 600)
        self._entities = []

        self._add_entity(self.player_ship, skip_widget=True)
        self._init_fleet()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)

        self._music = SoundLoader.load('sounds/DST-DFear.mp3')
        self._music.play()

    def update(self, dt):
        self.fleet.update(dt)

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

        elif keycode[1] in ('left', 'right'):
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
        if keycode[1] in ('left', 'right'):
            self.player_ship.move_direction = 0

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _init_fleet(self):
        self.fleet = Fleet(rows=5, cols=10)
        self.fleet.pos = ((self.width - self.fleet.width) / 2 + 50, 0)
        self.add_widget(self.fleet)

        self.fleet.create_fleet()
        for s in self.fleet.ships:
            self._add_entity(s)

    def _add_entity(self, entity, skip_widget=False):
        self._entities.append(entity)
        if not skip_widget:
            self.add_widget(entity)

    def _remove_entity(self, entity):
        self.remove_widget(entity)
        self._entities.remove(entity)
