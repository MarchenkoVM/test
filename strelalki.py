from pygame import *
import random
from time import time as timer
win_width = 700
win_height = 500
FPS = 60
lost = 0
score = 0
max_lost = 20
goal = 40
hearts = 5
num_fire = 0
rel_time = False
font.init()
font1 = font.SysFont(None, 50)
font2 = font.SysFont(None, 30)
lose = font1.render("You lose", True, (180, 0, 0))
win = font1.render("You win", True, (180, 0, 0))
#mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()
#fire_sound = mixer.Sound("fire.ogg")

window = display.set_mode((win_width, win_height))
display.set_caption("Alien-shooters")
background = transform.scale(image.load("gelex.jpeg"), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 50:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet("bull.png", self.rect.centerx, self.rect.top, 25, 15, 15)
        bullets.add(bullet)
        #fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player("racketo.png", 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

ufo = ["ufo-transformed.png", "ufo2.png", "ufo3.png", "ufo4.png"]
for i in range (1,6):
    monster = Enemy(random.choice(ufo), random.randint(80, win_width - 80), -40, 80, 50, random.randint(2,4))
    monsters.add(monster)

bullets = sprite.Group()

clock = time.Clock()
game = True
finish = False
while game:
    for el in event.get():
        if el.type == QUIT:
            game = False
        elif el.type == KEYDOWN:
            if el.key == K_p:
                if num_fire < 20 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                if num_fire >= 20 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Рахунок пропущених: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_hearts = font2.render("Житті: " + str(hearts), True, (255, 255, 255))
        window.blit(text_hearts, (10, 80))
        ship.update()
        ship.reset()
        bullets.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font2.render("ПЕРЕЗАРЯДКА...", None, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False


        if sprite.spritecollide(ship, monsters, True):
            hearts -= 1
            monster = Enemy(random.choice(ufo), random.randint(80, win_width - 80), -40, 80, 50, random.randint(2, 4))
            monsters.add(monster)

    collides = sprite.groupcollide(monsters, bullets, True, True)

    for c in collides:
        score += 1
        monster = Enemy(random.choice(ufo), random.randint(80, win_width - 80), -40, 80, 50, random.randint(2,4))
        monsters.add(monster)

    if hearts <= 0 or lost >= max_lost:
        finish = True
        window.blit((lose), (200, 200))
    if score >= goal:
        finish = True
        window.blit((win), (200, 200))




    display.update()
    clock.tick(FPS)