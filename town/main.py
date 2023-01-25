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

        hx = self.hitbox.x
        hy = self.hitbox.y

        d = list(map(lambda x:x*self.speed, d))
        
        for i in range(2):
            e = [0 , 0]
            e[i] = d[i]
            self.rect.move_ip(*e)
            self.hitbox.move_ip(*e)
            for g in self.groups():
                if isinstance(g, Collision_Group):
                    if len(pygame.sprite.spritecollide(self, g, False, collided=(lambda x, y : pygame.Rect.colliderect(x.hitbox, y.hitbox)))) > 1:
                        if i == 0:
                            print("x col")
                            self.rect.x = x
                            self.hitbox.x = hx
                        else:
                            print("y col")
                            self.rect.y = y
                            self.hitbox.y = hy
                        break

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=()):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(color, str):
            self.image = pygame.image.load(color).convert()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            rw = self.rect.width
            rh = self.rect.height
            self.hitbox = self.rect.inflate(w * rw - rw, h * rh - rh)
            self.hitbox.y = y + rh - self.hitbox.height
        else:
            self.image = pygame.Surface((w, h))
            self.image.fill(color)
            self.rect = pygame.Rect(x,y,w, h)
            self.hitbox = self.rect.copy()

class Collision_Group(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

wb = Box(0, height-64, width, 1, (0,0,0))
wt = Box(0, 0, width, 1, (0,0,0))
wl = Box(0, 0, 1, height, (0,0,0))
wr = Box(width, 0, 1, height, (0,0,0))

horse = Horse(800,400)
house = Box(200, -48, 1, 0.5, "house.gif")
tree1 = Box(800, 600, 0.2, 0.2, "tree.gif")
tree2 = Box(1256, 100, 0.2, 0.2, "tree.gif")
well = Box(32, 350, 1, 0.5, "well.gif")

draw = pygame.sprite.LayeredUpdates() 
collide = Collision_Group()

draw.add(horse, house, tree1, tree2, well)
collide.add(wb, wt, wr, wl, horse, house, tree1, tree2, well)

print(draw.layers())


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
        for s in collide:
            if s.hitbox is not None:
                b = Box(s.hitbox.x, s.hitbox.y, s.hitbox.width, s.hitbox.height, (255, 0,0))
                screen.blit(b.image, b.rect)

        pygame.display.flip()

run()
