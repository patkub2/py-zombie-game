import pygame
import math
import Weapon
from pygame.math import Vector2

PLAYERCOLOR = (255,   0,   0)

def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]    
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)

class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, screenSize):
        super().__init__()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, pygame.Color('steelblue2'),
                        [(0, 0), (50, 15), (0, 30)])
        self.orig_image = self.image
       
        self.rect = self.image.get_rect(center=screenSize)
        
        self.pos = [screenSize[0] // 2, screenSize[1] // 2]
        self.post = Vector2([screenSize[0] // 2, screenSize[1] // 2])
        self.health = 3
        self.alive = True
        self.movementVector = [0, 0]
        self.movementSpeed = 3
        self.availableWeapons = [Weapon.Pistol(),
                                 Weapon.Shotgun(),
                                 Weapon.MachineGun()]
        self.equippedWeapon = self.availableWeapons[0]

    def move(self, screenSize, tDelta):
        self.movementVector = normalize_vector(self.movementVector)
        newPos = (self.pos[0] + self.movementVector[0]*self.movementSpeed*tDelta,
                  self.pos[1] + self.movementVector[1]*self.movementSpeed*tDelta)
        if newPos[0] < 0:
            self.pos[0] = 0
        elif newPos[0] > screenSize[0] - self.rect.width:
            self.pos[0] = screenSize[0] - self.rect.width
        else:
            self.pos[0] = newPos[0]

        if newPos[1] < 0:
            self.pos[1] = 0
        elif newPos[1] > screenSize[1]-self.rect.height:
            self.pos[1] = screenSize[1]-self.rect.width
        else:
            self.pos[1] = newPos[1]
        
        self.rect.topleft = self.pos
        self.movementVector = [0, 0]
        
    def rotate(self):
        # The vector to the target (the mouse position).
        direction = pygame.mouse.get_pos() - self.post
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        radius, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pygame.transform.rotate(self.orig_image, -angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def update(self):
        self.rotate()
  

    def shoot(self, mousePos):
        self.equippedWeapon.shoot(self, mousePos)
        
    def render(self, surface):
        surface.blit(self.image, self.pos)
