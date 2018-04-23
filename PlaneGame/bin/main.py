#!/usr/bin/evn python
#-*- codeing:utf-8 -*-
#Author:Pinggen Li

import sys

from pygame.locals import *

from config.settings import *
from src.plane import OurPlane
from src.enemy import SmallEnemy
from src.bullet import Bullet

bg_size = 480, 852  # 初始化游戏背景大小（宽，高）
screen = pygame.display.set_mode(bg_size)  # 设置背景对话框
pygame.display.set_caption("飞机大战")  # 设置标题

background = pygame.image.load("material/image/background.png")  # 加载背景图片，并设置为不透明

# 获取我方飞机
our_plane = OurPlane(bg_size)

def add_small_enemies(group1, group2, num):  
    """
    添加小型敌机
    指定个敌机对象添加到精灵组（sprite.group）
    参数group1、group2是两个精灵组类型的形参，用以存储多个精灵对象（敌机）。
    需要注意的一点是group既然是特定的精灵组结构体，在向其内部添加精灵对象时需要调用其对应的成员函数add()
    :return:
    """
    for i in range(num):
        small_enemy = SmallEnemy(bg_size)
        group1.add(small_enemy)
        group2.add(small_enemy)

def main():
    # 响应音乐
    pygame.mixer.music.play(loops=-1)  # loops 对应值为 -1 则音乐会无限循环播放
    running = True
    switch_image = False  # 切换飞机的标识位(使飞机具有喷气式效果)
    delay = 60  # 对一些效果进行延迟, 效果更好一些

    enemies = pygame.sprite.Group()  # 生成敌方飞机组(一种精灵组用以存储所有敌机精灵)
    small_enemies = pygame.sprite.Group()  # 敌方小型飞机组(不同型号敌机创建不同的精灵组来存储)

    add_small_enemies(small_enemies, enemies, 4)  # 生成若干地方小型飞机

    # 定义子弹, 各种敌机和我方敌机的毁坏图像索引
    bullet_index = 0
    e1_destroy_index = 0
    me_destroy_index = 0

    # 定义子弹实例化个数
    bullet1 = []
    bullet_num = 6
    for i in range(bullet_num):
        bullet1.append(Bullet(our_plane.rect.midtop))

    while running:
        # 绘制背景图
        screen.blit(background, (0, 0))

        # 微信的飞机貌似是喷气式的, 那么这个就涉及到一个帧数的问题
        clock = pygame.time.Clock()
        clock.tick(60)

        # 绘制我方飞机的两种不同的形式
        if not delay % 3:
            switch_image = not switch_image

        for each in small_enemies:
            if each.active:
                # 随机循环输出小飞机敌机
                for e in small_enemies:
                    e.move()
                    screen.blit(e.image, e.rect)
            else:
                if e1_destroy_index == 0:
                    enemy1_down_sound.play()
                screen.blit(each.destroy_image[e1_destroy_index], each.rect)
                e1_destroy_index = (e1_destroy_index + 1 ) % 4
                if e1_destroy_index == 0:
                    each.reset()

        # 当我方飞机存活状态, 正常展示
        if our_plane.active:
            if switch_image:
                screen.blit(our_plane.image_one, our_plane.rect)
            else:
                screen.blit(our_plane.image_two, our_plane.rect)

            # 飞机存货状态下才可以发射子弹
            if not (delay % 10):  # 每十帧发射一颗移动的子弹
                bullet_sound.play()
                bullets = bullet1
                bullets[bullet_index].reset(our_plane.rect.midtop)
                bullet_index = (bullet_index + 1) % bullet_num

            for b in bullets:
                if b.active:  # 只有激活的子弹才能击中敌机
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:  #如果子弹击中飞机
                        b.active = False  # 子弹损毁
                        for e in enemies_hit:
                            e.active = False  #小型敌机损毁

        # 毁坏状态绘制爆炸的场面
        else:
            if not (delay % 3):
                screen.blit(our_plane.destroy_images[me_destroy_index], our_plane.rect)
                me_destroy_index = (me_destroy_index + 1) % 4
                if me_destroy_index == 0:
                    me_down_sound.play()
                    our_plane.reset()

        # 调用 pygame 实现的碰撞方法 spritecollide (我方飞机如果和敌机碰撞, 更改飞机的存活属性)
        enemies_down = pygame.sprite.spritecollide(our_plane, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            our_plane.active = False
            for row in enemies:
                row.active = False

        # 获得用户所有的键盘输入序列(如果用户通过键盘发出“向上”的指令,其他类似)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            our_plane.move_up()
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            our_plane.move_down()
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            our_plane.move_left()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            our_plane.move_right()

        # 按键为 j 飞机更改存活标识
        if key_pressed[pygame.K_j]:
            our_plane.active = False

        # 响应用户的操作(一定要有响应的用户操作)
        for event in pygame.event.get():
            if event.type == 12: # 如果用户按下屏幕上的关闭按钮，触发QUIT事件，程序退出
                pygame.quit()
                sys.exit()

        if delay == 0:
            delay = 60
        delay -= 1


        # 再而我们将背景图像并输出到屏幕上面
        pygame.display.flip()

# if __name__ == '__main__':
#     main()
