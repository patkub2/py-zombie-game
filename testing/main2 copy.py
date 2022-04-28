import pygame

# === CONSTANS === (UPPER_CASE names)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

# === MAIN === (lower_case names)

# --- init ---

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# --- objects ---

player = pygame.Rect(screen_rect.centerx, screen_rect.bottom, 0, 0)
start = pygame.math.Vector2(player.center)
end = start
length = 50

SPEED = 5

all_bullets = []

# --- mainloop ---

clock = pygame.time.Clock()
is_running = True


while is_running:

    # --- events ---

    for event in pygame.event.get():

        # --- global events ---

        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
            end = start + (mouse - start).normalize() * length
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            distance = mouse - start

            position = pygame.math.Vector2(start) # duplicate # start position in start of canon
            #position = pygame.math.Vector2(end)   # duplicate # start position in end of canon
            speed = distance.normalize() * SPEED
            
            all_bullets.append([position, speed])
            
        # --- objects events ---

            # empty

    # --- updates ---

    for position, speed in all_bullets:
        position += speed

    # --- draws ---

    screen.fill(BLACK)

    pygame.draw.line(screen, RED, start, end)

    for position, speed in all_bullets:
        # need to convert `float` to `int` because `screen` use only `int` values
        pos_x = int(position.x)
        pos_y = int(position.y)
        pygame.draw.line(screen, (0,255,0), (pos_x, pos_y), (pos_x, pos_y))
        
    pygame.display.update()

    # --- FPS ---

    clock.tick(25)

# --- the end ---

pygame.quit()