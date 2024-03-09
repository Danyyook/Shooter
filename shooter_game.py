#Создай собственный Шутер!

from pygame import *
from random import *
font.init()
score = 0
lost = 0
font2 = font.SysFont('Arial',36)
font3 = font.SysFont('Arial',110)
game = True
clock = time.Clock()
window_hieght = 500
window_wieght = 700
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.01)
window = display.set_mode((window_wieght, window_hieght))
display.set_caption('шутер')
fon = transform.scale(image.load('galaxy.jpg'), (700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >5:
            self.rect.x -=self.speed
        if keys[K_d] and self.rect.x < window_wieght - 65:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -10, 15, 20)
        bullets.add(bullet)

        
class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_hieght:
            self.rect.x = randint(0,650)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y < 0:
            self.kill()

    


player1 = Player('player.png', 500, 400, 10, 100, 100)
finish = False
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('monster.png', randint(0,650), 0, randint(1,2), 50, 50)
    monsters.add(monster)
for i in range(2):
    asteroid = Enemy('asteroid.png', randint(0,650), 0, randint(1,2), 50, 50)
    asteroids.add(asteroid)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                player1.fire()
    if not finish:
        window.blit(fon,(0,0))
        text = font2.render('Счет: '+str(score),1,(255,255,255))
        window.blit(text,(10,10))
        text2 = font2.render('Пропещено: '+str(lost),1,(255,255,255))
        window.blit(text2,(10,35))
        collides = sprite.groupcollide(bullets, monsters, True, True)
        collides1 = sprite.groupcollide(bullets, asteroids, True, True)
        for collide in collides:
            score += 1
            monster = Enemy('monster.png', randint(0,650), 0, randint(1,2), 50, 50)
            monsters.add(monster)
        
        bullets.update()      
        monsters.update()
        asteroids.update()
        player1.update()
        player1.reset()
        asteroids.draw(window)
        bullets.draw(window) 
        monsters.draw(window)
        if score >= 10:
            finish = True
            win_text = font3.render('You Win!',1,(200,0,0))
            window.blit(win_text,(180, 200))
        if lost >= 5:
            finish = True
            loos_text = font3.render('You Lose!',1,(200,0,0))
            window.blit(loos_text,(180, 200))

    display.update()
    clock.tick(60)