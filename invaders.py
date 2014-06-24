from kivy.app import App
from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.clock import Clock

from invaders.game import InvadersGame


class InvadersApp(App):
    def build(self):
        game = InvadersGame()

        Clock.schedule_interval(game.update, 1.0 / 60.0)

        return game


if __name__ == '__main__':
    InvadersApp().run()