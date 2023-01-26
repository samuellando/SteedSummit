import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=(0,0,0,0)):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(color, str):
            self.image = pygame.image.load(color).convert()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            rw = self.rect.width
            rh = self.rect.height
            self.hitbox = self.rect.inflate(w - rw, h - rh)
            self.hitbox.y = y + rh - self.hitbox.height
        else:
            self.image = pygame.Surface((w, h))
            self.image.fill(color)
            self.rect = pygame.Rect(x,y,w, h)
            self.hitbox = self.rect.copy()