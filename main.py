# coding:utf-8
# 用面向对象思想编写飞机大战游戏

import pygame
import time
import random


# 定义子弹类
class Bullet:
    def restart(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2

    def __init__(self):
        # 初始化子弹位置及图片
        self.image = pygame.image.load('bullet.png')
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2

    def move(self):
        # 处理子弹运动
        if self.y < 0:
            self.restart()
        else:
            self.y -= 10


# 定义Enemy类
class Enemy:
    def restart(self):
        self.x = random.randint(0, background.get_width() - self.image.get_width())
        self.y = random.randint(-200, -50)
        self.speed = random.randint(0, 3) + 1
        self.ACTIVE = False

    def __init__(self):
        self.image = pygame.image.load('enemy.png')
        self.restart()

    def move(self):
        if self.y < 800:
            self.y += self.speed
            if self.y > 0:
                self.ACTIVE = True
        else:
            self.restart()


# 定义战机
class Fighter:
    def __init__(self):
        self.image = pygame.image.load('plane.png')
        self.x = 0
        self.y = 0
        # 子弹list
        self.i = 0
        self.max_bullets = 20
        self.bullets = []

    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2

    # 定义子弹发射动作
    def shoot(self):
        # 创建子弹实例，如果未满最大子弹数则增加实例，如果已满则重新定义实例
        if len(self.bullets) < self.max_bullets:
            self.bullets.append(Bullet())
        else:
            self.bullets[self.i % 5] = Bullet()
            self.i += 1

    # 发射一枚炸弹
    def bomb(self):
        global score
        for e in enemy:
            if e.ACTIVE:
                score += 100
                e.restart()


# 检测子弹是否命中敌机
def check_hit(bullet, enemy):
    if (bullet.x + bullet.image.get_width()/1.5 > enemy.x and bullet.x < enemy.x + enemy.image.get_width()/1.5) and \
            (bullet.y + bullet.image.get_height()/1.5 > enemy.y and bullet.y < enemy.y + enemy.image.get_height()/1.5):
        enemy.restart()
        bullet.restart()
        return True
    else:
        return False


# 检测是否与敌机碰撞
def check_crack(fighter, enemy):
    if (enemy.x + enemy.image.get_width()/1.5 > fighter.x and enemy.x < fighter.x + fighter.image.get_width()/1.5) and \
            (enemy.y + enemy.image.get_height()/1.5 > fighter.y and enemy.y < fighter.y + fighter.image.get_height()/1.5):
        print 'crack'
        return True
    else:
        return False

# 初始化pygame，为使用应用做准备
pygame.init()
# 载入背景图
background = pygame.image.load('bg.jpg')
# 载入结束背景图，定义结束标记
game_over = pygame.image.load('gameover.jpg')
GAMEOVER = False
# 创建一个窗口，大小与背景图一致
screen = pygame.display.set_mode((background.get_width(), background.get_height()), 0, 32)
# 设置窗口标题
pygame.display.set_caption('飞机大战')
# 创建enemy列表
max_enemy = 20
enemy = []
for i in range(max_enemy):
    enemy.append(Enemy())
# 创建一个fighter实例
fighter = Fighter()
# 初始化分数
global score
score = 0
# None表示默认字体，32表示字号
font1 = pygame.font.Font(None, 32)
font2 = pygame.font.Font(None, 24)
# 初始化fps
fps_count = 100
# 子弹间隔
b_interval = 100
b_count = b_interval

while True:
    start_time = time.time()
    for event in pygame.event.get():
        # 接收到退出事件后退出程序
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            fighter.bomb()
    if not GAMEOVER:
        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制子弹，处理子弹运动
        if b_count >= b_interval:
            fighter.shoot()
            b_count = 0
        else:
            b_count += 1
        for i in fighter.bullets:
            i.move()
            screen.blit(i.image, (i.x, i.y))
        # 绘制敌机，处理敌机运动
        for i in enemy:
            i.move()
            screen.blit(i.image, (i.x, i.y))
            for b in fighter.bullets:
                if check_hit(b, i):
                    score += 100
            if not GAMEOVER:
                GAMEOVER = check_crack(fighter, i)
        # 绘制分数
        text1 = font1.render('Score:%d'% score, 1, (0, 0, 0))
        screen.blit(text1, (0, 0))
        # 绘制战机，处理战机运动
        screen.blit(fighter.image, (fighter.x, fighter.y))
        fighter.move()
    if GAMEOVER:
        text2 = font1.render('Game Over', 1, (0, 0, 0))
        screen.blit(text2, (background.get_width()/3, background.get_height()/2))
    # 刷新屏幕
    time.sleep(0.001)
    end_time = time.time()
    if fps_count >= 50:
        fps = int(1.0 / (end_time - start_time))
        fps_count = 0
    else:
        fps_count += 1
    if not GAMEOVER:
        text3 = font2.render('fps:%d' % fps, 1, (0, 0, 0))
    screen.blit(text3, (background.get_width() - text3.get_width(), 0))
    pygame.display.update()

