#!/usr/bin/evn python
#-*- codeing:utf-8 -*-
#Author:Pinggen Li

import pygame

pygame.init()  # 游戏初始化
pygame.mixer.init()  # 混音器初始化

# 游戏背景音乐
pygame.mixer.music.load("material/sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)

# 子弹发射音乐
bullet_sound = pygame.mixer.Sound("material/sound/bullet.wav")
bullet_sound.set_volume(0.2)

# 我方飞机挂了的音乐
me_down_sound = pygame.mixer.Sound("material/sound/game_over.wav")
me_down_sound.set_volume(0.2)

# 敌方飞机挂了的音乐
enemy1_down_sound = pygame.mixer.Sound("material/sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
