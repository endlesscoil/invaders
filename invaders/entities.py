from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector


class Fleet(Widget):
    last_move_direction = NumericProperty(1)
    move_direction = NumericProperty(0)

    MOVE_TIME = 0.5
    MOVE_STEP = 10

    def __init__(self, **kwargs):
        self.rows = kwargs.pop('rows', 0)
        self.cols = kwargs.pop('cols', 0)

        super(Fleet, self).__init__(**kwargs)

        self.width = self.cols * Invader().width
        self.height = self.rows * Invader().height

        self.last_update = None
        self.elapsed = 0
        self.ships = []
        self.move_direction = 1

    def create_fleet(self):
        for i in range(self.cols):
            for j in range(self.rows):
                invader = Invader()
                invader.x = (self.parent.width - self.width) / 2 + (i + 1) * invader.width
                invader.y = self.parent.height - ((j + 1) * invader.height)

                self.add_ship(invader)

    def add_ship(self, ship):
        self.ships.append(ship)
        ship.fleet = self

    def update(self, dt):
        self.elapsed += dt

        if self.elapsed > self.MOVE_TIME or self.last_update is None:
            #Logger.debug('move_dir=%d, last_dir=%d, x=%d, y=%d, height=%d, width=%d' % (self.move_direction, self.last_move_direction, self.x, self.y, self.height, self.width))

            # Move based on current direction.
            if self.move_direction == 0:
                self.center_y -= self.MOVE_STEP
                for s in self.ships:
                    s.center_y -= self.MOVE_STEP

                # After moving down switch back to moving horizontally.
                self.last_move_direction, self.move_direction = self.move_direction, -self.last_move_direction

            else:
                # Move left or right.
                self.center_x += self.move_direction * self.MOVE_STEP
                for s in self.ships:
                    s.center_x += self.move_direction * self.MOVE_STEP

                # Reset position and direction if out of bounds.
                if self.x <= 0:
                    self.last_move_direction, self.move_direction = self.move_direction, 0

                elif self.x + self.width >= self.parent.width:
                    self.last_move_direction, self.move_direction = self.move_direction, 0

            self.last_update, self.elapsed = self.elapsed, 0

        return True


class Invader(Widget):
    image = StringProperty('images/invader.jpg')
    last_move_direction = NumericProperty(0)
    move_direction = NumericProperty(0)

    MOVE_TIME = 0.5
    MOVE_STEP = 10

    def __init__(self, **kwargs):
        super(Invader, self).__init__(**kwargs)

        self.fleet = None
        self.last_update = None
        self.elapsed = 0
        self.collision_detected = False

    def update(self, dt):
        self.elapsed += dt

        # NOTE: Only move if not a part of a fleet.  Let the fleet control movement normally.
        if not self.fleet and (self.elapsed > self.MOVE_TIME or self.last_update is None):
            # Move based on current direction.
            if self.move_direction == 0:
                self.center_y -= self.MOVE_STEP

                # After moving down switch back to moving horizontally.
                self.last_move_direction, self.move_direction = self.move_direction, -self.last_move_direction

            else:
                # Move left or right.
                self.center_x += self.move_direction * self.MOVE_STEP

                # Reset position and direction if out of bounds.
                if self.x <= 0:
                    self.last_move_direction, self.move_direction = self.move_direction, 0

                elif self.x + self.width >= self.parent.width:
                    self.last_move_direction, self.move_direction = self.move_direction, 0
            
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