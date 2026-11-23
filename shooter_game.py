from pygame import *
from random import randint
from time import time as timer

mixer.init()

fire_sound = mixer.Sound('fire.ogg')

font.init()
shrift2 = font.SysFont('Arial', 80)
shrift = font.SysFont('Arial', 36)
text_win = shrift2.render('YOU WON!!!', True, (255,255,255))
text_loser = shrift2.render('YOU LOSE!!!', True, (180,0,0))
score = 0
lose = 0
goal = 10
max_lose = 3
life = 3

img_enemy = 'ufo.png'
img_hero = 'rocket.png'
img_bg = 'galaxy.jpg'
img_bullet = 'bullet.png'
img_ast = 'asteroid.png'
n = randint(1,3)
n2 = randint(1,4)
n3 = randint(1,4)
if n == 1:
    img_enemy = 'ufo.png'
if n == 2:
    img_enemy = 'ufo2.png'

if n2 == 1:
    img_hero = 'rocket.png'
if n2 == 2:
    img_hero = 'rocket2.png'
if n2 == 3:
    img_hero = 'rocket3.png'

if n3 == 1:
    mixer.music.load('space.ogg')
    mixer.music.play()
if n3 == 2:
    mixer.music.load('space2.ogg')
    mixer.music.play()
if n3 == 3:
    mixer.music.load('space3.ogg')
    mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
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
        if keys[K_RIGHT] and self.rect.x < ww_width -80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > ww_height:
            self.rect.x = randint(80, 620)
            self.rect.y = -40
            lose = lose + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ww_width = 700
ww_height = 500

display.set_caption('Шутер')
ww = display.set_mode((ww_width, ww_height))
bg = transform.scale(image.load(img_bg), (ww_width,ww_height))

ship = Player(img_hero, 5, ww_height-100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(80, 620), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

finish = False
run = True
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                fire_sound.play()
                ship.fire()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True

    if not finish:
        ww.blit(bg, (0,0))

        text_score = shrift.render("Счёт:" + str(score), 1, (255, 255, 255))
        ww.blit(text_score, (10, 20))
        text_lose = shrift.render("Пропущено:" + str(lose), 1, (255, 255, 255))
        ww.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()
        bullets.update()
        asteroids.update()
        monsters.update()
        monsters.draw(ww)
        bullets.draw(ww)
        asteroids.draw(ww)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = shrift.render('Reloading...', 1, (150, 0, 0))
                ww.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, 620), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lose >= max_lose:
            finish = True
            ww.blit(text_loser, (200, 200))

        if score >= goal:
            finish = True
            ww.blit(text_win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = shrift2.render(str(life), 1, life_color)
        ww.blit(text_life, (650, 10))

        display.update()

    else:
        finish = False
        score = 0
        lose = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 8):
            monster = Enemy(img_enemy, randint(80, 620), -40, 80, 50, randint(3, 6))
            monsters.add(monster)
        for i in range(1, 4):
            asteroid = Enemy(img_ast, randint(30, 620), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)

    time.delay(50)
