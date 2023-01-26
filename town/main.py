import sys, pygame
from character import TopDownHorse as Horse
from objects import Box 
from groups import CollisionGroup, DrawGroup

pygame.init()

size = width, height = 1680, 1000
screen = pygame.display.set_mode(size)
bg = pygame.image.load("areaHome/bg.png").convert()

wb = Box(0, height, width, 1, (0,0,0))
wt = Box(0, 0, width, 1, (0,0,0))
wl = Box(0, 0, 1, height, (0,0,0))
wr = Box(width, 0, 1, height, (0,0,0))

horse = Horse(800,400)
house = Box(200, -48, 1, 0.5, "areaHome/house.gif")
tree1 = Box(800, 600, 0.2, 0.2, "areaHome/tree.gif")
tree2 = Box(1256, 100, 0.2, 0.2, "areaHome/tree.gif")
well = Box(32, 350, 1, 0.5, "areaHome/well.gif")

draw = DrawGroup()
collide = CollisionGroup()

draw.add(horse, house, tree1, tree2, well)
collide.add(wb, wt, wr, wl, horse, house, tree1, tree2, well)

clock = pygame.time.Clock()
pygame.key.set_repeat(1)

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
        if False:
            for s in collide:
                if s.hitbox is not None:
                    b = Box(s.hitbox.x, s.hitbox.y, s.hitbox.width, s.hitbox.height, (255, 0,0))
                    screen.blit(b.image, b.rect)

        pygame.display.flip()

run()
