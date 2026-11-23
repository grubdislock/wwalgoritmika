#создай игру "Лабиринт"!
from pygame import *
mixer.init()
width = 700
height = 500
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        ww.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = 'up'
        self.direction1 = 'left'

    def update_up(self):
        if self.rect.y <= 250:
            self.direction = 'down'
        if self.rect.y > 450:
            self.direction = 'up'
        if self.direction == 'up':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    def update_left(self):
        if self.rect.x <= 470:
            self.direction1 = 'right'
        if self.rect.x > 615:
            self.direction1 = 'left'
        if self.direction1 == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        ww.blit(self.image, (self.rect.x, self.rect.y))

ww = display.set_mode((width,height))
display.set_caption("Лабиринт")
bg = transform.scale(image.load("background.jpg"), (width,height))

player = Player("hero.png", 5, height - 80, 5)
enemy = Enemy("cyborg.png", width - 80, 280, 2)
enemy2 = Enemy("cyborg.png", 215, 150, 2)
treasure = GameSprite("treasure.png", width - 120, height - 80, 0)

w1 = Wall(150, 14, 88, 200, 220, 90, 10)
w2 = Wall(150, 14, 88, 100, 20, 310, 10)
w3 = Wall(150, 14, 88, 100, 20, 10, 360)
w4 = Wall(150, 14, 88, 200, 220, 10, 320)
w5 = Wall(150, 14, 88, 400, 20, 10, 340)
w6 = Wall(150, 14, 88, 410, 150, 260, 10)
w7 = Wall(150, 14, 88, 500, 260, 10, 250)
w8 = Wall(150, 14, 88, 280, 220, 10, 380)

mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
f1 = font.Font(None, 70)
f2 = font.Font(None, 50)
win = f1.render('YOU ПОБЕДИЛ!', True, (255, 215, 0))
win2 = f2.render('ПОЗДОРОВОЛЯЕМ!', True, (255, 255, 0))
lose = f1.render('YOU ПРОИГРАЛ!', True, (180, 0, 0))
lose2 = f2.render('не расстраивайтетс', True, (255, 19, 89))

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        
        ww.blit(bg,(0,0))

        player.update()
        player.reset()
        enemy.update()
        enemy.reset()
        enemy2.reset()
        treasure.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()

        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, enemy2) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, w8):
            finish = True
            ww.blit(lose, (200, 200))
            ww.blit(lose2, (180, 250))
            kick.play()
        if sprite.collide_rect(player, treasure):
            finish = True
            ww.blit(win, (200, 200))
            ww.blit(win2, (180, 250))
            money.play()

    display.update()
    clock.tick(FPS)
