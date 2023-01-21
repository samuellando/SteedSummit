import sys, pygame
import spritesheet
pygame.init()

size = width, height = 1680, 1000
black = 0, 0, 0
clock = pygame.time.Clock()
pygame.key.set_repeat(1)

screen = pygame.display.set_mode(size)

bg = pygame.image.load("bg.png").convert()

class Horse(pygame.sprite.Sprite):
    ss = spritesheet.spritesheet("horse-brown.gif")
    irows = [0,1,3,2]
    icols = 3
    scale = 128

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.dir = 1
        self.iframe = 0
        self.frame = 0
        self.anFrame = 5
        self.image = None
        self.updateImage()
        self.rect = pygame.Rect(x,y,self.scale,self.scale)
        self.speed = 10

    def updateImage(self):
        self.image = self.ss.image_at((
            self.scale * self.iframe, 
            self.scale * self.irows[self.dir],
            self.scale, self.scale
            ))

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

        d = list(map(lambda x:x*self.speed, d))
        x, y = self.rect.x, self.rect.y
        
        for i in range(2):
            e = [0 , 0]
            e[i] = d[i]
            self.rect.move_ip(*e)
            for g in self.groups():
                if isinstance(g, Collision_Group):
                    if len(pygame.sprite.spritecollide(self, g, False)) > 1:
                        if i == 0:
                            self.rect.x = x
                        else:
                            self.rect.y = y
                        break

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h=-1, color=()):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(w, str):
            self.image = pygame.image.load(w).convert()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.image = pygame.Surface((w, h))
            self.image.fill(color)
            self.rect = pygame.Rect(x,y,w, h)

class Collision_Group(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

wb = Box(0, height-64, width, 1, (0,0,0))
wt = Box(0, 0, width, 1, (0,0,0))
wl = Box(0, 0, 1, height, (0,0,0))
wr = Box(width, 0, 1, height, (0,0,0))

horse = Horse(800,400)
house = Box(200, -48, "house.gif")
tree1 = Box(800, 600, "tree.gif")
tree2 = Box(1256, 100, "tree.gif")
well = Box(32, 350, "well.gif")

draw = pygame.sprite.LayeredUpdates() 
collide = Collision_Group()

draw.add(horse, house, tree1, tree2, well)
collide.add(wb, wt, wr, wl, horse, house, tree1, tree2, well)

def run():
    while True:
        clock.tick(60)
        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

        keys =  pygame.key.get_pressed()
        d = [0, 0]
        if keys[pygame.K_d]:
          d[0] = 1
        elif keys[pygame.K_a]:
          d[0] = -1
        if keys[pygame.K_s]:
          d[1] = 1
        elif keys[pygame.K_w]:
          d[1] = -1

        if d[0] != 0 or d[1] != 0:
            horse.move(d)

        draw.draw(screen)

        pygame.display.flip()

run()
