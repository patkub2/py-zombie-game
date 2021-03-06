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
        self.image =  pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35)) 
        self.orig_image = self.image
        
        self.x = screenSize[0]
        self.y = screenSize[1]
        self.offset = Vector2(0,0)  # We shift the sprite 50 px to the right.
        
        self.pos = Vector2(screenSize[0]// 2, screenSize[1]// 2 )
        self.rect = self.image.get_rect(center=(screenSize[0]// 2, screenSize[1]// 2 ))



        self.health = 5
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
        
        self.rect.center = self.pos
        self.movementVector = [0, 0]
        
    def update(self):
        self.rotate()
  
    def rotate(self):
        direction = pygame.mouse.get_pos() - self.pos
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        radius, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pygame.transform.rotate(self.orig_image, -angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center -self.offset)
    
  
        


    def shoot(self, mousePos):
        self.equippedWeapon.shoot(self, mousePos)
        
    def render(self, surface):
        surface.blit(self.image, self.rect)
