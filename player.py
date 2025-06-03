import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot, Missile


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.missile_timer = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        self.missile_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt, direction=1)
        elif keys[pygame.K_s]:
            self.move(dt, direction=-1)
        else:

            if self.velocity.length() > 0:
                decel = self.velocity.normalize() * PLAYER_DECEL * dt
                if decel.length() > self.velocity.length():
                    self.velocity = pygame.Vector2(0, 0)
                else:
                    self.velocity -= decel

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if keys[pygame.K_f]:
            self.missile_shoot()

        self.position += self.velocity * dt
        self.position.x = max(PLAYER_RADIUS, min(SCREEN_WIDTH - PLAYER_RADIUS, self.position.x))
        self.position.y = max(PLAYER_RADIUS, min(SCREEN_HEIGHT - PLAYER_RADIUS, self.position.y))


    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt, direction=1):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        accel_vector = forward * PLAYER_ACCEL * direction
        self.velocity += accel_vector * dt

        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED
    
    def missile_shoot(self):
        if self.missile_timer > 0:
            return
        self.missile_timer = PLAYER_MISSILE_COOLDOWN
        missile = Missile(self.position.x, self.position.y)
        missile.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_MISSILE_SHOOT_SPEED