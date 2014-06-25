from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector


class Invader(Widget):
    image = StringProperty('images/invader.jpg')
    move_direction = NumericProperty(0)

    MOVE_TIME = 0.5
    MOVE_STEP = 5

    def __init__(self, **kwargs):
        super(Invader, self).__init__(**kwargs)

        self.last_update = None
        self.elapsed = 0
        self.collision_detected = False

    def update(self, dt):
        self.elapsed += dt

        if self.elapsed > self.MOVE_TIME or self.last_update is None:
            # Move based on current direction.
            if self.move_direction == 0:
                self.center_y -= self.MOVE_STEP

                # After moving down switch back to moving horizontally.
                if self.center_x < self.parent.width / 2:
                    self.move_direction = 1
                else:
                    self.move_direction = -1

            else:
                # Move left or right.
                self.center_x += self.move_direction * self.MOVE_STEP

                # Reset position and direction if out of bounds.
                if self.x < 0:
                    self.x = 0
                    self.move_direction = 0

                elif self.x + self.width >= self.parent.width:
                    self.x = self.parent.width - self.width
                    self.move_direction = 0
            
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