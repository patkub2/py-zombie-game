import pygame
wn = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('Sprite0.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, x, y):
        self.rect.move_ip(x * self.velocity, y * self.velocity)


player = Player(200, 200)
all_sprites = pygame.sprite.Group(player)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    player.point_at(*pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])

    wn.fill((255, 255, 255))
    all_sprites.draw(wn)
    pygame.display.update()