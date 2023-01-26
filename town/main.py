import sys, json, pygame
from character import TopDownHorse as Horse
from objects import Box 
from groups import CollisionGroup, DrawGroup

pygame.init()

size = width, height = 1680, 1000
screen = pygame.display.set_mode(size)

area = "home.json"

horse = Horse(800,400)

draw = DrawGroup()
collide = CollisionGroup()

clock = pygame.time.Clock()
pygame.key.set_repeat(1)

def loadArea(fileName):
    draw.empty()
    collide.empty()

    draw.add(horse)
    collide.add(horse)

    with open(fileName, "r") as f:
        data = json.load(f)

    dr = data["directory"]
    bg = pygame.image.load("{}/{}".format(dr, data["background"])).convert()
    screen.blit(bg, (0,0))
    draw.bg = bg

    for b in data["boundaries"]:
        x = b["start"]["x"]
        y = b["start"]["y"]
        w = b["end"]["x"] - x
        h = b["end"]["y"] - y
        if w == 0:
            w = 1
        if h == 0:
            h = 1
        collide.add(Box(x, y, w, h))

    for o in data["objects"]:
        i = "{}/{}".format(dr, o["image"])

        x = o["position"]["x"]
        y = o["position"]["y"]
        w = o["hitbox"]["w"] 
        h = o["hitbox"]["h"]

        ob = Box(x, y, w, h, i)

        draw.add(ob)
        collide.add(ob)

def transition(d, fileName):
    with open(fileName, "r") as f:
        data = json.load(f)

    if d in data["adj"]:
        loadArea(data["adj"][d])
        if d == "right": 
            horse.setPosition(x=0-horse.rect.width // 3)
        elif d == "left": 
            horse.setPosition(x=width-2 * horse.rect.width // 3)
        elif d == "top": 
            horse.setPosition(y=height-2 *horse.rect.height // 3)
        elif d == "bottom": 
            horse.setPosition(y=0-horse.rect.height // 3)
        return data["adj"][d]
    else:
        return area

def run():
    global area
    loadArea(area)
    while True:
        clock.tick(60)

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

        t = None
        if horse.rect.x + horse.rect.width // 2 >= width:
            t = "right"
        elif horse.rect.x <= 0 - horse.rect.width // 2:
            t = "left"
        elif horse.rect.y + horse.rect.height // 2 >= height:
            t = "bottom"
        elif horse.rect.y <= 0 - horse.rect.height // 2:
            t = "top"

        if t is not None:
            area = transition(t, area)

        draw.draw(screen)

        if False:
            for c in collide:
                hb = DrawGroup()
                h = c.hitbox.copy()
                b = Box(h.x,h.y,h.width,h.height,(255,0,0))
                hb.add(b)
                hb.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    run()
