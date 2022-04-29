# -*- coding: utf-8 -*-

import pygame
import random
import math
from Player import Player
from EnemyNormal import EnemyNormal
from EnemyNormal import EnemyNormal


pygame.init()
size    = (800, 600)
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

#=========================== Damage calculation ============================
def move_entities(hero, enemies, timeDelta):
    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.center, timeDelta)
        if pygame.sprite.spritecollide(enemy, hero, False):
            enemy.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0: #kill player
                hero.sprite.alive = False
  
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
    
#=========================== Player moving ============================
def process_keys(keys, hero):
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
    if keys[pygame.K_2]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]

#=========================== Player shooting ============================     
def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())

#=========================== Main game loop ============================  
def game_loop():
    done = False
    player = Player(screen.get_size())
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
        screen.fill(BGCOLOR)
        process_keys(keys, hero)
        process_mouse(mouse, hero)
        hero.update()
        
        
        # EnemyNormal spawning process
        if lastEnemyNormal < currentTime - 200 and len(enemies) < 50:
            spawnSide = random.random()
            if spawnSide < 0.25:
                enemies.add(EnemyNormal((0, random.randint(0, size[1]))))
            elif spawnSide < 0.5:
                enemies.add(EnemyNormal((size[0], random.randint(0, size[1]))))
            elif spawnSide < 0.75:
                enemies.add(EnemyNormal((random.randint(0, size[0]), 0)))
            else:
                enemies.add(EnemyNormal((random.randint(0, size[0]), size[1])))
            lastEnemyNormal = currentTime
        
        score += move_entities(hero, enemies, clock.get_time()/17)
        render_entities(hero, enemies)
        
        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(healthRender, (15 + hp*35, 0))
        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        scoreRect = scoreRender.get_rect()
        scoreRect.right = size[0] - 20
        scoreRect.top = 20
        screen.blit(scoreRender, scoreRect)
        
        pygame.display.flip()
        clock.tick(120)

done = game_loop()
#=========================== End main game loop ============================  
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if keys[pygame.K_r]:
        done = game_loop()
pygame.quit()
