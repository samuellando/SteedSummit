import sys, pygame
pygame.init()

size = width, height = 1680, 1000
speed = [0, 0]
black = 0, 0, 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while True:
    clock.tick_busy_loop(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN: 
          k = event.__dict__["unicode"]
          if k == "d":
              speed[0] += 1
          elif k == "a":
              speed[0] -= 1
          elif k == "w":
              speed[1] -= 1
          elif k == "s":
              speed[1] += 1

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
