from random import randint
from pygame import *
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700, 500))

lost = 0
score = 0
win_width = 700

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 36)

lose = font2.render('Ты проиграл', True,(180,0,0))
win = font2.render('Ты победил', True,(255,215,0))
img_back = "galaxy.jpg"
img_bullet = "bullet.png"  
img_hero = "rocket.png"
img_enemy = "asteroid.png"
win_height = 500

window.blit(background,(0, 0))
class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-50, self.rect.top,10,20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Nokia(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40,80,80, randint(1, 6))
    monsters.add(monster)

bullets = sprite.Group()

mysors = sprite.Group()
for i in range(3, 5):
    mysor = Nokia("nokia.png", randint(80, win_width - 80), -40,70,125, randint(1, 6))
    mysors.add(mysor)


finish = False
run = True
ship = Player(img_hero,5,win_height-100,100,100,10)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))
        text = font2.render('счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' '' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.reset()
        ship.update()
       
        mysors.update()
        mysors.draw(window)       
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40,80,80, randint(1, 5))
            monsters.add(monster)
             
        if sprite.spritecollide(ship, monsters, False) or lost >= 3 or sprite.spritecollide(ship, mysors, False):
            finish = True
            window.blit(lose, (280, 200))

        if score >= 30:
            finish = True
            window.blit(win, (280, 200))

        if finish == True:
            mixer.music.stop()    
        display.update()    

    
    time.delay(50)        
    