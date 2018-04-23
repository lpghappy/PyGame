#!/usr/bin/evn python
#-*- codeing:utf-8 -*-
#Author:Pinggen Li

"""
    定义敌机
"""

from random import randint

import pygame


class SmallEnemy(pygame.sprite.Sprite):
    """
    定义小飞机敌人
    """
    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy1.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.mask = pygame.mask.from_surface(self.image) # 获取飞机图像的掩膜用以更加精确的碰撞检测
        self.speed = 2
        # 定义敌机出现的位置，保证敌机不会在程序已经开始就立即出现
        self.rect.left, self.rect.top = (
            randint(0, self.width - self.rect.width), randint(-5 * self.rect.height, -5)
        )
        self.active = True
        #加载飞机损毁图片
        self.destroy_image = []
        self.destroy_image.extend(
            [
                pygame.image.load("material/image/enemy1_down1.png"),
                pygame.image.load("material/image/enemy1_down2.png"),
                pygame.image.load("material/image/enemy1_down3.png"),
                pygame.image.load("material/image/enemy1_down4.png")
            ]
        )

    def move(self):
        """
        定义敌机的移动函数
        :return:
        """
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        """
        当敌机向下移动出屏幕时, 以及敌机死亡
        :return:
        """
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width), randint(-5 * self.rect.height, 0))