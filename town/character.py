import pygame
import spritesheet
from groups import CollisionGroup

class TopDownHorse(pygame.sprite.Sprite):
    irows = [0,1,3,2]
    icols = 3
    scale = 128

    def __init__(self, x, y):
        self.ss = spritesheet.spritesheet("horse-brown.gif")
        pygame.sprite.Sprite.__init__(self)
        self.dir = 1
        self.iframe = 0
        self.frame = 0
        self.anFrame = 5
        self.image = None
        self.updateImage()
        self.rect = pygame.Rect(x,y,self.scale,self.scale)
        self.hitbox = self.rect.copy()
        rw = self.rect.width
        rh = self.rect.height
        self.hitbox = self.rect.inflate(0.5 * rw - rw, 0.5 * rh - rh)
        self.hitbox.y = y + rh - self.hitbox.height
        self.speed = 10

    def updateImage(self):
        self.image = self.ss.image_at((
            self.scale * self.iframe, 
            self.scale * self.irows[self.dir],
            self.scale, self.scale
            ))

    def setPosition(self, x=None, y=None):
        if x != None:
            self.rect.x = x
            self.hitbox.x = x
            self.hitbox.x += self.rect.width // 2
            self.hitbox.x -= self.hitbox.width // 2

        if y != None:
            self.rect.y = y
            self.hitbox.y = y
            self.hitbox.y += self.rect.height
            self.hitbox.y -= self.hitbox.height

    def move(self, d):
        if d[0] == 1:
            self.dir = 1
        elif d[0] == -1:
            self.dir = 2
        elif d[1] == 1:
            self.dir = 3
        elif d[1] == -1:
            self.dir = 0

        self.frame = (self.frame + 1) % self.anFrame
        if self.frame == 0:
            self.iframe = (self.iframe + 1) % self.icols
            self.updateImage()

        x = self.rect.x
        y = self.rect.y

        d = list(map(lambda x:x*self.speed, d))
        
        for i in range(2):
            e = [0 , 0]
            e[i] = d[i]
            self.rect.move_ip(*e)
            self.hitbox.move_ip(*e)
            for g in self.groups():
                if isinstance(g, CollisionGroup):
                    if len(pygame.sprite.spritecollide(self, g, False, collided=(lambda x, y : pygame.Rect.colliderect(x.hitbox, y.hitbox)))) > 1:
                        if i == 0:
                            self.setPosition(x=x)
                        else:
                            self.setPosition(y=y)
                        break