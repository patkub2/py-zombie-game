# -*- coding: utf-8 -*-


import pygame, sys
import random
from Player import Player
from EnemyNormal import EnemyNormal
from EnemyShoot import EnemyShoot
from button import Button
from os import path
from datetime import datetime

pygame.init()
size    = (1280, 720)
BGCOLOR = (158, 255, 166)
screen = pygame.display.set_mode(size)
scoreFont = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down")
gameDisplay = pygame.display.set_mode(size)

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
enemies = pygame.sprite.Group()
lastEnemyNormal = 0
score = 0
clock = pygame.time.Clock()
BG = pygame.image.load("assets/BG.jpg")
BGblured = pygame.image.load("assets/BGblured.png")

pistol = pygame.image.load('assets/pistol.png')
pistol = pygame.transform.scale(pistol, (80, 80)) 
machinegun = pygame.image.load('assets/shotgun.png')
machinegun = pygame.transform.scale(machinegun, (80, 80)) 
shotgun = pygame.image.load('assets/submachinegun.png')
shotgun = pygame.transform.scale(shotgun, (80, 80)) 

def weapon(img):
    gameDisplay.blit(img, (20,620))

def load_score():
        # load high score
        with open('highscore.txt') as f:
            first_line = f.readline()
            try:
                return int(first_line)
            except:
                return 0

                
def load_date():
        # load high score
        with open('highscore.txt') as f:
            f.readline()
            second_line = f.readline()
            try:
                return second_line
            except:
                return 0


def write_data(score):
        # write high score
        dir = path.dirname(__file__)
        with open(path.join(dir, "highscore.txt"), 'w') as f:
                f.write(str(score)+"\n"+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        

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
    if keys[pygame.K_2]and score>20:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]and score>40:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]
    if score==20:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if score==40:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]
    

#=========================== Player moving ============================
def process_aviable_weapon(hero):
    
    if hero.sprite.equippedWeapon == hero.sprite.availableWeapons[0]:
        weapon(pistol)
    if hero.sprite.equippedWeapon == hero.sprite.availableWeapons[1]:
        weapon(machinegun)
    if hero.sprite.equippedWeapon == hero.sprite.availableWeapons[2]:
        weapon(shotgun)

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
        process_aviable_weapon(hero)
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
    highscore = load_score()
    date = load_date()
    
    highscoretext = "HIGHSCORE:"+str(highscore)
    if score > highscore:
        highscoretext ="NEW HIGHSCORE!"
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        highscore = score
        write_data(score)
    while True:
        screen.blit(BGblured, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Game Over", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))

        DATE_TEXT = get_font(20).render(str(date), True, "#ffffff")
        DATE_RECT = DATE_TEXT.get_rect(center=(640, 515))

        SCORE = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 360), 
                            text_input="SCORE:"+str(score), font=get_font(40), base_color="#d7fcd4", hovering_color="#d7fcd4")

        HIGHSCORE = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 480), 
                            text_input=highscoretext, font=get_font(40), base_color="#d7fcd4", hovering_color="#d7fcd4")
        
        RESTART_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 600), 
                            text_input="RESTART", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(DATE_TEXT, DATE_RECT)

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

        MENU_TEXT = get_font(70).render("ZOMBIE SHOOTER", True, "#ffffff")
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


#score_board()
#game_over(23)
main_menu()