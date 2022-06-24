# -*- coding: utf-8 -*-


import pygame, sys
import random
from Player import Player
from EnemyNormal import EnemyNormal
from EnemyShoot import EnemyShoot
from button import Button
from os import path


pygame.init()
size    = (1280, 720)
BGCOLOR = (158, 255, 166)
screen = pygame.display.set_mode(size)
scoreFont = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down")

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
enemies = pygame.sprite.Group()
lastEnemyNormal = 0
score = 0
clock = pygame.time.Clock()
BG = pygame.image.load("assets/BG.jpg")
BGblured = pygame.image.load("assets/BGblured.png")
highscore = 0


def store_highscore_in_file(dictionary, fn = "./high.txt", top_n=0):
    """Store the dict into a file, only store top_n highest values."""
    with open(fn,"w") as f:
        for idx,(name,pts) in enumerate(sorted(dictionary.items(), key= lambda x:-x[1])):
            f.write(f"{name}:{pts}\n")
            if top_n and idx == top_n-1:
                break

def load_highscore_from_file(fn = "./high.txt"):
    """Retrieve dict from file"""
    hs = {}
    try:
        with open(fn,"r") as f:
            for line in f:
                name,_,points = line.partition(":")
                if name and points:
                    hs[name]=int(points)
    except FileNotFoundError:
        return {}
    return hs

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/font.ttf", size)

#=========================== Damage calculation ============================
def move_entities(hero, enemies, timeDelta):
    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    #Player shooting and score
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.center, timeDelta)
        enemy.shoot(hero.sprite.rect.topleft)
        if pygame.sprite.spritecollide(enemy, hero, False):
            enemy.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0: #kill player
                hero.sprite.alive = False
    for proj in EnemyShoot.projectiles:
        proj.move(screen.get_size(), timeDelta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0:
                hero.sprite.alive = False
    #Player shooting and score
    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta)
        enemiesHit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemiesHit:
            proj.kill()
            score += len(enemiesHit)
    return score

#=========================== Rendering ============================
def render_entities(hero, enemies):
    hero.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)
    for proj in EnemyShoot.projectiles:
        proj.render(screen)    
    
#=========================== Player moving ============================
def process_keys(keys, hero, score):
    if keys[pygame.K_w]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_a]:
        hero.sprite.movementVector[0] -= 1
    if keys[pygame.K_s]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movementVector[0] += 1
    if keys[pygame.K_1]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[0]
    if keys[pygame.K_2]and score>50:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]and score>100:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]

#=========================== Player shooting ============================     
def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())

#=========================== Main game loop ============================  
def game_loop():
    done = False
    hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    enemies = pygame.sprite.Group()
    lastEnemyNormal = pygame.time.get_ticks()
    score = 0

    # If player alive loop
    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        screen.blit(BG, (0, 0))
        process_keys(keys, hero, score)
        process_mouse(mouse, hero)
        hero.update()
        
        
        # EnemyNormal spawning process
        if lastEnemyNormal < currentTime - (1000 - score*10 ) and len(enemies) < 50:
            spawnSide = random.random()
            if spawnSide < 0.25:
                enemies.add(EnemyShoot((0, random.randint(0, size[1]))))
            elif spawnSide < 0.5:
                enemies.add(EnemyShoot((size[0], random.randint(0, size[1]))))
            elif spawnSide < 0.75:
                enemies.add(EnemyNormal((random.randint(0, size[0]), 0)))
            else:
                enemies.add(EnemyNormal((random.randint(0, size[0]), size[1])))
            lastEnemyNormal = currentTime
        
        # Enemy and player render
        score += move_entities(hero, enemies, clock.get_time()/15)
        render_entities(hero, enemies)
        
        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(healthRender, (15 + hp*35, 0))
        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        scoreRect = scoreRender.get_rect()
        scoreRect.right = size[0] - 20
        scoreRect.top = 20
        screen.blit(scoreRender, scoreRect)
        
        # Weapon render screen
        
        pygame.display.flip()
        clock.tick(120)
    game_over(score)

#=========================== Game Over screen ============================  

def game_over(score):
    kk = load_highscore_from_file()
    while True:
        screen.blit(BGblured, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Game Over", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))

        SCORE = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                            text_input=str(score), font=get_font(75), base_color="#d7fcd4", hovering_color="#d7fcd4")

        HIGHSCORE = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 450), 
                            text_input=str(list(kk.items())[0]), font=get_font(75), base_color="#d7fcd4", hovering_color="#d7fcd4")
        
        RESTART_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 600), 
                            text_input="RESTART", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [SCORE,HIGHSCORE,  RESTART_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if RESTART_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_loop()

        pygame.display.update()

#=========================== Main menu ============================  

def main_menu():
    while True:
        screen.blit(BGblured, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON,  QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# file does not exist
k = load_highscore_from_file()
#print(k)

## add some highscores to dict
k["psa"]=12
#k["a"]=110
#k["k"]=1110
#k["l"]=1022 
#print(k)
#
# store file, only top 3
store_highscore_in_file(k, top_n=3)

# load back into new dict
kk = load_highscore_from_file()
print(list(k.items())[0])

main_menu()