# self is the same as this in java
# The self variable is used to represent the instance of the class. Used for OOP.
from os import spawnl
import pygame
from utils import load_sprite, get_random_position
from models import Spaceship, Asteroid


MAX_BULLETS = 3
start_time = pygame.time.get_ticks()

# Class with all the methods we need


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        # Set screen size
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space1", False)
        self.clock = pygame.time.Clock()

        self.asteroids = []
        self.bullets = []
        # Create object spaceship & Asteroid
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(3):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            # Add to array
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    # Game loop
    def main_loop(self):
        while True:
            # Will handle the user input
            self._handle_input()
            # Will handle the game mechanics
            self._process_game_logic()
            # Will draw everything on the screen
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _handle_input(self):
        is_key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            # Quits the game if you press escape or the X top rightfiix
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
                # Shoot bullets
            elif(
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                # if length of bullet array == 4, you can't shoot more bullets
                and len(self.bullets) <= MAX_BULLETS

            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
               self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
               self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
               self.spaceship.accelerating = True
               self.spaceship.no_action = False
            else:
               self.spaceship.accelerating = False
               self.spaceship.no_action = True

        # self.spaceship.showspeed()
        self.spaceship.accelerate()
        self.spaceship.slowdown()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    # Call split method
                    asteroid.split()
                    break

        if self.spaceship:
         for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
            if len(self.bullets) == 5:
                self.bullets.remove(bullet)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        pygame.display.flip()
        # This will run the game in 60 fps
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
